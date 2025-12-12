"""
Primitive Router - Intelligent routing from primitive names to implementations.

This module implements the core routing intelligence that maps a primitive name
(e.g., "think") plus execution context to the optimal implementation (e.g., ThinkDeep,
ThinkFast, CodeAnalysisThink).

Routing uses a 5-layer intelligence system:
1. Experience Layer: O(1) hash lookup for known patterns
2. Knowledge Layer: Rule-based matching from knowledge base
3. Heuristics Layer: Multi-factor scoring (capability, history, load)
4. LLM Intelligence Layer: Deep reasoning for novel/ambiguous cases
5. JIT Synthesis: Dynamic code generation when no implementation exists

The router enables separation between:
- WHAT: Primitive names (operations) - defined in catalog
- HOW: Implementations (concrete classes) - registered with router
- WHEN: Routing decisions (context-based selection) - made by intelligence layers
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
from enum import Enum
import threading
import hashlib
import time
import logging

from brainary.memory.working import WorkingMemory
from brainary.primitive.base import Primitive, PrimitiveResult
from brainary.primitive.catalog import get_primitive_catalog, is_valid_primitive
from brainary.core.context import ExecutionContext

logger = logging.getLogger(__name__)


class RoutingSource(Enum):
    """Source of routing decision."""
    EXPERIENCE = "experience"       # L1: Cached from history
    KNOWLEDGE = "knowledge"          # L2: Rule-based matching  
    HEURISTICS = "heuristics"        # L3: Multi-factor scoring
    LLM_REASONING = "llm_reasoning"  # L4: Deep analysis
    JIT_SYNTHESIS = "jit_synthesis"  # L5: Dynamic generation
    DEFAULT = "default"              # Fallback to generic


@dataclass
class RoutingDecision:
    """Result of routing intelligence."""
    
    implementation: Primitive           # Selected implementation
    source: RoutingSource              # How decision was made
    confidence: float                  # Confidence in decision [0-1]
    rationale: str                     # Human-readable explanation
    alternatives: List[Tuple[Primitive, float]] = field(default_factory=list)  # Other candidates
    latency_ms: float = 0.0            # Time taken to route
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            'implementation': self.implementation.name,
            'source': self.source.value,
            'confidence': self.confidence,
            'rationale': self.rationale,
            'alternatives': [(impl.name, score) for impl, score in self.alternatives],
            'latency_ms': self.latency_ms,
        }


@dataclass
class RoutingStatistics:
    """Statistics for an implementation's performance."""
    
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    total_latency_ms: float = 0.0
    total_tokens: int = 0
    avg_confidence: float = 0.0
    domain_scores: Dict[str, float] = field(default_factory=dict)
    current_load: int = 0  # Current number of active executions
    max_concurrent: int = 10  # Maximum concurrent executions
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_calls == 0:
            return 0.0
        return self.successful_calls / self.total_calls
    
    @property
    def avg_latency_ms(self) -> float:
        """Calculate average latency."""
        if self.total_calls == 0:
            return 0.0
        return self.total_latency_ms / self.total_calls
    
    @property
    def avg_tokens(self) -> float:
        """Calculate average token usage."""
        if self.total_calls == 0:
            return 0.0
        return self.total_tokens / self.total_calls
    
    def record_execution(
        self,
        success: bool,
        latency_ms: float,
        tokens: int,
        confidence: float,
        domain: Optional[str] = None
    ) -> None:
        """Record an execution."""
        self.total_calls += 1
        if success:
            self.successful_calls += 1
        else:
            self.failed_calls += 1
        
        self.total_latency_ms += latency_ms
        self.total_tokens += tokens
        
        # Update running average of confidence
        alpha = 0.9  # Exponential moving average factor
        self.avg_confidence = alpha * self.avg_confidence + (1 - alpha) * confidence
        
        # Update domain score
        if domain:
            if domain not in self.domain_scores:
                self.domain_scores[domain] = 0.0
            # Boost domain score on success
            if success:
                self.domain_scores[domain] = min(1.0, self.domain_scores[domain] + 0.1)


class ExperienceCache:
    """
    Layer 1: Experience cache for O(1) routing.
    
    Caches successful routing decisions for known context signatures.
    """
    
    def __init__(self, max_size: int = 10000):
        """
        Initialize cache.
        
        Args:
            max_size: Maximum cache entries
        """
        self._cache: Dict[str, Tuple[str, float, int]] = {}  # signature -> (impl_name, confidence, hits)
        self._max_size = max_size
        self._lock = threading.RLock()
    
    def compute_signature(
        self,
        primitive_name: str,
        context: ExecutionContext,
        **kwargs
    ) -> str:
        """
        Compute context signature for caching.
        
        Args:
            primitive_name: Name of primitive
            context: Execution context
            **kwargs: Additional parameters
            
        Returns:
            Hash signature string
        """
        # Build signature from key context features
        sig_parts = [
            primitive_name,
            context.domain or "general",
            str(context.quality_threshold),
            str(int(context.time_pressure * 10)),
            str(int(context.criticality * 10)),
        ]
        
        # Add relevant kwargs
        for key in sorted(kwargs.keys()):
            if key in ['depth', 'mode', 'approach', 'style']:
                sig_parts.append(f"{key}={kwargs[key]}")
        
        # Hash to fixed-length signature
        sig_str = "|".join(sig_parts)
        return hashlib.sha256(sig_str.encode()).hexdigest()[:16]
    
    def get(self, signature: str, confidence_threshold: float = 0.95) -> Optional[str]:
        """
        Get cached implementation name.
        
        Args:
            signature: Context signature
            confidence_threshold: Minimum confidence required
            
        Returns:
            Implementation name if cached and confident, None otherwise
        """
        with self._lock:
            if signature in self._cache:
                impl_name, confidence, hits = self._cache[signature]
                if confidence >= confidence_threshold:
                    # Update hit count
                    self._cache[signature] = (impl_name, confidence, hits + 1)
                    return impl_name
            return None
    
    def put(
        self,
        signature: str,
        impl_name: str,
        confidence: float = 0.95
    ) -> None:
        """
        Cache a routing decision.
        
        Args:
            signature: Context signature
            impl_name: Implementation name
            confidence: Decision confidence
        """
        with self._lock:
            # Evict oldest if full
            if len(self._cache) >= self._max_size:
                # Remove entry with lowest hits
                min_sig = min(self._cache.items(), key=lambda x: x[1][2])[0]
                del self._cache[min_sig]
            
            self._cache[signature] = (impl_name, confidence, 1)
    
    def update_confidence(self, signature: str, success: bool) -> None:
        """
        Update confidence based on execution outcome.
        
        Args:
            signature: Context signature
            success: Whether execution succeeded
        """
        with self._lock:
            if signature in self._cache:
                impl_name, confidence, hits = self._cache[signature]
                # Adjust confidence based on outcome
                if success:
                    new_confidence = min(1.0, confidence + 0.01)
                else:
                    new_confidence = max(0.0, confidence - 0.05)
                self._cache[signature] = (impl_name, new_confidence, hits)


class PrimitiveRouter:
    """
    Intelligent router from primitive names to implementations.
    
    Implements 5-layer routing intelligence:
    1. Experience: Fast O(1) lookup for known patterns
    2. Knowledge: Rule-based matching
    3. Heuristics: Multi-factor scoring
    4. LLM: Deep reasoning for ambiguous cases
    5. JIT: Dynamic synthesis for missing implementations
    """
    
    def __init__(self):
        """Initialize router."""
        self._implementations: Dict[str, List[Primitive]] = {}  # primitive_name -> [implementations]
        self._statistics: Dict[str, RoutingStatistics] = {}  # impl_name -> stats
        self._experience_cache = ExperienceCache()
        self._lock = threading.RLock()
        self._catalog = get_primitive_catalog()
        self._load_lock = threading.RLock()  # Separate lock for load tracking
    
    def register_implementation(
        self,
        primitive_name: str,
        implementation: Primitive,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register an implementation for a primitive.
        
        Args:
            primitive_name: Name of primitive (must be in catalog)
            implementation: Implementation instance
            metadata: Optional metadata
            
        Raises:
            ValueError: If primitive name not in catalog
        """
        # Validate primitive name
        if not is_valid_primitive(primitive_name):
            raise ValueError(
                f"Primitive '{primitive_name}' not in catalog. "
                f"Use catalog.register() to define new primitives."
            )
        
        with self._lock:
            # Register implementation
            if primitive_name not in self._implementations:
                self._implementations[primitive_name] = []
            self._implementations[primitive_name].append(implementation)
            
            # Initialize statistics
            impl_name = implementation.name
            if impl_name not in self._statistics:
                self._statistics[impl_name] = RoutingStatistics()
    
    def get_implementations(self, primitive_name: str) -> List[Primitive]:
        """
        Get all registered implementations for a primitive.
        
        Args:
            primitive_name: Primitive name
            
        Returns:
            List of implementations
        """
        with self._lock:
            return self._implementations.get(primitive_name, [])
    
    def route(
        self,
        primitive_name: str,
        context: ExecutionContext,
        **kwargs
    ) -> RoutingDecision:
        """
        Route primitive name to optimal implementation.
        
        This is the main entry point for intelligent routing.
        
        Args:
            primitive_name: Name of primitive to route
            context: Execution context
            **kwargs: Additional parameters
            
        Returns:
            RoutingDecision with selected implementation
            
        Raises:
            ValueError: If primitive not registered or no implementations available
        """
        start_time = time.time()
        
        logger.debug(f"ROUTER: Routing '{primitive_name}'")
        
        # Validate primitive
        if not is_valid_primitive(primitive_name):
            logger.error(f"        ✗ Unknown primitive: {primitive_name}")
            raise ValueError(f"Unknown primitive: {primitive_name}")
        
        # Get available implementations
        implementations = self.get_implementations(primitive_name)
        if not implementations:
            logger.error(f"        ✗ No implementations registered for: {primitive_name}")
            raise ValueError(f"No implementations registered for: {primitive_name}")
        
        logger.debug(f"        Found {len(implementations)} implementations: {[i.name for i in implementations]}")
        
        # Compute context signature
        signature = self._experience_cache.compute_signature(
            primitive_name, context, **kwargs
        )
        
        # Layer 1: Experience Cache (O(1))
        logger.debug(f"        Trying Layer 1: Experience Cache")
        cached_impl_name = self._experience_cache.get(signature)
        if cached_impl_name:
            # Find implementation by name
            impl = next((i for i in implementations if i.name == cached_impl_name), None)
            if impl:
                logger.debug(f"        ✓ Layer 1 HIT: {impl.name} (cached)")
                latency_ms = (time.time() - start_time) * 1000
                return RoutingDecision(
                    implementation=impl,
                    source=RoutingSource.EXPERIENCE,
                    confidence=0.95,
                    rationale=f"Cached from experience (signature: {signature})",
                    latency_ms=latency_ms,
                )
        logger.debug(f"        Layer 1 MISS: No cached decision")
        
        # Layer 2: Knowledge Rules
        logger.debug(f"        Trying Layer 2: Knowledge Rules")
        impl, confidence = self._route_via_knowledge(
            primitive_name, implementations, context, **kwargs
        )
        if impl and confidence >= 0.85:
            logger.debug(f"        ✓ Layer 2 HIT: {impl.name} (confidence={confidence:.2f})")
            latency_ms = (time.time() - start_time) * 1000
            # Cache this decision
            self._experience_cache.put(signature, impl.name, confidence)
            return RoutingDecision(
                implementation=impl,
                source=RoutingSource.KNOWLEDGE,
                confidence=confidence,
                rationale="Matched knowledge rules",
                latency_ms=latency_ms,
            )
        logger.debug(f"        Layer 2 MISS: No strong knowledge match")
        
        # Layer 3: Heuristic Scoring
        logger.debug(f"        Trying Layer 3: Heuristic Scoring")
        impl, confidence, alternatives = self._route_via_heuristics(
            primitive_name, implementations, context, **kwargs
        )
        if impl and confidence >= 0.7:
            logger.debug(f"        ✓ Layer 3 HIT: {impl.name} (confidence={confidence:.2f})")
            latency_ms = (time.time() - start_time) * 1000
            # Cache if confidence high enough
            if confidence >= 0.85:
                self._experience_cache.put(signature, impl.name, confidence)
            return RoutingDecision(
                implementation=impl,
                source=RoutingSource.HEURISTICS,
                confidence=confidence,
                rationale=f"Heuristic score: {confidence:.2f}",
                alternatives=alternatives,
                latency_ms=latency_ms,
            )
        
        # Layer 4: LLM Reasoning (for ambiguous cases)
        impl, confidence = self._route_via_llm(
            primitive_name, implementations, context, **kwargs
        )
        if impl and confidence >= 0.6:
            latency_ms = (time.time() - start_time) * 1000
            # Cache if confidence high enough
            if confidence >= 0.85:
                self._experience_cache.put(signature, impl.name, confidence)
            return RoutingDecision(
                implementation=impl,
                source=RoutingSource.LLM_REASONING,
                confidence=confidence,
                rationale="LLM semantic analysis selected best match",
                latency_ms=latency_ms,
            )
        
        # Layer 5: JIT Synthesis (dynamic generation when no suitable implementation exists)
        # Only attempt JIT synthesis if existing implementations have low confidence
        # or if context requires specialized implementation not available
        should_synthesize = (
            confidence < 0.6 or  # Low confidence in existing implementations
            context.quality_threshold > 0.85 or  # High quality requirements
            (context.domain and not any(  # Domain-specific need not met
                hasattr(i, 'domain') and i.domain == context.domain 
                for i in implementations
            ))
        )
        
        if should_synthesize:
            jit_impl = self._synthesize_implementation(
                primitive_name, implementations, context, **kwargs
            )
            if jit_impl:
                latency_ms = (time.time() - start_time) * 1000
                # Register the synthesized implementation for future use
                self.register_implementation(primitive_name, jit_impl)
                return RoutingDecision(
                    implementation=jit_impl,
                    source=RoutingSource.JIT_SYNTHESIS,
                    confidence=0.75,  # Moderate confidence in synthesized implementation
                    rationale=f"Synthesized new implementation for {primitive_name} tailored to context",
                    latency_ms=latency_ms,
                )
        
        # Fallback: Use default (first) implementation
        impl = implementations[0]
        latency_ms = (time.time() - start_time) * 1000
        return RoutingDecision(
            implementation=impl,
            source=RoutingSource.DEFAULT,
            confidence=0.5,
            rationale="Default implementation (no strong match)",
            latency_ms=latency_ms,
        )
    
    def _route_via_knowledge(
        self,
        primitive_name: str,
        implementations: List[Primitive],
        context: ExecutionContext,
        **kwargs
    ) -> Tuple[Optional[Primitive], float]:
        """
        Layer 2: Route using knowledge rules.
        
        Returns:
            (implementation, confidence) or (None, 0.0)
        """
        # Rule 1: Domain matching
        if context.domain:
            for impl in implementations:
                if hasattr(impl, 'domain') and impl.domain == context.domain:
                    return impl, 0.90
        
        # Rule 2: Quality threshold (think primitive)
        if primitive_name == "think":
            if context.quality_threshold > 0.8:
                # Prefer deep thinking
                deep_impl = next((i for i in implementations if 'deep' in i.name.lower()), None)
                if deep_impl:
                    return deep_impl, 0.88
            elif context.time_pressure > 0.7:
                # Prefer fast thinking
                fast_impl = next((i for i in implementations if 'fast' in i.name.lower()), None)
                if fast_impl:
                    return fast_impl, 0.87
        
        # Rule 3: Depth parameter
        depth = kwargs.get('depth', 0)
        if depth >= 5:
            deep_impls = [i for i in implementations if 'deep' in i.name.lower()]
            if deep_impls:
                return deep_impls[0], 0.85
        
        return None, 0.0
    
    def _route_via_heuristics(
        self,
        primitive_name: str,
        implementations: List[Primitive],
        context: ExecutionContext,
        **kwargs
    ) -> Tuple[Optional[Primitive], float, List[Tuple[Primitive, float]]]:
        """
        Layer 3: Route using multi-factor heuristics.
        
        Returns:
            (best_implementation, confidence, alternatives)
        """
        scores = []
        
        for impl in implementations:
            score = 0.0
            
            # Factor 1: Capability match (40%)
            capability_score = impl.matches_context(context, **kwargs)
            score += 0.4 * capability_score
            
            # Factor 2: Historical success (30%)
            stats = self._statistics.get(impl.name)
            if stats:
                score += 0.3 * stats.success_rate
                # Boost for domain expertise
                if context.domain and context.domain in stats.domain_scores:
                    score += 0.1 * stats.domain_scores[context.domain]
            else:
                score += 0.15  # Default for new implementations
            
            # Factor 3: Resource efficiency (20%)
            # Prefer implementations with lower latency/tokens
            if stats:
                # Normalize: lower is better
                if stats.avg_latency_ms < 500:
                    score += 0.2
                elif stats.avg_latency_ms < 1000:
                    score += 0.1
            else:
                score += 0.1  # Neutral for new implementations
            
            # Factor 4: Load balancing (10%)
            if stats:
                # Compute load factor: 1.0 (no load) to 0.0 (overloaded)
                load_factor = max(0.0, 1.0 - (stats.current_load / stats.max_concurrent))
                score += 0.1 * load_factor
            else:
                score += 0.1  # Default for new implementations
            
            scores.append((impl, score))
        
        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)
        
        if scores:
            best_impl, best_score = scores[0]
            alternatives = scores[1:4]  # Top 3 alternatives
            return best_impl, best_score, alternatives
        
        return None, 0.0, []
    
    def _synthesize_implementation(
        self,
        primitive_name: str,
        existing_implementations: List[Primitive],
        context: ExecutionContext,
        **kwargs
    ) -> Optional[Primitive]:
        """
        Layer 5: Synthesize a new implementation dynamically using LLM.
        
        This creates a specialized implementation tailored to the execution context
        when existing implementations are not suitable.
        
        Args:
            primitive_name: Name of primitive
            existing_implementations: Existing implementations (for reference)
            context: Execution context
            **kwargs: Additional parameters
            
        Returns:
            Synthesized Primitive implementation or None if synthesis fails
        """
        try:
            from brainary.llm.manager import get_llm_manager
            import textwrap
            
            # Get primitive definition from catalog
            prim_def = self._catalog.get(primitive_name)
            if not prim_def:
                return None
            
            # Build synthesis prompt
            context_desc = (
                f"Domain: {context.domain or 'general'}\n"
                f"Quality threshold: {context.quality_threshold}\n"
                f"Time pressure: {context.time_pressure}\n"
                f"Criticality: {context.criticality}\n"
                f"Execution mode: {context.execution_mode.value}"
            )
            
            existing_names = [impl.name for impl in existing_implementations]
            
            prompt = f"""You are an expert cognitive architecture designer synthesizing a specialized primitive implementation.

Primitive to implement: {primitive_name}
Description: {prim_def.description if prim_def else 'No description'}

Execution Context:
{context_desc}

Additional Parameters: {kwargs}

Existing implementations (not suitable for this context): {', '.join(existing_names)}

Design a specialized implementation that:
1. Is optimally suited for the given execution context
2. Leverages appropriate cognitive strategies
3. Balances quality and resource constraints
4. Has clear decision logic

Provide the implementation plan as JSON:
{{
  "implementation_name": "<descriptive name>",
  "strategy": "<high-level approach>",
  "reasoning_steps": ["<step 1>", "<step 2>", ...],
  "quality_indicators": ["<indicator 1>", "<indicator 2>", ...],
  "resource_profile": {{
    "estimated_tokens": <int>,
    "estimated_latency_ms": <int>,
    "complexity": <float 0-1>
  }},
  "hint": "<when to use this implementation>"
}}"""
            
            # Call LLM to generate implementation plan
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                messages=prompt,
                temperature=0.7,  # Higher temperature for creative synthesis
                max_tokens=800
            )
            
            # Parse response
            import json
            result_text = response.content.strip()
            
            # Extract JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            plan = json.loads(result_text)
            
            # Create dynamic implementation class
            impl = self._create_jit_implementation(
                primitive_name=primitive_name,
                plan=plan,
                context=context,
                **kwargs
            )
            
            return impl
            
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(
                f"JIT synthesis failed for {primitive_name}: {e}"
            )
            return None
    
    def _create_jit_implementation(
        self,
        primitive_name: str,
        plan: Dict[str, Any],
        context: ExecutionContext,
        **kwargs
    ) -> Primitive:
        """
        Create a JIT-synthesized primitive implementation.
        
        Args:
            primitive_name: Name of primitive
            plan: Implementation plan from LLM
            context: Execution context
            **kwargs: Additional parameters
            
        Returns:
            Primitive instance
        """
        from brainary.primitive.base import CorePrimitive, PrimitiveResult, CostMetrics, ConfidenceScore
        from brainary.llm.manager import get_llm_manager
        
        # Create dynamic class
        class JITSynthesizedPrimitive(CorePrimitive):
            """Dynamically synthesized primitive implementation."""
            
            def __init__(self, name: str, plan: Dict[str, Any], synthesis_context: ExecutionContext):
                super().__init__()
                self._name = name
                self._plan = plan
                self._synthesis_context = synthesis_context
                self._hint = plan.get('hint', 'Dynamically synthesized implementation')
                self.description = plan.get('strategy', 'JIT synthesized implementation')
                
                # Set capabilities based on plan
                resource_profile = plan.get('resource_profile', {})
                self._capabilities = {
                    'domain': synthesis_context.domain or 'general',
                    'complexity': resource_profile.get('complexity', 0.5),
                    'modes': [synthesis_context.execution_mode],
                }
            
            def validate_inputs(self, **validate_kwargs) -> None:
                """Validate inputs."""
                # Basic validation - can be enhanced
                pass
            
            def estimate_cost(self, **estimate_kwargs) -> CostMetrics:
                """Estimate resource requirements."""
                resource_profile = self._plan.get('resource_profile', {})
                return CostMetrics(
                    tokens=resource_profile.get('estimated_tokens', 1000),
                    latency_ms=resource_profile.get('estimated_latency_ms', 1000),
                    memory_slots=1,
                    provider_cost_usd=0.0,
                )
            
            def execute(
                self,
                context: ExecutionContext,
                memory: WorkingMemory,
                **exec_kwargs
            ) -> PrimitiveResult:
                """Execute the synthesized implementation."""
                import time
                start_time = time.time()
                
                try:
                    # Build execution prompt based on synthesis plan
                    strategy = self._plan.get('strategy', '')
                    reasoning_steps = self._plan.get('reasoning_steps', [])
                    
                    exec_prompt = f"""Execute the cognitive primitive: {primitive_name}

Strategy: {strategy}

Reasoning steps to follow:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(reasoning_steps))}

Context: {exec_kwargs}

Execute this primitive and return the result."""
                    
                    # Execute using LLM
                    llm_manager = get_llm_manager()
                    response = llm_manager.request(
                        messages=exec_prompt,
                        temperature=0.5,
                        max_tokens=2000
                    )
                    
                    # Calculate metrics
                    latency_ms = int((time.time() - start_time) * 1000)
                    
                    return PrimitiveResult(
                        content=response.content,
                        primitive_name=self._name,
                        success=True,
                        confidence=ConfidenceScore(
                            overall=0.75,
                            reasoning=0.75,
                            evidence=0.7
                        ),
                        execution_mode=context.execution_mode,
                        cost=CostMetrics(
                            tokens=response.usage.total_tokens,
                            latency_ms=latency_ms,
                            memory_slots=1,
                            provider_cost_usd=response.usage.cost_usd,
                        ),
                        metadata={
                            'jit_synthesized': True,
                            'synthesis_plan': self._plan,
                            'synthesis_context': self._synthesis_context.to_dict(),
                        }
                    )
                    
                except Exception as e:
                    latency_ms = int((time.time() - start_time) * 1000)
                    return PrimitiveResult(
                        content=None,
                        primitive_name=self._name,
                        success=False,
                        error=str(e),
                        confidence=ConfidenceScore(overall=0.0, reasoning=0.0, evidence=0.0),
                        execution_mode=context.execution_mode,
                        cost=CostMetrics(latency_ms=latency_ms),
                        metadata={'jit_synthesized': True, 'error': str(e)}
                    )
            
            def rollback(self, context: ExecutionContext) -> None:
                """Rollback - no-op for JIT implementations."""
                pass
        
        # Instantiate and return
        impl_name = plan.get('implementation_name', f'{primitive_name}_JIT_{int(time.time())}')
        return JITSynthesizedPrimitive(impl_name, plan, context)
    
    def _route_via_llm(
        self,
        primitive_name: str,
        implementations: List[Primitive],
        context: ExecutionContext,
        **kwargs
    ) -> Tuple[Optional[Primitive], float]:
        """
        Layer 4: Route using LLM reasoning with hints.
        
        Uses implementation hints for semantic analysis.
        
        Args:
            primitive_name: Name of primitive
            implementations: Available implementations
            context: Execution context
            **kwargs: Additional parameters
            
        Returns:
            (implementation, confidence) or (None, 0.0)
        """
        try:
            # Import LLM manager
            from brainary.llm.manager import get_llm_manager
            
            # Build context description
            context_desc = (
                f"Execution context:\n"
                f"- Domain: {context.domain or 'general'}\n"
                f"- Quality threshold: {context.quality_threshold}\n"
                f"- Time pressure: {context.time_pressure}\n"
                f"- Criticality: {context.criticality}\n"
                f"- Execution mode: {context.execution_mode.value}\n"
            )
            
            # Build implementation options with hints
            impl_options = []
            for idx, impl in enumerate(implementations):
                hint = impl.hint if hasattr(impl, 'hint') else "No specific guidance available"
                impl_options.append(
                    f"{idx}. {impl.name}\n"
                    f"   Guidance: {hint}\n"
                )
            
            # Build LLM prompt
            prompt = f"""You are an intelligent routing system for cognitive primitives.
Given the execution context and available implementations, select the best implementation.

Primitive to route: {primitive_name}

{context_desc}

Available implementations:
{''.join(impl_options)}

Additional parameters: {kwargs}

Analyze the context and implementation hints. Return your selection in this JSON format:
{{
  "selected_index": <integer index of best implementation>,
  "confidence": <float 0.0-1.0>,
  "rationale": "<brief explanation>"
}}

Select the implementation that best matches the execution requirements."""
            
            # Call LLM
            llm_manager = get_llm_manager()
            response = llm_manager.request(
                messages=prompt,
                temperature=0.3,  # Low temperature for consistent routing
                max_tokens=200
            )
            
            # Parse response
            import json
            result_text = response.content.strip()
            
            # Try to extract JSON from response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(result_text)
            
            selected_idx = result.get('selected_index', 0)
            confidence = result.get('confidence', 0.7)
            
            # Validate and return
            if 0 <= selected_idx < len(implementations):
                return implementations[selected_idx], confidence
            
        except Exception as e:
            # Fall back to heuristic-based selection on error
            import logging
            logging.getLogger(__name__).warning(
                f"LLM routing failed: {e}, falling back to heuristics"
            )
        
        # Fallback: Use simple heuristic-based selection
        for impl in implementations:
            hint = impl.hint if hasattr(impl, 'hint') else ""
            
            # Check time pressure hints
            if context.time_pressure > 0.7 and "time pressure" in hint.lower() and "high" in hint.lower():
                return impl, 0.75
            
            # Check quality hints
            if context.quality_threshold > 0.8 and "quality" in hint.lower() and "high" in hint.lower():
                return impl, 0.75
            
            # Check criticality hints
            if context.criticality > 0.7 and "critical" in hint.lower():
                return impl, 0.7
        
        # No strong match
        return None, 0.0
    
    def record_execution(
        self,
        impl_name: str,
        result: PrimitiveResult,
        context: ExecutionContext,
        signature: Optional[str] = None
    ) -> None:
        """
        Record execution outcome for learning.
        
        Args:
            impl_name: Implementation name
            result: Execution result
            context: Execution context
            signature: Optional context signature
        """
        with self._lock:
            if impl_name in self._statistics:
                stats = self._statistics[impl_name]
                stats.record_execution(
                    success=result.success,
                    latency_ms=result.cost.latency_ms,
                    tokens=result.cost.tokens,
                    confidence=result.confidence.overall,
                    domain=context.domain,
                )
        
        # Update experience cache confidence
        if signature:
            self._experience_cache.update_confidence(signature, result.success)
    
    def acquire_load(self, impl_name: str) -> bool:
        """
        Acquire load slot for an implementation.
        
        Args:
            impl_name: Implementation name
            
        Returns:
            True if load acquired, False if overloaded
        """
        with self._load_lock:
            if impl_name in self._statistics:
                stats = self._statistics[impl_name]
                if stats.current_load < stats.max_concurrent:
                    stats.current_load += 1
                    return True
                return False
            return True  # Allow if no stats yet
    
    def release_load(self, impl_name: str) -> None:
        """
        Release load slot for an implementation.
        
        Args:
            impl_name: Implementation name
        """
        with self._load_lock:
            if impl_name in self._statistics:
                stats = self._statistics[impl_name]
                stats.current_load = max(0, stats.current_load - 1)
    
    def get_statistics(self, impl_name: str) -> Optional[RoutingStatistics]:
        """
        Get statistics for an implementation.
        
        Args:
            impl_name: Implementation name
            
        Returns:
            RoutingStatistics if found, None otherwise
        """
        with self._lock:
            return self._statistics.get(impl_name)
    
    def list_all_implementations(self) -> Dict[str, List[str]]:
        """
        List all registered implementations.
        
        Returns:
            Dict mapping primitive names to implementation names
        """
        with self._lock:
            return {
                prim_name: [impl.name for impl in impls]
                for prim_name, impls in self._implementations.items()
            }


# Global router singleton
_global_router: Optional[PrimitiveRouter] = None
_router_lock = threading.Lock()


def get_primitive_router() -> PrimitiveRouter:
    """
    Get the global primitive router.
    
    Returns:
        Singleton PrimitiveRouter instance
    """
    global _global_router
    
    if _global_router is None:
        with _router_lock:
            if _global_router is None:
                _global_router = PrimitiveRouter()
    
    return _global_router


def register_implementation(
    primitive_name: str,
    implementation: Primitive,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Register an implementation for a primitive.
    
    This is the primary way to bind implementations to primitive names.
    
    Args:
        primitive_name: Name of primitive (e.g., "think", "perceive")
        implementation: Implementation instance (e.g., ThinkDeep(), PerceiveLLM())
        metadata: Optional metadata
        
    Example:
        >>> register_implementation("think", ThinkDeep())
        >>> register_implementation("think", ThinkFast())
        >>> register_implementation("think", CodeAnalysisThink(), metadata={'domain': 'code_analysis'})
    """
    router = get_primitive_router()
    router.register_implementation(primitive_name, implementation, metadata)


def route_primitive(
    primitive_name: str,
    context: ExecutionContext,
    **kwargs
) -> RoutingDecision:
    """
    Route a primitive name to optimal implementation.
    
    Args:
        primitive_name: Primitive name
        context: Execution context
        **kwargs: Additional parameters
        
    Returns:
        RoutingDecision with selected implementation
    """
    router = get_primitive_router()
    return router.route(primitive_name, context, **kwargs)

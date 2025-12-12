"""
Reflect: review(experience) + extract(lessons) + generalize(insights).
"""

from typing import Any, Dict, List, Optional, Tuple
import time
import logging

from brainary.primitive.base import (
    MetacognitivePrimitive,
    PrimitiveResult,
    ResourceEstimate,
    ConfidenceMetrics,
    CostMetrics,
)
from brainary.core.context import ExecutionContext
from brainary.memory.working import WorkingMemory
from brainary.llm.manager import get_llm_manager

logger = logging.getLogger(__name__)


class ReflectMetacognitive(MetacognitivePrimitive):
    """
    Reflect: review(experience) + extract(lessons) + generalize(insights).
    
    Reflects on experience to extract lessons and insights.
    """
    
    def __init__(self):
        """Initialize primitive."""
        super().__init__()
        self._name = "reflect"
        self._hint = (
            "Use for reflection on completed experiences to extract lessons. "
            "Best after task completion, at project milestones, or when consolidating "
            "learning. Analyzes what worked, what didn't, and extracts generalizable "
            "insights. Use for continuous improvement, knowledge extraction, and "
            "learning from experience. Most valuable with sufficient experience data "
            "and when long-term learning matters."
        )
    
    def execute(
        self,
        context: ExecutionContext,
        working_memory: WorkingMemory,
        experience: Dict[str, Any],
        focus: str = "general",
        **kwargs
    ) -> PrimitiveResult:
        """
        Reflect on experience using LLM for deep learning extraction.
        
        Args:
            context: Execution context
            working_memory: Working memory
            experience: Experience to reflect on (dict with task, outcome, etc.)
            focus: Reflection focus (general, technical, strategic, emotional)
            **kwargs: Additional parameters (depth)
        
        Returns:
            PrimitiveResult with reflection and lessons
        """
        start_time = time.time()
        
        try:
            # Retrieve reflection history
            memory_items = working_memory.retrieve(
                query=f"reflection learning {focus}",
                top_k=4
            )
            memory_context = "\n".join([f"- {item.content}" for item in memory_items])
            
            # Extract experience components
            task = experience.get('task', 'Unknown task')
            outcome = experience.get('outcome', 'Unknown outcome')
            success = experience.get('success', True)
            challenges = experience.get('challenges', [])
            decisions = experience.get('decisions', [])
            
            # Extract reflection depth
            depth = kwargs.get('depth', 'moderate')  # shallow, moderate, deep
            
            # Format experience
            experience_text = f"""
Task: {task}
Outcome: {outcome}
Success: {success}

Challenges Encountered:
{chr(10).join(f'- {c}' for c in challenges) if challenges else '- None reported'}

Key Decisions Made:
{chr(10).join(f'- {d}' for d in decisions) if decisions else '- None reported'}
"""
            
            # Build reflection prompt
            prompt = f"""Reflect deeply on the following experience to extract valuable lessons and insights.

EXPERIENCE:{experience_text}

REFLECTION FOCUS: {focus}
REFLECTION DEPTH: {depth}

PRIOR REFLECTIONS:
{memory_context if memory_context else "No prior reflections on similar experiences"}

Provide comprehensive reflection with:

1. WHAT HAPPENED: Objective summary of the experience
2. WHAT WORKED: Identify effective approaches, decisions, and strategies
3. WHAT DIDN'T WORK: Identify ineffective approaches or missed opportunities
4. WHY IT HAPPENED: Analyze root causes of both successes and failures
5. LESSONS LEARNED: Extract specific, actionable lessons from this experience
6. GENERALIZABLE INSIGHTS: Identify patterns and principles that apply beyond this specific case
7. FUTURE APPLICATIONS: How can these lessons be applied to future situations?
8. TRANSFERABILITY: Assess how transferable these lessons are to other domains

Be honest, insightful, and focus on extracting maximum learning value."""

            # Get LLM reflection
            llm_manager = get_llm_manager()
            
            # Use gpt-4o for deep reflection
            model = "gpt-4o" if depth == "deep" else "gpt-4o-mini"
            
            response = llm_manager.request(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
            )
            
            reflection_text = response.content
            
            # Parse sections
            sections = {}
            section_names = ["WHAT HAPPENED:", "WHAT WORKED:", "WHAT DIDN'T WORK:", 
                           "WHY IT HAPPENED:", "LESSONS LEARNED:", "GENERALIZABLE INSIGHTS:", 
                           "FUTURE APPLICATIONS:", "TRANSFERABILITY:"]
            for i, section_name in enumerate(section_names):
                start_idx = reflection_text.find(section_name)
                if start_idx == -1:
                    sections[section_name.rstrip(':')] = ""
                    continue
                
                end_idx = len(reflection_text)
                for next_section in section_names[i+1:]:
                    next_idx = reflection_text.find(next_section)
                    if next_idx != -1:
                        end_idx = next_idx
                        break
                
                sections[section_name.rstrip(':')] = reflection_text[start_idx+len(section_name):end_idx].strip()
            
            # Extract transferability score
            transfer_text = sections.get('TRANSFERABILITY', '').lower()
            if 'high' in transfer_text or 'very transferable' in transfer_text:
                transferability = 0.9
            elif 'moderate' in transfer_text or 'somewhat' in transfer_text:
                transferability = 0.7
            elif 'low' in transfer_text or 'limited' in transfer_text:
                transferability = 0.4
            else:
                transferability = 0.6
            
            reflection = {
                'experience': experience,
                'focus': focus,
                'depth': depth,
                'what_happened': sections.get('WHAT HAPPENED', ''),
                'what_worked': sections.get('WHAT WORKED', ''),
                'what_didnt_work': sections.get("WHAT DIDN'T WORK", ''),
                'why_it_happened': sections.get('WHY IT HAPPENED', ''),
                'lessons_learned': sections.get('LESSONS LEARNED', ''),
                'generalizable_insights': sections.get('GENERALIZABLE INSIGHTS', ''),
                'future_applications': sections.get('FUTURE APPLICATIONS', ''),
                'transferability': transferability,
                'success': success,
            }
            
            # Store reflection in memory
            working_memory.store(
                content=f"Reflection on '{task}': extracted lessons with {transferability:.1f} transferability",
                importance=0.75,
                tags=["metacognition", "reflection", focus, "learning"],
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return PrimitiveResult(
                content=reflection,
                confidence=ConfidenceMetrics(
                    overall=0.82,
                    reasoning=0.85,
                    completeness=0.82,
                    consistency=0.8,
                    evidence_strength=0.8,
                ),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=response.usage.total_tokens,
                    latency_ms=execution_time,
                    memory_slots=1,
                    provider_cost_usd=response.cost,
                ),
                primitive_name=self.name,
                success=True,
                metadata={
                    'focus': focus,
                    'depth': depth,
                    'transferability': transferability,
                    'model': model,
                }
            )
            
        except Exception as e:
            logger.error(f"Reflection failed: {e}")
            execution_time = int((time.time() - start_time) * 1000)
            return PrimitiveResult(
                content={'error': str(e)},
                confidence=ConfidenceMetrics(overall=0.0),
                execution_mode=context.execution_mode,
                cost=CostMetrics(
                    tokens=0,
                    latency_ms=execution_time,
                    memory_slots=0,
                    provider_cost_usd=0.0,
                ),
                primitive_name=self.name,
                success=False,
                metadata={'error': str(e)}
            )
    
    def estimate_cost(self, **kwargs) -> ResourceEstimate:
        """Estimate execution cost."""
        return ResourceEstimate(
            tokens=90,
            time_ms=35,
            memory_items=1,
            complexity=0.5,
        )
    
    def validate_inputs(self, **kwargs) -> None:
        """Validate inputs."""
        if "experience" not in kwargs:
            raise ValueError("'experience' parameter required")
    
    def matches_context(self, context: ExecutionContext, **kwargs) -> float:
        """Check context match."""
        return 0.75  # Generally useful for learning
    
    def rollback(self, context: ExecutionContext) -> None:
        """Rollback reflection."""
        pass


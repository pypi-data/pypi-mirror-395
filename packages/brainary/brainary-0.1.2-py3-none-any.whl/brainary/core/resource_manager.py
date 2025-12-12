"""
Resource manager for intelligent resource allocation.

Manages token budgets, time limits, and memory resources with
adaptive allocation and predictive optimization.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import threading
import time
import uuid

from brainary.primitive.base import ResourceEstimate, CostMetrics
from brainary.core.context import ExecutionContext


@dataclass
class ResourceQuota:
    """Resource allocation limits (matches SPECIFICATION.md)."""
    
    token_budget: int               # Maximum tokens allowed
    timeout_ms: float               # Maximum execution time
    memory_slots: int               # Working memory slots
    priority: float = 0.5           # [0-1] Scheduling priority


@dataclass
class ResourceAllocation:
    """Allocated resources for operation (matches SPECIFICATION.md)."""
    
    allocation_id: str
    quota: ResourceQuota
    allocated_at: float
    expires_at: float


class IResourceManager:
    """Interface for resource quota management (matches SPECIFICATION.md)."""
    
    def allocate(
        self,
        context: ExecutionContext,
        estimated_cost: CostMetrics
    ) -> ResourceAllocation:
        """Allocate resources for operation."""
        raise NotImplementedError
    
    def release(self, allocation_id: str) -> None:
        """Release allocated resources."""
        raise NotImplementedError
    
    def check_quota(
        self,
        context: ExecutionContext
    ) -> Dict[str, float]:
        """Check remaining quota."""
        raise NotImplementedError
    
    def update_usage(
        self,
        allocation_id: str,
        actual_cost: CostMetrics
    ) -> None:
        """Update resource usage statistics."""
        raise NotImplementedError


class ResourceManager(IResourceManager):
    """
    Intelligent resource manager (matches SPECIFICATION.md).
    
    Features:
    - Adaptive budget allocation based on criticality
    - Predictive timeout adjustment
    - Resource usage tracking
    - Dynamic reallocation
    """
    
    def __init__(self):
        """Initialize resource manager."""
        self._allocations: Dict[str, ResourceAllocation] = {}
        self._usage: Dict[str, CostMetrics] = {}
        self._lock = threading.RLock()
        
        # Statistics
        self.total_tokens_allocated = 0
        self.total_tokens_used = 0
        self.total_time_allocated_ms = 0.0
        self.total_time_used_ms = 0.0
    
    def allocate(
        self,
        context: ExecutionContext,
        estimated_cost: ResourceEstimate
    ) -> ResourceAllocation:
        """
        Allocate resources for operation (SPECIFICATION.md interface).
        
        Algorithm:
            1. Check available quota
            2. Apply priority scaling
            3. Reserve resources
            4. Set expiration timer
        
        Args:
            context: Execution context
            estimated_cost: Predicted resource usage (ResourceEstimate)
            
        Returns:
            ResourceAllocation: Allocated resources
            
        Raises:
            InsufficientResourcesError: If quota exceeded
        """
        with self._lock:
            # Base allocation from estimate
            token_alloc = estimated_cost.tokens
            time_alloc = estimated_cost.time_ms
            memory_alloc = estimated_cost.memory_items
            
            # Adjust based on context
            if context.criticality > 0.8:
                # Critical operations get 50% more resources
                token_alloc = int(token_alloc * 1.5)
                time_alloc = time_alloc * 1.5
            
            if context.quality_threshold > 0.9:
                # High quality needs more resources
                token_alloc = int(token_alloc * 1.3)
                time_alloc = time_alloc * 1.3
            
            # Ensure within context budget
            available_tokens = context.token_budget - context.token_usage
            if token_alloc > available_tokens:
                from brainary.core.errors import ResourceExhaustedError
                raise ResourceExhaustedError(
                    'tokens',
                    requested=token_alloc,
                    available=available_tokens,
                    context=context
                )
            
            token_alloc = min(token_alloc, available_tokens)
            
            if context.time_budget_ms:
                available_time = context.time_budget_ms - context.time_usage_ms
                time_alloc = min(time_alloc, available_time)
            
            # Create allocation
            allocation_id = str(uuid.uuid4())
            now = time.time()
            
            quota = ResourceQuota(
                token_budget=token_alloc,
                timeout_ms=time_alloc,
                memory_slots=memory_alloc,
                priority=context.criticality,
            )
            
            allocation = ResourceAllocation(
                allocation_id=allocation_id,
                quota=quota,
                allocated_at=now,
                expires_at=now + (time_alloc / 1000.0),  # Convert ms to seconds
            )
            
            self._allocations[allocation_id] = allocation
            self.total_tokens_allocated += token_alloc
            self.total_time_allocated_ms += time_alloc
            
            return allocation
    
    def release(self, allocation_id: str) -> None:
        """
        Release allocated resources (SPECIFICATION.md interface).
        
        Args:
            allocation_id: Allocation to release
        """
        with self._lock:
            if allocation_id in self._allocations:
                del self._allocations[allocation_id]
    
    def check_quota(
        self,
        context: ExecutionContext
    ) -> Dict[str, float]:
        """
        Check remaining quota (SPECIFICATION.md interface).
        
        Args:
            context: Execution context
            
        Returns:
            Dict with keys:
                - tokens_remaining: int
                - time_remaining_ms: float
                - memory_slots_remaining: int
        """
        return {
            'tokens_remaining': context.token_budget - context.token_usage,
            'time_remaining_ms': (
                (context.time_budget_ms - context.time_usage_ms)
                if context.time_budget_ms
                else float('inf')
            ),
            'memory_slots_remaining': context.memory_capacity,  # Simplified
        }
    
    def update_usage(
        self,
        allocation_id: str,
        actual_cost: CostMetrics
    ) -> None:
        """
        Update resource usage statistics (SPECIFICATION.md interface).
        
        Args:
            allocation_id: Allocation being updated
            actual_cost: Actual resources consumed
        """
        with self._lock:
            self._usage[allocation_id] = actual_cost
            self.total_tokens_used += actual_cost.tokens
            self.total_time_used_ms += actual_cost.latency_ms
    
    def record_usage(
        self,
        operation_id: str,
        tokens_used: int,
        time_used_ms: float,
        context: ExecutionContext
    ) -> None:
        """
        Record actual resource usage (backward compatibility method).
        
        Args:
            operation_id: Operation identifier
            tokens_used: Tokens consumed
            time_used_ms: Time consumed in milliseconds
            context: Execution context
        """
        cost = CostMetrics(
            tokens=tokens_used,
            latency_ms=time_used_ms,
            memory_slots=0,
            provider_cost_usd=0.0
        )
        self.update_usage(operation_id, cost)
        
        # Update context
        context.consume_tokens(tokens_used)
        context.consume_time(int(time_used_ms))
    
    def check_availability(
        self,
        estimate: ResourceEstimate,
        context: ExecutionContext
    ) -> bool:
        """
        Check if resources are available.
        
        Args:
            estimate: Resource estimate
            context: Execution context
        
        Returns:
            True if resources available
        """
        return context.has_capacity(
            tokens=estimate.tokens,
            milliseconds=estimate.time_ms
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get resource statistics.
        
        Returns:
            Dictionary of statistics
        """
        with self._lock:
            return {
                'tokens_allocated': self.total_tokens_allocated,
                'tokens_used': self.total_tokens_used,
                'token_efficiency': (
                    self.total_tokens_used / max(1, self.total_tokens_allocated)
                ),
                'time_allocated_ms': self.total_time_allocated_ms,
                'time_used_ms': self.total_time_used_ms,
                'time_efficiency': (
                    self.total_time_used_ms / max(1, self.total_time_allocated_ms)
                ),
                'operations': len(self._usage),
            }

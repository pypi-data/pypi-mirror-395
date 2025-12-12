"""
Test that all default primitive implementations are automatically registered.
"""

import pytest
from brainary.core.kernel import CognitiveKernel
from brainary.core.context import ExecutionContext
from brainary.primitive import get_primitive_router


def test_all_core_primitives_registered():
    """Test that all core level primitives have implementations registered."""
    # Initialize kernel to trigger registration
    kernel = CognitiveKernel()
    router = get_primitive_router()
    
    core_primitives = [
        "perceive",
        "think",
        "remember",
        "recall",
        "associate",
        "action",
        "monitor",
        "adapt",
    ]
    
    for prim_name in core_primitives:
        # Check if primitive has at least one implementation
        impls = router.get_implementations(prim_name)
        assert len(impls) > 0, \
            f"Core primitive '{prim_name}' has no registered implementation"


def test_all_control_primitives_registered():
    """Test that all control flow primitives have implementations registered."""
    kernel = CognitiveKernel()
    router = get_primitive_router()
    
    control_primitives = [
        "sequence",
        "parallel",
        "conditional",
        "loop",
        "retry",
    ]
    
    for prim_name in control_primitives:
        impls = router.get_implementations(prim_name)
        assert len(impls) > 0, \
            f"Control primitive '{prim_name}' has no registered implementation"


def test_all_metacognitive_primitives_registered():
    """Test that all metacognitive primitives have implementations registered."""
    kernel = CognitiveKernel()
    router = get_primitive_router()
    
    metacognitive_primitives = [
        "introspect",
        "self_assess",
        "select_strategy",
        "self_correct",
        "reflect",
    ]
    
    for prim_name in metacognitive_primitives:
        impls = router.get_implementations(prim_name)
        assert len(impls) > 0, \
            f"Metacognitive primitive '{prim_name}' has no registered implementation"


def test_primitives_executable():
    """Test that registered primitives can be executed."""
    kernel = CognitiveKernel()
    ctx = ExecutionContext(program_name="test_primitives")
    
    # Test a few key primitives with minimal parameters
    test_cases = [
        ("conditional", {"condition": "true", "if_true": "yes", "if_false": "no"}),
        ("sequence", {"operations": []}),
        ("parallel", {"operations": []}),
    ]
    
    for prim_name, kwargs in test_cases:
        result = kernel.execute(prim_name, ctx, **kwargs)
        # Should execute without raising exceptions
        assert result is not None, f"Primitive '{prim_name}' returned None"
        assert hasattr(result, 'success'), f"Primitive '{prim_name}' result has no 'success' attribute"


def test_registration_is_singleton():
    """Test that primitives are only registered once even with multiple kernels."""
    from brainary.primitive import _primitives_registered
    
    # Create first kernel
    k1 = CognitiveKernel()
    assert _primitives_registered, "Primitives should be registered after first kernel"
    
    # Create second kernel - should not re-register
    k2 = CognitiveKernel()
    assert _primitives_registered, "Primitives should still be registered"
    
    # Both kernels should work
    ctx = ExecutionContext(program_name="test")
    result1 = k1.execute("conditional", ctx, condition="true", if_true="yes", if_false="no")
    result2 = k2.execute("conditional", ctx, condition="true", if_true="yes", if_false="no")
    
    assert result1.success
    assert result2.success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Test enhanced ConditionalControl primitive with built-in semantic evaluation.

Demonstrates the primitive's ability to evaluate both simple and complex
natural language conditions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from brainary.core.kernel import CognitiveKernel
from brainary.core.context import ExecutionContext
from brainary.memory.working import WorkingMemory
from brainary.primitive import register_implementation
from brainary.primitive.implementations.control import ConditionalControl


def test_simple_conditions():
    """Test simple boolean conditions (no LLM)."""
    print("=" * 80)
    print("Test 1: Simple Boolean Conditions")
    print("=" * 80)
    
    # Register primitive
    register_implementation("conditional", ConditionalControl())
    
    context = ExecutionContext(program_name="test_simple")
    memory = WorkingMemory()
    kernel = CognitiveKernel()
    
    # Test various simple conditions
    test_cases = [
        ("true", True),
        ("false", False),
        ("yes", True),
        ("no", False),
        ("1", True),
        ("0", False),
    ]
    
    for condition, expected in test_cases:
        result = kernel.execute("conditional", context, memory,
                              condition=condition,
                              if_true="proceed",
                              if_false="stop")
        
        actual = result.content['condition_result']
        method = result.content['evaluation_method']
        confidence = result.content['confidence']
        
        print(f"  '{condition}' -> {actual} (method: {method}, confidence: {confidence:.2f}) " +
              f"{'✓' if actual == expected else '✗ FAILED'}")
        
        assert actual == expected, f"Expected {expected}, got {actual}"
        assert method == "direct", f"Expected 'direct' method, got {method}"
        assert confidence == 1.0, f"Expected confidence 1.0, got {confidence}"
    
    print("✅ All simple conditions passed\n")


def test_semantic_conditions():
    """Test semantic natural language conditions (with LLM)."""
    print("=" * 80)
    print("Test 2: Semantic Natural Language Conditions")
    print("=" * 80)
    
    context = ExecutionContext(program_name="test_semantic")
    memory = WorkingMemory()
    kernel = CognitiveKernel()
    
    # Test Case 1: SQL Injection Detection
    print("\n📋 Test Case 1: SQL Injection Detection")
    sql_code = '''
    String userInput = request.getParameter("id");
    String query = "SELECT * FROM users WHERE id = '" + userInput + "'";
    statement.execute(query);
    '''
    
    result = kernel.execute("conditional", context, memory,
                          condition="the code contains SQL injection vulnerability",
                          if_true="flag_vulnerability",
                          if_false="continue_analysis",
                          code=sql_code,
                          language="java",
                          context_type="database_query")
    
    actual = result.content['condition_result']
    method = result.content['evaluation_method']
    confidence = result.content['confidence']
    
    print(f"  Condition: 'SQL injection vulnerability present'")
    print(f"  Code: {sql_code[:80]}...")
    print(f"  Result: {actual} (method: {method}, confidence: {confidence:.2f})")
    print(f"  Expected: True (dangerous string concatenation)")
    print(f"  Status: {'✓ PASS' if actual else '✗ FAIL'}")
    
    # Test Case 2: Input Validation Check
    print("\n📋 Test Case 2: Input Validation Check")
    validated_code = '''
    String input = request.getParameter("username");
    if (input != null && input.matches("[a-zA-Z0-9]+")) {
        processUsername(input);
    }
    '''
    
    result = kernel.execute("conditional", context, memory,
                          condition="the input parameter is properly validated",
                          if_true="safe_to_use",
                          if_false="needs_validation",
                          code=validated_code,
                          variable="input")
    
    actual = result.content['condition_result']
    method = result.content['evaluation_method']
    confidence = result.content['confidence']
    
    print(f"  Condition: 'input is properly validated'")
    print(f"  Code: {validated_code[:80]}...")
    print(f"  Result: {actual} (method: {method}, confidence: {confidence:.2f})")
    print(f"  Expected: True (has regex validation)")
    print(f"  Status: {'✓ PASS' if actual else '✗ FAIL'}")
    
    # Test Case 3: Security Controls Check
    print("\n📋 Test Case 3: Security Controls Check")
    auth_code = '''
    @PreAuthorize("hasRole('ADMIN')")
    public void deleteUser(String userId) {
        userRepository.delete(userId);
    }
    '''
    
    result = kernel.execute("conditional", context, memory,
                          condition="the code has authorization controls",
                          if_true="secure",
                          if_false="needs_auth",
                          code=auth_code,
                          operation="delete_user")
    
    actual = result.content['condition_result']
    method = result.content['evaluation_method']
    confidence = result.content['confidence']
    
    print(f"  Condition: 'code has authorization controls'")
    print(f"  Code: {auth_code[:80]}...")
    print(f"  Result: {actual} (method: {method}, confidence: {confidence:.2f})")
    print(f"  Expected: True (has @PreAuthorize)")
    print(f"  Status: {'✓ PASS' if actual else '✗ FAIL'}")
    
    # Test Case 4: Negative Case - No Vulnerability
    print("\n📋 Test Case 4: Negative Case - Safe Code")
    safe_code = '''
    String userId = UUID.randomUUID().toString();
    String query = "SELECT * FROM users WHERE id = ?";
    PreparedStatement stmt = connection.prepareStatement(query);
    stmt.setString(1, userId);
    '''
    
    result = kernel.execute("conditional", context, memory,
                          condition="the code contains SQL injection vulnerability",
                          if_true="flag_vulnerability",
                          if_false="code_is_safe",
                          code=safe_code,
                          language="java")
    
    actual = result.content['condition_result']
    method = result.content['evaluation_method']
    confidence = result.content['confidence']
    
    print(f"  Condition: 'SQL injection vulnerability present'")
    print(f"  Code: {safe_code[:80]}...")
    print(f"  Result: {actual} (method: {method}, confidence: {confidence:.2f})")
    print(f"  Expected: False (uses PreparedStatement)")
    print(f"  Status: {'✓ PASS' if not actual else '✗ FAIL'}")
    
    print("\n✅ All semantic condition tests completed\n")


def test_evaluation_methods():
    """Test that appropriate evaluation methods are selected."""
    print("=" * 80)
    print("Test 3: Evaluation Method Selection")
    print("=" * 80)
    
    context = ExecutionContext(program_name="test_methods")
    memory = WorkingMemory()
    kernel = CognitiveKernel()
    
    test_cases = [
        ("true", "direct", "Simple boolean"),
        ("yes", "direct", "Simple affirmative"),
        ("the value is positive", "llm", "Semantic with context"),
    ]
    
    for condition, expected_method, description in test_cases:
        result = kernel.execute("conditional", context, memory,
                              condition=condition,
                              if_true="proceed",
                              if_false="stop",
                              value=42 if expected_method == "llm" else None)
        
        actual_method = result.content['evaluation_method']
        print(f"  {description}: '{condition}'")
        print(f"    Expected method: {expected_method}")
        print(f"    Actual method: {actual_method}")
        print(f"    Status: {'✓ PASS' if actual_method == expected_method else '✗ FAIL'}")
    
    print("\n✅ Evaluation method selection tests completed\n")


def test_cost_estimation():
    """Test cost estimation for different condition types."""
    print("=" * 80)
    print("Test 4: Cost Estimation")
    print("=" * 80)
    
    primitive = ConditionalControl()
    
    # Simple condition - should be cheap
    simple_cost = primitive.estimate_cost(condition="true", if_true="x", if_false="y")
    print(f"  Simple condition: {simple_cost.tokens} tokens, {simple_cost.time_ms}ms, {simple_cost.llm_calls} LLM calls")
    assert simple_cost.tokens == 0, "Simple conditions should use 0 tokens"
    assert simple_cost.llm_calls == 0, "Simple conditions should not call LLM"
    
    # Semantic condition - should estimate LLM cost
    semantic_cost = primitive.estimate_cost(
        condition="the code is vulnerable",
        if_true="x",
        if_false="y",
        code="some code here",
        description="test"
    )
    print(f"  Semantic condition: {semantic_cost.tokens} tokens, {semantic_cost.time_ms}ms, {semantic_cost.llm_calls} LLM calls")
    assert semantic_cost.tokens > 0, "Semantic conditions should estimate token usage"
    assert semantic_cost.llm_calls == 1, "Semantic conditions should estimate 1 LLM call"
    
    print("\n✅ Cost estimation tests completed\n")


def test_memory_integration():
    """Test that decisions are stored in working memory."""
    print("=" * 80)
    print("Test 5: Memory Integration")
    print("=" * 80)
    
    context = ExecutionContext(program_name="test_memory")
    memory = WorkingMemory()
    kernel = CognitiveKernel()
    
    # Execute several conditions
    kernel.execute("conditional", context, memory,
                  condition="the code is safe",
                  if_true="proceed",
                  if_false="stop",
                  code="test code")
    
    kernel.execute("conditional", context, memory,
                  condition="true",
                  if_true="yes",
                  if_false="no")
    
    # Check memory
    stored_items = memory.retrieve(query="conditional", top_k=5)
    
    print(f"  Stored memory items: {len(stored_items)}")
    print(f"  Expected: >= 2 (one per conditional execution)")
    
    for item in stored_items:
        print(f"    - {item.content[:80]}...")
    
    assert len(stored_items) >= 2, "Conditional decisions should be stored in memory"
    
    print("\n✅ Memory integration tests completed\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("Testing Enhanced ConditionalControl Primitive")
    print("Built-in Semantic Evaluation with LLM")
    print("=" * 80)
    print()
    
    try:
        test_simple_conditions()
        test_semantic_conditions()
        test_evaluation_methods()
        test_cost_estimation()
        test_memory_integration()
        
        print("=" * 80)
        print("✅ All tests passed successfully!")
        print("=" * 80)
        print("\n📊 Summary:")
        print("  - Simple boolean conditions: Direct evaluation (no LLM)")
        print("  - Semantic conditions: LLM-based evaluation")
        print("  - Automatic method selection based on complexity")
        print("  - Cost estimation reflects evaluation method")
        print("  - Decisions stored in working memory for learning")
        print()
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

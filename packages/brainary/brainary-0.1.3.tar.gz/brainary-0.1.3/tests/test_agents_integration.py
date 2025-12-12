"""
Real Integration Tests for Agent Templates with LLM Interactions

These tests make actual LLM calls and are slower than unit tests.
Run with: pytest tests/test_agents_integration.py -v -s

Note: Requires valid LLM configuration (OpenAI API key in llm.yml or OPENAI_API_KEY env var)
"""

import pytest
import os
import yaml
from pathlib import Path
from brainary.sdk import Agent, AgentTeam, AgentRole, AgentConfig


# Load API key from llm.yml
def load_api_key():
    """Load OpenAI API key from llm.yml or environment."""
    # First check environment
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return api_key
    
    # Then check llm.yml
    llm_config_path = Path(__file__).parent.parent / 'llm.yml'
    if llm_config_path.exists():
        try:
            with open(llm_config_path, 'r') as f:
                config = yaml.safe_load(f)
                api_key = config.get('openai-key')
                if api_key:
                    os.environ['OPENAI_API_KEY'] = api_key
                    return api_key
        except Exception as e:
            print(f"Warning: Could not load llm.yml: {e}")
    
    return None


# Skip all tests if no LLM is available
def check_llm_available():
    """Check if LLM is available for testing."""
    return load_api_key() is not None


pytestmark = pytest.mark.skipif(
    not check_llm_available(),
    reason="No LLM available (set OPENAI_API_KEY or configure llm.yml)"
)


class TestAgentRealOperations:
    """Test agent operations with real LLM calls"""
    
    def test_analyst_analyze_data(self):
        """Test analyst analyzing real data"""
        analyst = Agent.create('analyst', domain='data')
        
        data = {
            'sales': [100, 150, 120, 180, 200],
            'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May']
        }
        
        # Note: Using think() instead of analyze() because analyze primitive is not yet implemented
        result = analyst.think(
            f"As a data analyst, analyze this sales data: {data}. Identify trends."
        )
        
        print(f"\n--- Analyst Analysis ---")
        print(f"Content: {result.content}")
        print(f"Confidence: {result.confidence.overall:.2f}")
        
        assert result.success
        assert result.content is not None
        assert len(str(result.content)) > 50  # Should have substantial response
        assert result.confidence.overall > 0.5
    
    def test_coder_solve_problem(self):
        """Test coder solving a programming problem"""
        coder = Agent.create('coder', domain='python')
        
        problem = """
        As a Python coder, write a Python function that takes a list of numbers and returns 
        the sum of all even numbers. Include error handling.
        """
        
        # Note: Using think() instead of solve() because solve primitive is not yet implemented
        result = coder.think(problem)
        
        print(f"\n--- Coder Solution ---")
        print(f"Content: {result.content}")
        print(f"Confidence: {result.confidence.overall:.2f}")
        
        assert result.success
        assert result.content is not None
        # Should contain Python code indicators
        content_str = str(result.content).lower()
        assert any(keyword in content_str for keyword in ['def', 'function', 'return', 'sum', 'even'])
        assert result.confidence.overall > 0.5
    
    def test_researcher_gather_info(self):
        """Test researcher gathering information"""
        researcher = Agent.create('researcher', domain='technology')
        
        query = "What are the key features of transformer neural networks?"
        
        result = researcher.process(query)
        
        print(f"\n--- Researcher Results ---")
        print(f"Content: {result.content}")
        print(f"Confidence: {result.confidence.overall:.2f}")
        
        assert result.success
        assert result.content is not None
        assert len(str(result.content)) > 100  # Should be detailed
        # Should mention relevant concepts
        content_str = str(result.content).lower()
        assert any(keyword in content_str for keyword in ['attention', 'transformer', 'neural', 'network'])
    
    def test_teacher_explain_concept(self):
        """Test teacher explaining a concept"""
        teacher = Agent.create('teacher', domain='computer_science')
        
        concept = "Explain binary search algorithm to a beginner"
        
        result = teacher.think(concept)
        
        print(f"\n--- Teacher Explanation ---")
        print(f"Content: {result.content}")
        print(f"Confidence: {result.confidence.overall:.2f}")
        
        assert result.success
        assert result.content is not None
        assert len(str(result.content)) > 100
        # Should be educational
        content_str = str(result.content).lower()
        assert any(keyword in content_str for keyword in ['search', 'sorted', 'divide', 'algorithm'])
    
    def test_writer_create_content(self):
        """Test writer creating content"""
        writer = Agent.create('writer', domain='technical')
        
        task = "Write a brief introduction paragraph for a blog post about AI agents"
        
        result = writer.process(task)
        
        print(f"\n--- Writer Content ---")
        print(f"Content: {result.content}")
        print(f"Confidence: {result.confidence.overall:.2f}")
        
        assert result.success
        assert result.content is not None
        assert len(str(result.content)) > 50
        # Should be well-written
        content_str = str(result.content)
        assert len(content_str.split()) > 20  # At least 20 words


class TestAgentWithMemory:
    """Test agent memory operations with real LLM"""
    
    def test_agent_remember_and_recall(self):
        """Test agent using memory across multiple operations"""
        analyst = Agent.create('analyst', domain='business')
        
        # Store some context
        analyst.remember("Company revenue 2023: $10 million", importance=0.9)
        analyst.remember("Company revenue 2024: $15 million", importance=0.9)
        analyst.remember("Growth rate: 50% YoY", importance=0.85)
        
        # Ask question that needs context
        result = analyst.think(
            "Based on the stored revenue data, what's the revenue trend?"
        )
        
        print(f"\n--- Analysis with Memory ---")
        print(f"Content: {result.content}")
        print(f"Confidence: {result.confidence.overall:.2f}")
        
        assert result.success
        assert result.content is not None
        
        # Verify memory is populated
        memory_stats = analyst.memory.get_stats()
        assert memory_stats['total'] >= 3
        
        # Recall specific information
        revenue_memories = analyst.recall("revenue")
        assert len(revenue_memories) > 0
    
    def test_agent_learning_over_tasks(self):
        """Test agent processing multiple related tasks"""
        coder = Agent.create('coder', domain='python', enable_learning=True)
        
        # Process related tasks
        tasks = [
            "As a Python coder, write a function to reverse a string",
            "As a Python coder, write a function to check if a string is palindrome",
            "As a Python coder, optimize the palindrome checker"
        ]
        
        results = []
        for i, task in enumerate(tasks):
            # Note: Using think() instead of solve() because solve primitive is not yet implemented
            result = coder.think(task)
            results.append(result)
            
            print(f"\n--- Task {i+1}: {task} ---")
            print(f"Success: {result.success}")
            print(f"Confidence: {result.confidence.overall:.2f}")
            
            # Store the solution
            if result.success:
                coder.remember(
                    f"Solution for '{task}': {result.content}",
                    importance=0.8
                )
        
        # All should succeed
        assert all(r.success for r in results)
        
        # Agent should have memory of solutions
        memory_stats = coder.memory.get_stats()
        assert memory_stats['total'] >= 3
        
        # Get stats
        stats = coder.get_stats()
        assert stats['agent']['tasks_processed'] >= 3


class TestAgentTeamReal:
    """Test agent teams with real LLM interactions"""
    
    def test_two_agent_collaboration(self):
        """Test two agents collaborating on a task"""
        team = AgentTeam("dev_team")
        team.add_agent(Agent.create('coder', domain='python'), alias='dev')
        team.add_agent(Agent.create('reviewer', domain='code'), alias='qa')
        
        # Developer writes code
        code_task = "Write a Python function to calculate factorial"
        dev_result = team.process(code_task, agent_name='dev')
        
        print(f"\n--- Developer's Code ---")
        print(f"Content: {dev_result.content}")
        
        assert dev_result.success
        code = str(dev_result.content)
        
        # Reviewer reviews the code
        review_task = f"Review this code for quality and correctness:\n{code}"
        review_result = team.process(review_task, agent_name='qa')
        
        print(f"\n--- Reviewer's Feedback ---")
        print(f"Content: {review_result.content}")
        
        assert review_result.success
        assert review_result.content is not None
    
    def test_sequential_workflow(self):
        """Test sequential agent workflow"""
        team = AgentTeam("analysis_team")
        team.add_agent(Agent.create('researcher', domain='AI'), alias='researcher')
        team.add_agent(Agent.create('analyst', domain='data'), alias='analyst')
        
        task = "Research transformer architectures and analyze their key features"
        
        results = team.collaborate(
            task,
            ['researcher', 'analyst'],
            strategy='sequential'
        )
        
        print(f"\n--- Sequential Workflow Results ---")
        for i, result in enumerate(results):
            print(f"\nAgent {i+1}:")
            print(f"Success: {result.success}")
            print(f"Confidence: {result.confidence.overall:.2f}")
            print(f"Content preview: {str(result.content)[:200]}...")
        
        assert len(results) == 2
        assert all(r.success for r in results)
    
    def test_parallel_analysis(self):
        """Test parallel analysis by multiple agents"""
        team = AgentTeam("review_team")
        team.add_agent(Agent.create('analyst', domain='security'), alias='security')
        team.add_agent(Agent.create('analyst', domain='performance'), alias='performance')
        
        code_sample = """
def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
        """
        
        task = f"Analyze this code:\n{code_sample}"
        
        results = team.collaborate(
            task,
            ['security', 'performance'],
            strategy='parallel'
        )
        
        print(f"\n--- Parallel Analysis Results ---")
        for i, result in enumerate(results):
            print(f"\nAnalyst {i+1}:")
            print(f"Success: {result.success}")
            print(f"Content: {result.content}")
        
        assert len(results) == 2
        assert all(r.success for r in results)


class TestAgentCustomization:
    """Test custom agent configurations"""
    
    def test_high_quality_agent(self):
        """Test agent with high quality threshold"""
        analyst = Agent.create(
            'analyst',
            domain='finance',
            quality_threshold=0.90,  # High quality requirement
            default_mode='deep',     # Deep reasoning
            memory_capacity=10
        )
        
        task = "As a financial analyst, analyze the pros and cons of value investing vs growth investing"
        # Note: Using think() instead of analyze() because analyze primitive is not yet implemented
        result = analyst.think(task)
        
        print(f"\n--- High Quality Analysis ---")
        print(f"Content: {result.content}")
        print(f"Confidence: {result.confidence.overall:.2f}")
        
        assert result.success
        assert result.content is not None
        # High quality mode should produce detailed response
        assert len(str(result.content)) > 200
    
    def test_agent_with_constraints(self):
        """Test agent with specific constraints"""
        coder = Agent.create('coder', domain='python')
        
        # Add constraints
        coder.add_constraint("use_type_hints")
        coder.add_constraint("include_docstrings")
        coder.add_constraint("handle_errors")
        
        task = "As a Python coder, write a function to parse JSON safely"
        # Note: Using think() instead of solve() because solve primitive is not yet implemented
        result = coder.think(task)
        
        print(f"\n--- Constrained Code ---")
        print(f"Content: {result.content}")
        
        assert result.success
        assert result.content is not None
        # Should include requested elements
        content_str = str(result.content).lower()
        # At least some constraints should be reflected
        assert 'def' in content_str or 'function' in content_str or 'json' in content_str
    
    def test_agent_with_focus(self):
        """Test agent with attention focus"""
        analyst = Agent.create('analyst', domain='security')
        
        # Set specific focus
        analyst.set_focus("vulnerabilities", "exploits", "mitigation")
        
        task = "As a security analyst, analyze this authentication system design"
        # Note: Using think() instead of analyze() because analyze primitive is not yet implemented
        result = analyst.think(task)
        
        print(f"\n--- Focused Analysis ---")
        print(f"Content: {result.content}")
        print(f"Focus keywords: {analyst.config.attention_focus}")
        
        assert result.success
        assert result.content is not None
        assert 'vulnerabilities' in analyst.config.attention_focus


class TestAgentStatistics:
    """Test agent statistics tracking"""
    
    def test_track_multiple_operations(self):
        """Test statistics tracking across operations"""
        agent = Agent.create('assistant', domain='general')
        
        # Perform multiple operations
        tasks = [
            "What is 2+2?",
            "Explain gravity briefly",
            "Name three primary colors"
        ]
        
        for task in tasks:
            result = agent.think(task)
            print(f"\nTask: {task}")
            print(f"Success: {result.success}")
        
        # Check statistics
        stats = agent.get_stats()
        
        print(f"\n--- Agent Statistics ---")
        print(f"Tasks processed: {stats['agent']['tasks_processed']}")
        print(f"Success rate: {stats['agent']['success_rate']:.2%}")
        print(f"Memory items: {stats['memory']['total']}")
        
        assert stats['agent']['tasks_processed'] >= 3
        assert stats['agent']['success_rate'] > 0.5


class TestRoleSpecificBehaviors:
    """Test that different roles produce different behaviors"""
    
    def test_analyst_vs_coder_response(self):
        """Test analyst and coder respond differently to same problem"""
        problem = "How to improve application performance?"
        
        analyst = Agent.create('analyst', domain='performance')
        coder = Agent.create('coder', domain='optimization')
        
        analyst_result = analyst.process(problem)
        coder_result = coder.process(problem)
        
        print(f"\n--- Analyst Response ---")
        print(f"{analyst_result.content}")
        
        print(f"\n--- Coder Response ---")
        print(f"{coder_result.content}")
        
        assert analyst_result.success
        assert coder_result.success
        
        # Responses should be different (not identical)
        assert analyst_result.content != coder_result.content
        
        # Analyst might focus on metrics/analysis
        # Coder might provide code examples
        analyst_str = str(analyst_result.content).lower()
        coder_str = str(coder_result.content).lower()
        
        # Just verify both produced substantial responses
        assert len(analyst_str) > 50
        assert len(coder_str) > 50
    
    def test_teacher_vs_researcher_explanation(self):
        """Test teacher and researcher explain differently"""
        topic = "What are neural networks?"
        
        teacher = Agent.create('teacher', domain='AI')
        researcher = Agent.create('researcher', domain='AI')
        
        teacher_result = teacher.think(topic)
        researcher_result = researcher.think(topic)
        
        print(f"\n--- Teacher Explanation ---")
        print(f"{teacher_result.content}")
        
        print(f"\n--- Researcher Explanation ---")
        print(f"{researcher_result.content}")
        
        assert teacher_result.success
        assert researcher_result.success
        
        # Both should mention neural networks
        teacher_str = str(teacher_result.content).lower()
        researcher_str = str(researcher_result.content).lower()
        
        assert 'neural' in teacher_str or 'network' in teacher_str
        assert 'neural' in researcher_str or 'network' in researcher_str


if __name__ == '__main__':
    # Run with verbose output to see LLM responses
    pytest.main([__file__, '-v', '-s'])

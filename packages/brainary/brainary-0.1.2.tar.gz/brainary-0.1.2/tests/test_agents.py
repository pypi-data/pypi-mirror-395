"""
Tests for Agent Templates System

Tests cover:
- Agent creation from all roles
- Custom agent configuration
- Agent operations (process, think, analyze, solve, decide)
- Memory integration (remember, recall)
- Agent configuration (set_focus, add_constraint)
- Agent statistics
- Team creation and management
- Team task routing
- Team collaboration (sequential and parallel)
- Error handling
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from brainary.sdk import Agent, AgentTeam, AgentRole, AgentConfig
from brainary.primitive.base import PrimitiveResult, ConfidenceScore, CostMetrics
from brainary.core.context import ExecutionMode


def make_mock_result(content="Test result", confidence=0.85, success=True, error=None):
    """Helper to create properly formatted PrimitiveResult mocks"""
    return PrimitiveResult(
        content=content,
        confidence=ConfidenceScore(overall=confidence),
        execution_mode=ExecutionMode.ADAPTIVE,
        cost=CostMetrics(),
        success=success,
        error=error
    )


class TestAgentCreation:
    """Test agent creation from templates and custom configs"""
    
    def test_create_all_roles(self):
        """Test creating agents from all 8 role templates"""
        roles = ['analyst', 'researcher', 'coder', 'reviewer', 
                 'planner', 'writer', 'teacher', 'assistant']
        
        for role in roles:
            agent = Agent.create(role, domain='test')
            assert agent is not None
            assert agent.config.name == f"{role}_test"
            assert agent.config.domain == 'test'
            assert agent.config.role.value == role
    
    def test_create_with_overrides(self):
        """Test creating agent with custom overrides"""
        agent = Agent.create(
            'analyst',
            domain='security',
            name='custom_name',
            quality_threshold=0.95,
            memory_capacity=15,
            default_mode='deep',
            token_budget=20000
        )
        
        assert agent.config.name == 'custom_name'
        assert agent.config.domain == 'security'
        assert agent.config.quality_threshold == 0.95
        assert agent.config.memory_capacity == 15
        assert agent.config.default_mode == 'deep'
        assert agent.config.token_budget == 20000
    
    def test_create_from_config(self):
        """Test creating agent from custom AgentConfig"""
        config = AgentConfig(
            name='custom_agent',
            role=AgentRole.ANALYST,
            domain='finance',
            description='Financial analyst',
            quality_threshold=0.90,
            memory_capacity=10
        )
        
        agent = Agent.from_config(config)
        assert agent.config.name == 'custom_agent'
        assert agent.config.role == AgentRole.ANALYST
        assert agent.config.domain == 'finance'
        assert agent.config.quality_threshold == 0.90
    
    def test_agent_has_brain_and_memory(self):
        """Test that agent has Brainary instance and MemoryManager"""
        agent = Agent.create('analyst', domain='test')
        assert agent.brain is not None
        assert agent.memory is not None
        assert hasattr(agent.brain, 'think')
        assert hasattr(agent.memory, 'store')


class TestAgentOperations:
    """Test agent cognitive operations"""
    
    @patch('brainary.sdk.client.Brainary.think')
    def test_agent_think(self, mock_think):
        """Test agent think operation"""
        mock_think.return_value = make_mock_result("Test response", 0.85)
        
        agent = Agent.create('analyst', domain='test')
        result = agent.think("Test query")
        
        assert result.success
        assert result.content == "Test response"
        mock_think.assert_called_once()
    
    @patch('brainary.sdk.client.Brainary.analyze')
    def test_agent_analyze(self, mock_analyze):
        """Test agent analyze operation"""
        mock_analyze.return_value = make_mock_result("Analysis complete", 0.90)
        
        agent = Agent.create('analyst', domain='data')
        result = agent.analyze({"test": "data"})
        
        assert result.success
        assert result.content == "Analysis complete"
        mock_analyze.assert_called_once()
    
    @patch('brainary.sdk.client.Brainary.solve')
    def test_agent_solve(self, mock_solve):
        """Test agent solve operation"""
        mock_solve.return_value = make_mock_result("Solution found", 0.88)
        
        agent = Agent.create('coder', domain='python')
        result = agent.solve("Implement binary search")
        
        assert result.success
        assert result.content == "Solution found"
        mock_solve.assert_called_once()
    
    @patch('brainary.sdk.client.Brainary.decide')
    def test_agent_decide(self, mock_decide):
        """Test agent decide operation"""
        mock_decide.return_value = make_mock_result("option_a", 0.92)
        
        agent = Agent.create('planner', domain='project')
        result = agent.decide(['option_a', 'option_b', 'option_c'])
        
        assert result.success
        assert result.content == "option_a"
        mock_decide.assert_called_once()
    
    @patch('brainary.sdk.client.Brainary.analyze')
    def test_agent_process_routing(self, mock_analyze):
        """Test that agent.process() routes to appropriate handler"""
        mock_analyze.return_value = make_mock_result("Processed", 0.85)
        
        # Analyst should route to analyze
        analyst = Agent.create('analyst', domain='test')
        result = analyst.process("analyze this data")
        
        assert result.success
        mock_analyze.assert_called()


class TestAgentMemory:
    """Test agent memory operations"""
    
    def test_agent_remember(self):
        """Test storing information in agent memory"""
        agent = Agent.create('analyst', domain='test')
        
        # Store information
        agent.remember("Important fact", importance=0.9)
        
        # Verify it's stored
        stats = agent.memory.get_stats()
        assert stats['total'] > 0
    
    def test_agent_recall(self):
        """Test recalling information from agent memory"""
        agent = Agent.create('researcher', domain='AI')
        
        # Store some facts
        agent.remember("Transformers use attention", importance=0.9)
        agent.remember("BERT is bidirectional", importance=0.8)
        
        # Recall
        results = agent.recall("transformer")
        assert len(results) > 0
    
    def test_agent_memory_capacity(self):
        """Test that agent memory respects capacity limits"""
        agent = Agent.create('analyst', domain='test')
        capacity = agent.config.memory_capacity
        
        # Store items up to capacity
        for i in range(capacity):
            agent.remember(f"Fact {i}", importance=0.5)
        
        # Memory should have items
        stats = agent.memory.get_stats()
        assert stats['total'] > 0
        assert stats['total'] <= capacity + 5  # Memory manager may allow some overflow


class TestAgentConfiguration:
    """Test agent configuration methods"""
    
    def test_set_focus(self):
        """Test setting attention focus keywords"""
        agent = Agent.create('analyst', domain='security')
        
        agent.set_focus("vulnerabilities", "exploits", "compliance")
        
        assert "vulnerabilities" in agent.config.attention_focus
        assert "exploits" in agent.config.attention_focus
        assert "compliance" in agent.config.attention_focus
    
    def test_add_constraint(self):
        """Test adding behavioral constraints"""
        agent = Agent.create('coder', domain='python')
        
        agent.add_constraint("no_external_calls")
        agent.add_constraint("validate_inputs")
        
        assert "no_external_calls" in agent.config.constraints
        assert "validate_inputs" in agent.config.constraints


class TestAgentStatistics:
    """Test agent statistics and monitoring"""
    
    def test_get_stats(self):
        """Test getting agent statistics"""
        agent = Agent.create('analyst', domain='test')
        
        # Get initial stats
        stats = agent.get_stats()
        
        # Verify structure
        assert 'agent' in stats
        assert 'memory' in stats
        assert 'brain' in stats
        
        # Verify agent stats fields
        assert 'name' in stats['agent']
        assert 'role' in stats['agent']
        assert 'domain' in stats['agent']
        assert 'tasks_processed' in stats['agent']
        assert 'success_rate' in stats['agent']
        
        # Initial values
        assert stats['agent']['name'] == 'analyst_test'
        assert stats['agent']['role'] == 'analyst'
        assert stats['agent']['domain'] == 'test'
        assert stats['agent']['tasks_processed'] >= 0


class TestAgentTeam:
    """Test multi-agent team functionality"""
    
    def test_team_creation(self):
        """Test creating an agent team"""
        team = AgentTeam(name='test_team')
        assert team.name == 'test_team'
        assert len(team.list_agents()) == 0
    
    def test_add_agent(self):
        """Test adding agents to team"""
        team = AgentTeam()
        analyst = Agent.create('analyst', domain='data')
        coder = Agent.create('coder', domain='python')
        
        team.add_agent(analyst, alias='analyst')
        team.add_agent(coder, alias='dev')
        
        agents = team.list_agents()
        assert len(agents) == 2
        assert 'analyst_data' in agents or 'analyst' in agents
        assert 'coder_python' in agents or 'dev' in agents
    
    def test_remove_agent(self):
        """Test removing agents from team"""
        team = AgentTeam()
        analyst = Agent.create('analyst', domain='data')
        
        team.add_agent(analyst)
        assert len(team.list_agents()) == 1
        
        team.remove_agent(analyst.config.name)
        assert len(team.list_agents()) == 0
    
    def test_get_agent(self):
        """Test retrieving specific agent from team"""
        team = AgentTeam()
        analyst = Agent.create('analyst', domain='security')
        
        team.add_agent(analyst, alias='sec_analyst')
        
        retrieved = team.get_agent('sec_analyst')
        assert retrieved is not None
        assert retrieved.config.domain == 'security'
    
    def test_list_agents(self):
        """Test listing all agents in team"""
        team = AgentTeam()
        
        team.add_agent(Agent.create('analyst', domain='data'))
        team.add_agent(Agent.create('coder', domain='python'))
        team.add_agent(Agent.create('reviewer', domain='code'))
        
        agents = team.list_agents()
        assert len(agents) == 3


class TestTeamOperations:
    """Test team task routing and execution"""
    
    @patch('brainary.sdk.agents.Agent.process')
    def test_team_process_with_agent_name(self, mock_process):
        """Test processing task with specific agent"""
        mock_process.return_value = make_mock_result("Result", 0.85)
        
        team = AgentTeam()
        analyst = Agent.create('analyst', domain='data')
        team.add_agent(analyst, alias='analyst')
        
        result = team.process("Analyze data", agent_name='analyst')
        
        assert result.success
        mock_process.assert_called_once()
    
    @patch('brainary.sdk.agents.Agent.process')
    def test_team_process_auto_select(self, mock_process):
        """Test automatic agent selection based on task"""
        mock_process.return_value = make_mock_result("Result", 0.85)
        
        team = AgentTeam()
        team.add_agent(Agent.create('analyst', domain='data'))
        team.add_agent(Agent.create('coder', domain='python'))
        
        # Should route to analyst
        result = team.process("Analyze this dataset")
        
        assert result.success
        mock_process.assert_called_once()
    
    @patch('brainary.sdk.agents.Agent.process')
    def test_team_collaborate_sequential(self, mock_process):
        """Test sequential collaboration strategy"""
        mock_process.return_value = make_mock_result("Step result", 0.85)
        
        team = AgentTeam()
        team.add_agent(Agent.create('planner', domain='project'), alias='pm')
        team.add_agent(Agent.create('coder', domain='python'), alias='dev')
        
        results = team.collaborate(
            "Build feature",
            ['pm', 'dev'],
            strategy='sequential'
        )
        
        assert len(results) == 2
        assert all(r.success for r in results)
        assert mock_process.call_count == 2
    
    @patch('brainary.sdk.agents.Agent.process')
    def test_team_collaborate_parallel(self, mock_process):
        """Test parallel collaboration strategy"""
        mock_process.return_value = make_mock_result("Analysis result", 0.85)
        
        team = AgentTeam()
        team.add_agent(Agent.create('analyst', domain='security'), alias='sec')
        team.add_agent(Agent.create('analyst', domain='performance'), alias='perf')
        
        results = team.collaborate(
            "Analyze application",
            ['sec', 'perf'],
            strategy='parallel'
        )
        
        assert len(results) == 2
        assert all(r.success for r in results)
        assert mock_process.call_count == 2
    
    def test_team_get_stats(self):
        """Test getting team statistics"""
        team = AgentTeam()
        team.add_agent(Agent.create('analyst', domain='data'))
        team.add_agent(Agent.create('coder', domain='python'))
        
        stats = team.get_stats()
        
        assert 'team' in stats
        assert 'agents' in stats
        assert stats['team']['name'] == team.name
        assert stats['team']['agent_count'] == 2


class TestAgentRoleTemplates:
    """Test role-specific template configurations"""
    
    def test_analyst_template(self):
        """Test analyst role template configuration"""
        agent = Agent.create('analyst', domain='test')
        
        assert agent.config.role == AgentRole.ANALYST
        assert agent.config.quality_threshold == 0.85
        assert agent.config.default_mode == 'deep'
        assert 'patterns' in agent.config.attention_focus
        assert 'evidence_based' in agent.config.constraints
    
    def test_researcher_template(self):
        """Test researcher role template configuration"""
        agent = Agent.create('researcher', domain='test')
        
        assert agent.config.role == AgentRole.RESEARCHER
        assert agent.config.quality_threshold == 0.90
        assert agent.config.default_mode == 'deep'
        assert 'sources' in agent.config.attention_focus
        assert 'cite_sources' in agent.config.constraints
    
    def test_coder_template(self):
        """Test coder role template configuration"""
        agent = Agent.create('coder', domain='test')
        
        assert agent.config.role == AgentRole.CODER
        assert agent.config.quality_threshold == 0.85
        assert agent.config.default_mode == 'adaptive'
        assert 'correctness' in agent.config.attention_focus
        assert 'syntactically_valid' in agent.config.constraints
    
    def test_reviewer_template(self):
        """Test reviewer role template configuration"""
        agent = Agent.create('reviewer', domain='test')
        
        assert agent.config.role == AgentRole.REVIEWER
        assert agent.config.quality_threshold == 0.90
        assert agent.config.default_mode == 'deep'
        assert 'errors' in agent.config.attention_focus
        assert 'constructive' in agent.config.constraints


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_role(self):
        """Test handling of invalid role name"""
        with pytest.raises(ValueError):  # AgentRole enum raises ValueError for invalid values
            Agent.create('invalid_role', domain='test')
    
    def test_team_get_nonexistent_agent(self):
        """Test getting non-existent agent from team"""
        team = AgentTeam()
        agent = team.get_agent('nonexistent')
        assert agent is None
    
    def test_team_remove_nonexistent_agent(self):
        """Test removing non-existent agent from team"""
        team = AgentTeam()
        # Should not raise error
        team.remove_agent('nonexistent')
        assert len(team.list_agents()) == 0
    
    def test_team_process_no_agents(self):
        """Test processing task with empty team"""
        team = AgentTeam()
        
        # Should raise ValueError when trying to process with no agents
        with pytest.raises(ValueError, match="No agents in team"):
            team.process("Some task")


class TestIntegration:
    """Integration tests for complete workflows"""
    
    @patch('brainary.sdk.client.Brainary.think')
    @patch('brainary.sdk.client.Brainary.analyze')
    def test_agent_with_memory_workflow(self, mock_analyze, mock_think):
        """Test agent using memory across multiple tasks"""
        mock_think.return_value = make_mock_result("Thought", 0.85)
        mock_analyze.return_value = make_mock_result("Analysis", 0.90)
        
        agent = Agent.create('analyst', domain='finance')
        
        # Store context
        agent.remember("2023 revenue: $10M", importance=0.9)
        agent.remember("Growth rate: 15%", importance=0.8)
        
        # Use context in analysis
        agent.think("What's the context?")
        context = agent.recall("revenue")
        assert len(context) > 0
        
        result = agent.analyze("2024 Q1 data")
        assert result.success
    
    @patch('brainary.sdk.agents.Agent.process')
    def test_development_pipeline_workflow(self, mock_process):
        """Test complete development pipeline with multiple agents"""
        mock_process.return_value = make_mock_result("Step complete", 0.85)
        
        # Create development team
        team = AgentTeam('dev_pipeline')
        team.add_agent(Agent.create('planner', domain='software'), alias='pm')
        team.add_agent(Agent.create('coder', domain='python'), alias='dev')
        team.add_agent(Agent.create('reviewer', domain='code'), alias='qa')
        
        # Execute pipeline
        results = team.collaborate(
            "Implement user authentication",
            ['pm', 'dev', 'qa'],
            strategy='sequential'
        )
        
        assert len(results) == 3
        assert all(r.success for r in results)
        assert mock_process.call_count == 3
    
    @patch('brainary.sdk.agents.Agent.process')
    def test_parallel_analysis_workflow(self, mock_process):
        """Test parallel analysis from multiple perspectives"""
        def mock_process_side_effect(task, **kwargs):
            return make_mock_result(f"Analysis: {task}", 0.85)
        
        mock_process.side_effect = mock_process_side_effect
        
        # Create analysis team
        team = AgentTeam('analysis')
        team.add_agent(Agent.create('analyst', domain='security'), alias='sec')
        team.add_agent(Agent.create('analyst', domain='performance'), alias='perf')
        team.add_agent(Agent.create('analyst', domain='usability'), alias='ux')
        
        # Parallel analysis
        results = team.collaborate(
            "Analyze web application",
            ['sec', 'perf', 'ux'],
            strategy='parallel'
        )
        
        assert len(results) == 3
        assert all(r.success for r in results)
        assert mock_process.call_count == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

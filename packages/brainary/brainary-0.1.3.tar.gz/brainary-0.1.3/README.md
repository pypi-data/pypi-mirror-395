# Brainary

**Programmable Intelligence System**

Brainary is a cognitive computing platform where intelligence is expressed as executable programs built from cognitive primitives (perceive, think, remember, act). It provides a framework for building intelligent systems grounded in cognitive science principles.

## Overview

Traditional AI systems are monolithic black boxes. Brainary makes intelligence **programmable**, **composable**, and **transparent** by:

1. **Cognitive Primitives**: Core operations (perceive, think, remember) that compose into complex behavior
2. **Intelligent Execution**: Adaptive routing that learns optimal implementations from experience
3. **Memory Architecture**: Working memory (7±2 capacity), attention mechanisms, and associative learning
4. **Meta-Cognition**: Self-monitoring and adaptive control for quality and resource management

## Quick Start

### 1. Brainary Client (recommended)

```python
from brainary.sdk import Brainary

brain = Brainary(quality_threshold=0.85, memory_capacity=7)
result = brain.think("How can I optimize database queries?")
print(result.content)
print(f"Confidence: {result.confidence.overall:.2f}")
```

### 2. Function-Based API

```python
from brainary.sdk import configure, think, analyze

configure(memory_capacity=9, quality_threshold=0.9)
think("When should I shard Postgres?")
analysis = analyze(code_block, analysis_type="security")
```

### 3. Template Agents

```python
from brainary.sdk.template_agent import TemplateAgent
from brainary.primitive.base import PrimitiveResult

class ResearchAgent(TemplateAgent):
    def process(self, input_data, context, **kwargs) -> PrimitiveResult:
        outline = self.kernel.execute("plan", context=context, goal=input_data)
        return self.kernel.execute("synthesize", context=context, components=[outline.content])

agent = ResearchAgent(name="analyst", domain="strategy")
report = agent.run("Summarize LLM tooling")
print(report.content)
```

### 4. Kernel Access (advanced)

```python
from brainery import get_kernel, create_execution_context, WorkingMemory

kernel = get_kernel()
context = create_execution_context(program_name="my_app", quality_threshold=0.8)
memory = WorkingMemory(capacity=7)
result = kernel.execute("think", context=context, working_memory=memory, query="How can I optimize database queries?")
```

## Key Features

### 🎯 User-Friendly SDK
- **Three API Styles**: Client-based, function-based, and agent templates
- **Agent Templates**: 8 pre-configured roles (analyst, coder, researcher, etc.)
- **Memory Management**: Intuitive memory storage and retrieval
- **Context Management**: Fluent builder and context managers
- **Multi-Agent Teams**: Coordinate multiple agents for complex workflows
- **Learning Integration**: Built-in learning insights and statistics
- **Full Type Safety**: Complete type hints for IDE support

### 🧠 Cognitive Architecture
- **5-Level Primitive Hierarchy**: Core → Composite → Metacognitive → Domain → Control
- **Working Memory**: 7±2 capacity with activation-based management
- **Attention Mechanism**: Keyword-driven focus and relevance computation
- **Associative Memory**: Graph-based semantic relationships
- **Learning System**: Continuous improvement from execution traces

### ⚡ Intelligent Execution
- **Three-Source Routing**: Experience cache → Knowledge rules → Heuristic scoring → LLM semantic
- **Adaptive Executors**: Direct LLM, ReAct Agent, LangGraph orchestration
- **Resource Management**: Token budgets, time limits, dynamic allocation
- **Learning System**: Automatic improvement from execution feedback

### 🔧 Composability
- **Control Flow**: Sequence, Parallel, Conditional, Retry primitives
- **Payload Augmentation**: Pre/post execution enhancements
- **Context Propagation**: Child contexts inherit parent configuration
- **Memory Snapshots**: Rollback support for experimentation

### 📊 Observability
- **Execution Traces**: Full visibility into decision-making
- **Performance Metrics**: Token usage, time, success rates
- **Confidence Scores**: Multi-dimensional quality assessment
- **Resource Tracking**: Budget consumption and allocation
- **Memory Debugging**: Real-time inspection of memory operations (store, retrieve, evict, consolidate, promote)

## Installation

Brainary is currently distributed from source.

```bash
git clone https://github.com/cs-wangchong/Brainary brainary
cd brainary
python -m venv .venv
source .venv/bin/activate
pip install -e .

# configure LLM credentials
export OPENAI_API_KEY="sk-..."
```

## Documentation

- **[Quickstart](docs/QUICKSTART.md)** – fastest way to experiment with the SDK.
- **[SDK Guide](docs/SDK_GUIDE.md)** – architecture tour + recommended patterns.
- **[API Reference](docs/API_REFERENCE.md)** – constructors, primitives, agents.
- **[User Manual](docs/USER_MANUAL.md)** – end-to-end workflows and troubleshooting.
- **[Memory Debugging](docs/MEMORY_DEBUGGING.md)** – inspecting working/semantic memory.

## Examples

See `examples/` directory for comprehensive demonstrations:

- **agent_templates_demo.py**: 8 examples of specialized agents and teams
- **sdk_demo.py**: 8 examples showing SDK usage patterns
- **test_sdk.py**: SDK validation and testing
- **simple_kernel_demo.py**: Kernel with learning system
- **intelligent_assistant.py**: Complete walkthrough of core features
- **tpl/java_security_detector/**: Full multi-agent security scanning template for Java projects. From the repo root run `python tpl/java_security_detector/examples/comprehensive_demo.py` to see the end-to-end pipeline (scanner → analyzer → validator → reporter), or explore `tpl/java_security_detector/README.md` for CLI/API usage.
- More examples coming soon...

## Architecture

### Cognitive Primitives

```python
from brainery import PerceiveLLM, ThinkDeep, RememberWorkingMemory

# Core primitives
perceive = PerceiveLLM()      # LLM interaction
think = ThinkDeep()            # Analytical reasoning  
remember = RememberWorkingMemory()  # Memory storage
```

### Execution Pipeline

```
User Request
    ↓
Cognitive Kernel
    ↓
Program Scheduler (Intelligent Routing)
    ├─→ Experience Cache (fast)
    ├─→ Knowledge Rules (learned)
    ├─→ Heuristic Scoring (contextual)
    └─→ LLM Semantic (fallback)
    ↓
Payload Assembly (augmentation planning)
    ↓
Executor Selection
    ├─→ DirectLLM (simple, complexity ≤ 0.4)
    ├─→ ReAct Agent (moderate, 0.4-0.7)
    └─→ LangGraph (complex, > 0.7)
    ↓
Primitive Execution
    ↓
Learning Update (cache + rules)
    ↓
Result + Statistics
```

### Memory System

```python
from brainery import WorkingMemory, AttentionMechanism, AssociativeMemory

# Working memory with cognitive constraints
memory = WorkingMemory(capacity=7)

# Attention-driven retrieval
attention = AttentionMechanism(memory)
attention.set_focus(keywords=["important", "urgent"])

# Semantic associations
associations = AssociativeMemory(memory)
associations.associate(item1, item2, strength=0.8)
```

## Additional References

- **[DESIGN.md](doc/DESIGN.md)** – architecture philosophy.
- **[IMPLEMENTATION.md](doc/IMPLEMENTATION.md)** – subsystem deep dives.
- **[examples/README.md](examples/README.md)** – per-example notes.

## Contributing

Contributions welcome! Please open an issue or pull request; a CONTRIBUTING guide is coming soon.
# moss-crewai

MOSS signing integration for CrewAI agents.

## Installation

```bash
pip install moss-crewai
```

## Usage

```python
from crewai import Agent
from moss_crewai import moss_wrap

# Create your CrewAI agent
agent = Agent(
    role="Researcher",
    goal="Find information",
    backstory="You are a research assistant"
)

# Wrap with MOSS signing
agent = moss_wrap(agent, "moss:team:researcher")

# After agent executes, signature is available
result = agent.execute_task(task)
envelope = agent.moss_envelope  # MOSS Envelope with signature
```

## Verification

```python
from moss import Subject

# Verify the agent's output
result = Subject.verify(agent.moss_envelope)
assert result.valid
```

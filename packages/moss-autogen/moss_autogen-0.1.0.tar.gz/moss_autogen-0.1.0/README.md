# moss-autogen

MOSS signing integration for AutoGen agents.

## Installation

```bash
pip install moss-autogen
```

## Usage

```python
from autogen import AssistantAgent
from moss_autogen import signed_agent

# Create your AutoGen agent
agent = AssistantAgent(
    name="analyst",
    llm_config={"model": "gpt-4"}
)

# Wrap with MOSS signing
agent = signed_agent(agent, "moss:lab:analyst")

# After agent replies, signature is available
reply = agent.generate_reply(messages=[{"content": "Analyze this data"}])
envelope = agent.moss_envelope  # MOSS Envelope with signature
```

## Verification

```python
from moss import Subject

# Verify the agent's output
result = Subject.verify(agent.moss_envelope)
assert result.valid
```

## Multi-Agent Scenarios

```python
from autogen import AssistantAgent, UserProxyAgent
from moss_autogen import signed_agent

assistant = signed_agent(
    AssistantAgent(name="assistant", ...),
    "moss:team:assistant"
)

analyst = signed_agent(
    AssistantAgent(name="analyst", ...),
    "moss:team:analyst"
)

# Each agent's replies are independently signed
# Check assistant.moss_envelope or analyst.moss_envelope after interactions
```

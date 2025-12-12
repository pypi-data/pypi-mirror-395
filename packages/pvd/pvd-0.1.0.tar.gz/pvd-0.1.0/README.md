# Paved SDK

PVD SDK for Paved platform (the Firewall for AI Agents). All policy checks and telemetry route through the Paved Platform API (default: https://app.hipaved.com).

## Install

```bash
pip install pvd
```

After installing, you can log in to the platform (assuming you have created an account in https://app.hipaved.com):

```bash
pvd login
```

## CLI Usage

```bash
# Init a starter agent project
pvd init my-agent --template llm

# Build a tarball to deploy
cd my-agent
pvd build . -o my-agent.tar.gz

# Deploy to the platform
pvd deploy my-agent.tar.gz --name my-agent

# List and invoke
pvd list
pvd invoke <agent-id> --payload '{"message": "hello"}'
pvd logs <invocation-id> --follow
```

## SDK Usage

```python
from pvd.sdk import Agent, PolicyDeniedError

agent = Agent(
    agent_id="my-remote-agent",
    policies=["pii_strict"],
)

try:
    text = agent.llm("Summarize our Q3 performance.")
finally:
    agent.complete(result={"ok": True})
```
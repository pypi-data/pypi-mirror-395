# Quickstart

This guide will help you get started with vendor-connectors.

## Installation

```bash
pip install vendor-connectors
```

## Basic Usage

### Using the VendorConnectors Class (Recommended)

```python
from vendor_connectors import VendorConnectors

# Initialize - reads credentials from environment variables
vc = VendorConnectors()

# Get cached clients for any connector
cursor = vc.get_cursor_client()       # Cursor AI agents
anthropic = vc.get_anthropic_client() # Claude AI
github = vc.get_github_client(github_owner="myorg")
slack = vc.get_slack_client()
```

### Using Individual Connectors

#### Anthropic (Claude AI)

```python
from vendor_connectors import AnthropicConnector

# Initialize (or set ANTHROPIC_API_KEY env var)
claude = AnthropicConnector(api_key="...")

# Create a message
response = claude.create_message(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.text)
```

**Source of truth for models:** https://docs.anthropic.com/en/docs/about-claude/models

#### Cursor (Background Agents)

```python
from vendor_connectors import CursorConnector

# Initialize (or set CURSOR_API_KEY env var)
cursor = CursorConnector(api_key="...")

# Launch an AI coding agent
agent = cursor.launch_agent(
    prompt_text="Implement user authentication",
    repository="myorg/myrepo"
)
print(f"Agent launched: {agent.id}")

# Check status
status = cursor.get_agent_status(agent.id)
print(f"State: {status.state}")
```

**API Reference:** https://docs.cursor.com/account/api

#### AWS

```python
from vendor_connectors import AWSConnector

aws = AWSConnector(execution_role_arn="arn:aws:iam::123456789012:role/MyRole")
s3 = aws.get_aws_client("s3")
```

#### GitHub

```python
from vendor_connectors import GithubConnector

github = GithubConnector(
    github_owner="myorg",
    github_repo="myrepo",
    github_token=os.getenv("GITHUB_TOKEN")
)
repos = github.list_repositories()
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic Claude API key |
| `CURSOR_API_KEY` | Cursor Background Agent API key |
| `AWS_*` | Standard AWS credentials |
| `GITHUB_TOKEN` | GitHub personal access token |
| `VAULT_ADDR` / `VAULT_TOKEN` | HashiCorp Vault |
| `SLACK_TOKEN` / `SLACK_BOT_TOKEN` | Slack API |

## Next Steps

- Check out the [API Reference](../api/index.rst) for detailed documentation
- See [Contributing](../development/contributing.md) to help improve this project

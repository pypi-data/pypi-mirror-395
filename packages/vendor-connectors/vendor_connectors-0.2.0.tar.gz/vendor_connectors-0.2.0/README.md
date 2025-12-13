# Vendor Connectors

Universal vendor connectors for the jbcom ecosystem, providing standardized access to cloud providers, third-party services, and AI APIs.

## Features

### AI/Agent Connectors (NEW)
- **Anthropic Connector**: Claude AI API wrapper with message generation, token counting, and model management
- **Cursor Connector**: Cursor Background Agent API for AI coding agent management

### Cloud Providers
- **AWS Connector**: Boto3-based client with role assumption and retry logic
- **Google Cloud Connector**: Workspace and Cloud Platform APIs with lazy credential loading

### Services
- **GitHub Connector**: Repository management, GraphQL queries, and file operations
- **Slack Connector**: Bot and app integrations with rate limiting
- **Vault Connector**: HashiCorp Vault with Token and AppRole auth
- **Zoom Connector**: Meeting and user management
- **Meshy Connector**: Meshy AI 3D asset generation (text-to-3D, rigging, animation, retexture)

### Unified Interface
- **VendorConnectors**: Cached public API with `get_*_client()` getters for all connectors

## Installation

```bash
pip install vendor-connectors
```

### Optional Extras

```bash
# For Meshy webhooks
pip install vendor-connectors[webhooks]

# For CrewAI agent integration
pip install vendor-connectors[crewai]

# For MCP server integration  
pip install vendor-connectors[mcp]

# For Meshy vector store/RAG
pip install vendor-connectors[vector]

# Everything
pip install vendor-connectors[all]
```

## Usage

### Using VendorConnectors (Recommended)

The `VendorConnectors` class provides cached access to all connectors:

```python
from vendor_connectors import VendorConnectors

# Initialize once - reads credentials from environment
vc = VendorConnectors()

# AI/Agent connectors
cursor = vc.get_cursor_client()       # Cursor Background Agent API
anthropic = vc.get_anthropic_client() # Claude AI

# Cloud providers
s3 = vc.get_aws_client("s3")
google = vc.get_google_client()

# Services
github = vc.get_github_client(github_owner="myorg")
slack = vc.get_slack_client()
vault = vc.get_vault_client()
zoom = vc.get_zoom_client()
```

### Using Individual Connectors

```python
from vendor_connectors import AWSConnector, GithubConnector, SlackConnector

# AWS with role assumption
aws = AWSConnector(execution_role_arn="arn:aws:iam::123456789012:role/MyRole")
s3 = aws.get_aws_client("s3")

# GitHub operations
github = GithubConnector(
    github_owner="myorg",
    github_repo="myrepo",
    github_token=os.getenv("GITHUB_TOKEN")
)

# Slack messaging
slack = SlackConnector(
    token=os.getenv("SLACK_TOKEN"),
    bot_token=os.getenv("SLACK_BOT_TOKEN")
)
slack.send_message("general", "Hello from vendor-connectors!")
```

### Anthropic Claude AI

```python
from vendor_connectors import AnthropicConnector

# Initialize with API key (or set ANTHROPIC_API_KEY env var)
claude = AnthropicConnector(api_key="...")

# Create a message
response = claude.create_message(
    model="claude-sonnet-4-5-20250929",  # Claude Sonnet 4.5
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain quantum computing in simple terms"}]
)
print(response.text)

# Count tokens before sending
tokens = claude.count_tokens(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Get recommended model for use case
model = claude.get_recommended_model("coding")  # Returns claude-sonnet-4-5-20250929
```

**Source of truth for models:** https://docs.anthropic.com/en/docs/about-claude/models

### Cursor Background Agents

```python
from vendor_connectors import CursorConnector

# Initialize with API key (or set CURSOR_API_KEY env var)
cursor = CursorConnector(api_key="...")

# List all agents
agents = cursor.list_agents()
for agent in agents:
    print(f"{agent.id}: {agent.state}")

# Launch a new agent
agent = cursor.launch_agent(
    prompt_text="Implement user authentication with OAuth2",
    repository="myorg/myrepo",
    ref="main",
    auto_create_pr=True
)
print(f"Launched agent: {agent.id}")

# Get agent status
status = cursor.get_agent_status(agent.id)
print(f"State: {status.state}")

# Send follow-up
cursor.add_followup(agent.id, "Also add rate limiting")

# List available repositories
repos = cursor.list_repositories()
```

**API Reference:** https://docs.cursor.com/account/api

### Meshy AI (3D Asset Generation)

```python
from vendor_connectors import meshy

# Generate a 3D model
model = meshy.text3d.generate("a medieval sword with ornate handle")
print(model.model_urls.glb)

# Rig it for animation
rigged = meshy.rigging.rig(model.id)

# Apply an animation (678 available)
animated = meshy.animate.apply(rigged.id, animation_id=0)  # Idle

# Or retexture it
gold = meshy.retexture.apply(model.id, "golden with embedded gems")
```

## Architecture

All connectors extend `DirectedInputsClass` from the jbcom ecosystem:

- **directed-inputs-class**: Input handling from environment, stdin, config
- **lifecyclelogging**: Structured logging with verbosity control
- **extended-data-types**: Utilities like `is_nothing`, `strtobool`, `wrap_raw_data_for_export`

The `VendorConnectors` class provides:
- Client caching (same parameters = same instance)
- Automatic credential loading from environment
- Consistent interface across all providers

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic Claude API key |
| `CURSOR_API_KEY` | Cursor Background Agent API key |
| `AWS_*` | Standard AWS credentials |
| `EXECUTION_ROLE_ARN` | AWS role to assume |
| `GITHUB_TOKEN` | GitHub personal access token |
| `GITHUB_OWNER` | GitHub organization/user |
| `GOOGLE_SERVICE_ACCOUNT` | Google service account JSON |
| `SLACK_TOKEN` | Slack user token |
| `SLACK_BOT_TOKEN` | Slack bot token |
| `VAULT_ADDR` | Vault server URL |
| `VAULT_TOKEN` | Vault authentication token |
| `VAULT_ROLE_ID` / `VAULT_SECRET_ID` | AppRole credentials |
| `ZOOM_CLIENT_ID` / `ZOOM_CLIENT_SECRET` / `ZOOM_ACCOUNT_ID` | Zoom OAuth |
| `MESHY_API_KEY` | Meshy AI API key |

## Part of jbcom Ecosystem

This package is part of the jbcom Python library ecosystem:
- [extended-data-types](https://pypi.org/project/extended-data-types/) - Foundation utilities
- [lifecyclelogging](https://pypi.org/project/lifecyclelogging/) - Structured logging
- [directed-inputs-class](https://pypi.org/project/directed-inputs-class/) - Input handling

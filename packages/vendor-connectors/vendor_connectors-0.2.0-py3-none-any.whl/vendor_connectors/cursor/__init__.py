"""Cursor Connector - HTTP client for Cursor Background Agent API.

This connector provides Python access to the Cursor Background Agent API for
managing AI coding agents, following the patterns established in the jbcom ecosystem.

Usage:
    from vendor_connectors.cursor import CursorConnector

    connector = CursorConnector(api_key="...")
    agents = connector.list_agents()

    agent = connector.launch_agent(
        prompt_text="Implement feature X",
        repository="org/repo",
        ref="main"
    )

Reference: https://cursor.com/docs/cloud-agent/api/endpoints
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional
from urllib.parse import urlparse

import httpx
from directed_inputs_class import DirectedInputsClass
from lifecyclelogging import Logging
from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    pass

__all__ = [
    "CursorConnector",
    "Agent",
    "AgentState",
    "Repository",
    "Conversation",
    "ConversationMessage",
    "LaunchOptions",
    "CursorError",
]


# =============================================================================
# Constants
# =============================================================================

DEFAULT_BASE_URL = "https://api.cursor.com/v0"
DEFAULT_TIMEOUT = 60.0  # seconds
MAX_PROMPT_LENGTH = 100000
MAX_REPO_LENGTH = 200

# Validation patterns
AGENT_ID_PATTERN = re.compile(r"^[a-zA-Z0-9-]+$")

# Blocked patterns for SSRF protection
# Note: urlparse returns hostname WITHOUT brackets for IPv6, so patterns match raw IPv6
BLOCKED_HOSTNAME_PATTERNS = [
    # IPv4 localhost and private ranges
    re.compile(r"^localhost$", re.IGNORECASE),
    re.compile(r"^127\."),
    re.compile(r"^10\."),
    re.compile(r"^172\.(1[6-9]|2[0-9]|3[0-1])\."),
    re.compile(r"^192\.168\."),
    re.compile(r"^169\.254\."),
    re.compile(r"^0\."),
    # IPv6 addresses (urlparse strips brackets, so match raw addresses)
    re.compile(r"^::1$"),  # IPv6 localhost
    re.compile(r"^fc", re.IGNORECASE),  # IPv6 unique local (fc00::/7)
    re.compile(r"^fd", re.IGNORECASE),  # IPv6 unique local (fd00::/8)
    re.compile(r"^fe80:", re.IGNORECASE),  # IPv6 link-local
    re.compile(r"^::ffff:", re.IGNORECASE),  # IPv4-mapped IPv6
    # DNS-based blocks
    re.compile(r"^metadata\.", re.IGNORECASE),
    re.compile(r"^internal\.", re.IGNORECASE),
    re.compile(r"\.local$", re.IGNORECASE),
    re.compile(r"\.internal$", re.IGNORECASE),
]


# =============================================================================
# Exceptions
# =============================================================================


class CursorError(Exception):
    """Base exception for Cursor API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class CursorValidationError(CursorError):
    """Validation error for Cursor API inputs."""


class CursorAPIError(CursorError):
    """API error from Cursor service."""


# =============================================================================
# Models
# =============================================================================


class AgentState(str, Enum):
    """Agent execution state."""

    PENDING = "pending"
    RUNNING = "running"
    FINISHED = "finished"
    ERRORED = "errored"
    CANCELLED = "cancelled"


class Agent(BaseModel):
    """Cursor Background Agent representation."""

    model_config = ConfigDict(extra="allow")  # Allow additional fields from API

    id: str = Field(description="Unique agent identifier")
    state: AgentState = Field(description="Current agent state")
    task: Optional[str] = Field(default=None, description="Task description")
    repository: Optional[str] = Field(default=None, description="Repository name")
    branch: Optional[str] = Field(default=None, description="Branch name")
    pr_number: Optional[int] = Field(default=None, description="Associated PR number")
    pr_url: Optional[str] = Field(default=None, description="PR URL")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
    model: Optional[str] = Field(default=None, description="Model used")
    error: Optional[str] = Field(default=None, description="Error message if errored")


class Repository(BaseModel):
    """Repository available for Cursor agents."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(description="Repository full name (owner/repo)")
    url: Optional[str] = Field(default=None, description="Repository URL")
    default_branch: Optional[str] = Field(default=None, description="Default branch")
    private: Optional[bool] = Field(default=None, description="Is private repository")


class ConversationMessage(BaseModel):
    """Single message in agent conversation."""

    model_config = ConfigDict(extra="allow")

    role: str = Field(description="Message role (user/assistant/system)")
    content: str = Field(description="Message content")
    timestamp: Optional[datetime] = Field(default=None, description="Message timestamp")


class Conversation(BaseModel):
    """Agent conversation history."""

    model_config = ConfigDict(extra="allow")

    agent_id: str = Field(description="Agent identifier")
    messages: list[ConversationMessage] = Field(default_factory=list, description="Conversation messages")


@dataclass
class LaunchOptions:
    """Options for launching a new agent."""

    prompt_text: str
    repository: str
    ref: Optional[str] = None
    images: Optional[list[dict[str, Any]]] = None
    auto_create_pr: bool = True
    branch_name: Optional[str] = None
    open_as_cursor_github_app: bool = True
    skip_reviewer_request: bool = False
    webhook_url: Optional[str] = None
    webhook_secret: Optional[str] = None


# =============================================================================
# Validators
# =============================================================================


def validate_agent_id(agent_id: str) -> None:
    """Validate an agent ID to prevent injection attacks.

    Args:
        agent_id: The agent ID to validate.

    Raises:
        CursorValidationError: If the agent ID is invalid.
    """
    if not agent_id or not isinstance(agent_id, str):
        raise CursorValidationError("Agent ID is required and must be a string")
    if len(agent_id) > 100:
        raise CursorValidationError("Agent ID exceeds maximum length (100 characters)")
    if not AGENT_ID_PATTERN.match(agent_id):
        raise CursorValidationError("Agent ID contains invalid characters (only alphanumeric and hyphens allowed)")


def validate_prompt_text(text: str) -> None:
    """Validate prompt text.

    Args:
        text: The prompt text to validate.

    Raises:
        CursorValidationError: If the prompt is invalid.
    """
    if not text or not isinstance(text, str):
        raise CursorValidationError("Prompt text is required and must be a string")
    if not text.strip():
        raise CursorValidationError("Prompt text cannot be empty")
    if len(text) > MAX_PROMPT_LENGTH:
        raise CursorValidationError(f"Prompt text exceeds maximum length ({MAX_PROMPT_LENGTH} characters)")


def validate_repository(repository: str) -> None:
    """Validate repository name.

    Args:
        repository: The repository name to validate.

    Raises:
        CursorValidationError: If the repository is invalid.
    """
    if not repository or not isinstance(repository, str):
        raise CursorValidationError("Repository is required and must be a string")
    if len(repository) > MAX_REPO_LENGTH:
        raise CursorValidationError(f"Repository name exceeds maximum length ({MAX_REPO_LENGTH} characters)")
    if "/" not in repository:
        raise CursorValidationError("Repository must be in format 'owner/repo' or a valid URL")


def validate_webhook_url(url: str) -> None:
    """Validate webhook URL to prevent SSRF attacks.

    Only allows HTTPS URLs to external hosts.

    Args:
        url: The webhook URL to validate.

    Raises:
        CursorValidationError: If the URL is invalid or potentially dangerous.
    """
    if not url or not isinstance(url, str):
        raise CursorValidationError("Webhook URL is required and must be a string")

    try:
        parsed = urlparse(url)
    except Exception as e:
        raise CursorValidationError(f"Webhook URL is not a valid URL: {e}") from e

    # Security: Only allow HTTPS
    if parsed.scheme != "https":
        raise CursorValidationError("Webhook URL must use HTTPS protocol")

    hostname = (parsed.hostname or "").lower()

    # Security: Block internal/private IP ranges
    for pattern in BLOCKED_HOSTNAME_PATTERNS:
        if pattern.search(hostname):
            raise CursorValidationError("Webhook URL cannot point to internal/private addresses")

    # Security: Block cloud metadata endpoints
    if hostname in ("169.254.169.254", "metadata.google.internal"):
        raise CursorValidationError("Webhook URL cannot point to cloud metadata services")


def sanitize_error(error: Any) -> str:
    """Sanitize error messages to prevent sensitive data leakage.

    Args:
        error: The error to sanitize.

    Returns:
        Sanitized error message string.
    """
    message = str(error) if not isinstance(error, str) else error
    # Remove potential API keys, tokens, or sensitive patterns
    message = re.sub(r"Bearer\s+[a-zA-Z0-9._-]+", "Bearer [REDACTED]", message, flags=re.IGNORECASE)
    message = re.sub(
        r"api[_-]?key[=:]\s*[\"']?[a-zA-Z0-9._-]+[\"']?", "api_key=[REDACTED]", message, flags=re.IGNORECASE
    )
    message = re.sub(r"token[=:]\s*[\"']?[a-zA-Z0-9._-]+[\"']?", "token=[REDACTED]", message, flags=re.IGNORECASE)
    return message


# =============================================================================
# Connector
# =============================================================================


class CursorConnector(DirectedInputsClass):
    """Cursor Background Agent API connector.

    Provides HTTP client access to Cursor's agent management API for spawning,
    monitoring, and coordinating AI coding agents.

    Args:
        api_key: Cursor API key. Defaults to CURSOR_API_KEY env var.
        base_url: API base URL. Only override for testing.
        timeout: Request timeout in seconds. Default 60s.
        logger: Optional logger instance.
        **kwargs: Additional DirectedInputsClass arguments.

    Example:
        >>> connector = CursorConnector()
        >>> agents = connector.list_agents()
        >>> for agent in agents:
        ...     print(f"{agent.id}: {agent.state}")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        logger: Optional[Logging] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.logging = logger or Logging(logger_name="CursorConnector")
        self.logger = self.logging.logger

        # Get API key from input, env, or constructor
        self.api_key = api_key or self.get_input("CURSOR_API_KEY", required=False) or os.environ.get("CURSOR_API_KEY")
        if not self.api_key:
            raise CursorError("CURSOR_API_KEY is required. Set it in environment or pass to constructor.")

        # Security: Only allow base_url via explicit programmatic configuration
        # Do NOT allow env var override to prevent SSRF attacks
        self.base_url = base_url or DEFAULT_BASE_URL
        self.timeout = timeout

        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

        self.logger.info(f"Initialized CursorConnector with base URL: {self.base_url}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    @staticmethod
    def is_available() -> bool:
        """Check if API key is available.

        Returns:
            True if CURSOR_API_KEY is set in environment.
        """
        return bool(os.environ.get("CURSOR_API_KEY"))

    def _request(
        self,
        endpoint: str,
        method: str = "GET",
        json_body: Optional[dict[str, Any]] = None,
    ) -> Optional[dict[str, Any]]:
        """Make an HTTP request to the Cursor API.

        Args:
            endpoint: API endpoint path (e.g., "/agents").
            method: HTTP method.
            json_body: Optional JSON body for POST/PUT requests.

        Returns:
            JSON response data or None for empty responses.

        Raises:
            CursorAPIError: If the API returns an error.
        """
        try:
            response = self._client.request(
                method=method,
                url=endpoint,
                json=json_body,
            )

            if not response.is_success:
                error_text = response.text
                try:
                    error_data = response.json()
                    details = error_data.get("message") or error_data.get("error") or "Unknown API error"
                except Exception:
                    details = sanitize_error(error_text)

                raise CursorAPIError(f"API Error {response.status_code}: {details}", status_code=response.status_code)

            # Handle empty responses (e.g., 204 No Content)
            content_type = response.headers.get("content-type", "")
            if "application/json" not in content_type:
                return None

            text = response.text
            if not text or not text.strip():
                return None

            return response.json()

        except httpx.TimeoutException as e:
            raise CursorAPIError(f"Request timeout after {self.timeout}s") from e
        except httpx.RequestError as e:
            raise CursorAPIError(sanitize_error(str(e))) from e

    # =========================================================================
    # Agent Operations
    # =========================================================================

    def list_agents(self) -> list[Agent]:
        """List all agents.

        Returns:
            List of Agent objects.

        Raises:
            CursorAPIError: If the API request fails.
        """
        self.logger.info("Listing agents")
        data = self._request("/agents")
        if not data:
            return []

        agents_data = data.get("agents", [])
        return [Agent.model_validate(a) for a in agents_data]

    def get_agent_status(self, agent_id: str) -> Agent:
        """Get status of a specific agent.

        Args:
            agent_id: The agent identifier.

        Returns:
            Agent object with current status.

        Raises:
            CursorValidationError: If agent_id is invalid.
            CursorAPIError: If the API request fails or returns empty response.
        """
        validate_agent_id(agent_id)
        self.logger.info(f"Getting status for agent: {agent_id}")

        data = self._request(f"/agents/{agent_id}")
        if not data:
            raise CursorAPIError(f"Empty response when getting agent status for {agent_id}")
        return Agent.model_validate(data)

    def get_agent_conversation(self, agent_id: str) -> Conversation:
        """Get conversation history for an agent.

        Args:
            agent_id: The agent identifier.

        Returns:
            Conversation object with message history.

        Raises:
            CursorValidationError: If agent_id is invalid.
            CursorAPIError: If the API request fails.
        """
        validate_agent_id(agent_id)
        self.logger.info(f"Getting conversation for agent: {agent_id}")

        data = self._request(f"/agents/{agent_id}/conversation")
        if not data:
            return Conversation(agent_id=agent_id, messages=[])

        messages = [ConversationMessage.model_validate(m) for m in data.get("messages", [])]
        return Conversation(agent_id=agent_id, messages=messages)

    def launch_agent(
        self,
        prompt_text: str,
        repository: str,
        ref: Optional[str] = None,
        images: Optional[list[dict[str, Any]]] = None,
        auto_create_pr: bool = True,
        branch_name: Optional[str] = None,
        open_as_cursor_github_app: bool = True,
        skip_reviewer_request: bool = False,
        webhook_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
    ) -> Agent:
        """Launch a new agent.

        Args:
            prompt_text: The task description for the agent.
            repository: Repository name (owner/repo) or URL.
            ref: Git ref (branch/tag/commit). Defaults to default branch.
            images: Optional list of images with data and dimensions.
            auto_create_pr: Whether to automatically create a PR.
            branch_name: Custom branch name for the PR.
            open_as_cursor_github_app: Open PR as Cursor GitHub App.
            skip_reviewer_request: Skip reviewer request on PR.
            webhook_url: Webhook URL for status updates.
            webhook_secret: Webhook secret for signature verification.

        Returns:
            The launched Agent object.

        Raises:
            CursorValidationError: If inputs are invalid.
            CursorAPIError: If the API request fails.
        """
        validate_prompt_text(prompt_text)
        validate_repository(repository)

        if ref is not None:
            if not isinstance(ref, str) or len(ref) > 200:
                raise CursorValidationError("Invalid ref: must be a string under 200 characters")

        if webhook_url:
            validate_webhook_url(webhook_url)

        self.logger.info(f"Launching agent for repository: {repository}")

        body: dict[str, Any] = {
            "prompt": {
                "text": prompt_text,
            },
            "source": {
                "repository": repository,
            },
        }

        if images:
            body["prompt"]["images"] = images

        if ref:
            body["source"]["ref"] = ref

        target: dict[str, Any] = {}
        if auto_create_pr is not None:
            target["autoCreatePr"] = auto_create_pr
        if branch_name:
            target["branchName"] = branch_name
        if open_as_cursor_github_app is not None:
            target["openAsCursorGithubApp"] = open_as_cursor_github_app
        if skip_reviewer_request is not None:
            target["skipReviewerRequest"] = skip_reviewer_request
        if target:
            body["target"] = target

        if webhook_url:
            webhook: dict[str, Any] = {"url": webhook_url}
            if webhook_secret:
                webhook["secret"] = webhook_secret
            body["webhook"] = webhook

        data = self._request("/agents", method="POST", json_body=body)
        if not data:
            raise CursorAPIError("Empty response when launching agent")
        return Agent.model_validate(data)

    def add_followup(self, agent_id: str, prompt_text: str) -> None:
        """Send a follow-up message to an agent.

        Args:
            agent_id: The agent identifier.
            prompt_text: The follow-up message text.

        Raises:
            CursorValidationError: If inputs are invalid.
            CursorAPIError: If the API request fails.
        """
        validate_agent_id(agent_id)
        validate_prompt_text(prompt_text)

        self.logger.info(f"Adding follow-up to agent: {agent_id}")

        self._request(
            f"/agents/{agent_id}/followup",
            method="POST",
            json_body={"prompt": {"text": prompt_text}},
        )

    # =========================================================================
    # Repository Operations
    # =========================================================================

    def list_repositories(self) -> list[Repository]:
        """List available repositories.

        Returns:
            List of Repository objects.

        Raises:
            CursorAPIError: If the API request fails.
        """
        self.logger.info("Listing repositories")
        data = self._request("/repositories")
        if not data:
            return []

        repos_data = data.get("repositories", [])
        return [Repository.model_validate(r) for r in repos_data]

    # =========================================================================
    # Model Operations
    # =========================================================================

    def list_models(self) -> list[str]:
        """List available models.

        Returns:
            List of model names.

        Raises:
            CursorAPIError: If the API request fails.
        """
        self.logger.info("Listing models")
        data = self._request("/models")
        if not data:
            return []

        return data.get("models", [])

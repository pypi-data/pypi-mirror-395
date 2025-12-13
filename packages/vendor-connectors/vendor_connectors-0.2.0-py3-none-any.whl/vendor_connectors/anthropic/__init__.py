"""Anthropic Connector - Claude AI SDK wrapper for the jbcom ecosystem.

This connector provides Python access to Anthropic's Claude AI, including
the Claude Agent SDK for sandbox/local agent execution.

Usage:
    from vendor_connectors.anthropic import AnthropicConnector

    # Standard API access
    connector = AnthropicConnector(api_key="...")
    response = connector.create_message(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )

    # Agent execution (sandbox mode)
    result = await connector.execute_agent_task(
        task="Implement feature X",
        working_dir="/path/to/repo"
    )

Reference: https://docs.anthropic.com/claude/reference
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

from directed_inputs_class import DirectedInputsClass
from lifecyclelogging import Logging
from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    pass

__all__ = [
    "AnthropicConnector",
    "AnthropicError",
    "Message",
    "MessageRole",
    "ContentBlock",
    "Usage",
    "Model",
    "AgentExecutionResult",
]


# =============================================================================
# Constants
# =============================================================================

DEFAULT_API_URL = "https://api.anthropic.com"
DEFAULT_API_VERSION = "2023-06-01"
DEFAULT_TIMEOUT = 60.0
DEFAULT_MAX_TOKENS = 4096

# Available Claude models
# SOURCE OF TRUTH: https://docs.anthropic.com/en/docs/about-claude/models
# API verification: curl https://api.anthropic.com/v1/models -H "x-api-key: $KEY" -H "anthropic-version: 2023-06-01"
# Last verified: 2025-12-07
CLAUDE_MODELS = {
    # Claude 4.5 family (latest)
    "claude-opus-4-5-20251101": "Claude Opus 4.5",
    "claude-sonnet-4-5-20250929": "Claude Sonnet 4.5",
    "claude-haiku-4-5-20251001": "Claude Haiku 4.5",
    # Claude 4.1 family
    "claude-opus-4-1-20250805": "Claude Opus 4.1",
    # Claude 4 family
    "claude-sonnet-4-20250514": "Claude Sonnet 4",
    "claude-opus-4-20250514": "Claude Opus 4",
    # Claude 3.7 family
    "claude-3-7-sonnet-20250219": "Claude Sonnet 3.7",
    # Claude 3.5 family
    "claude-3-5-haiku-20241022": "Claude Haiku 3.5",
    # Claude 3 family
    "claude-3-opus-20240229": "Claude Opus 3",
    "claude-3-haiku-20240307": "Claude Haiku 3",
}


# =============================================================================
# Exceptions
# =============================================================================


class AnthropicError(Exception):
    """Base exception for Anthropic API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, error_type: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_type = error_type


class AnthropicAuthError(AnthropicError):
    """Authentication error."""


class AnthropicRateLimitError(AnthropicError):
    """Rate limit exceeded error."""


class AnthropicAPIError(AnthropicError):
    """API error from Anthropic service."""


# =============================================================================
# Models
# =============================================================================


class MessageRole(str, Enum):
    """Message role in conversation."""

    USER = "user"
    ASSISTANT = "assistant"


class ContentBlock(BaseModel):
    """Content block within a message."""

    model_config = ConfigDict(extra="allow")

    type: str = Field(description="Content type (text, image, tool_use, tool_result)")
    text: Optional[str] = Field(default=None, description="Text content")
    id: Optional[str] = Field(default=None, description="Tool use ID")
    name: Optional[str] = Field(default=None, description="Tool name")
    input: Optional[dict[str, Any]] = Field(default=None, description="Tool input")


class Usage(BaseModel):
    """Token usage information."""

    model_config = ConfigDict(extra="allow")

    input_tokens: int = Field(description="Number of input tokens")
    output_tokens: int = Field(description="Number of output tokens")


class Message(BaseModel):
    """Claude message response."""

    model_config = ConfigDict(extra="allow")

    id: str = Field(description="Message ID")
    type: str = Field(default="message", description="Response type")
    role: MessageRole = Field(description="Message role")
    content: list[ContentBlock] = Field(description="Message content blocks")
    model: str = Field(description="Model used")
    stop_reason: Optional[str] = Field(default=None, description="Stop reason")
    stop_sequence: Optional[str] = Field(default=None, description="Stop sequence if triggered")
    usage: Usage = Field(description="Token usage")

    @property
    def text(self) -> str:
        """Get the text content of the message."""
        text_blocks = [b.text for b in self.content if b.type == "text" and b.text]
        return "".join(text_blocks)


class Model(BaseModel):
    """Claude model information."""

    model_config = ConfigDict(extra="allow")

    id: str = Field(description="Model ID")
    display_name: str = Field(description="Human-readable model name")
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp")


@dataclass
class AgentExecutionResult:
    """Result of agent task execution."""

    success: bool
    output: str
    error: Optional[str] = None
    duration_seconds: Optional[float] = None
    tokens_used: Optional[int] = None


# =============================================================================
# Connector
# =============================================================================


class AnthropicConnector(DirectedInputsClass):
    """Anthropic Claude API connector.

    Provides HTTP client access to Anthropic's Claude AI API for message
    generation and agent execution.

    Args:
        api_key: Anthropic API key. Defaults to ANTHROPIC_API_KEY env var.
        api_version: API version string. Default "2023-06-01".
        timeout: Request timeout in seconds. Default 60s.
        logger: Optional logger instance.
        **kwargs: Additional DirectedInputsClass arguments.

    Example:
        >>> connector = AnthropicConnector()
        >>> response = connector.create_message(
        ...     model="claude-sonnet-4-20250514",
        ...     max_tokens=1024,
        ...     messages=[{"role": "user", "content": "Hello"}]
        ... )
        >>> print(response.text)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_version: str = DEFAULT_API_VERSION,
        timeout: float = DEFAULT_TIMEOUT,
        logger: Optional[Logging] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.logging = logger or Logging(logger_name="AnthropicConnector")
        self.logger = self.logging.logger

        # Get API key
        self.api_key = (
            api_key or self.get_input("ANTHROPIC_API_KEY", required=False) or os.environ.get("ANTHROPIC_API_KEY")
        )
        if not self.api_key:
            raise AnthropicError("ANTHROPIC_API_KEY is required. Set it in environment or pass to constructor.")

        self.api_version = api_version
        self.timeout = timeout

        # Lazy import httpx to avoid issues if not installed
        import httpx

        self._client = httpx.Client(
            base_url=DEFAULT_API_URL,
            timeout=self.timeout,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": self.api_version,
                "Content-Type": "application/json",
            },
        )

        self.logger.info(f"Initialized AnthropicConnector with API version: {self.api_version}")

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
            True if ANTHROPIC_API_KEY is set in environment.
        """
        return bool(os.environ.get("ANTHROPIC_API_KEY"))

    @staticmethod
    def get_available_models() -> dict[str, str]:
        """Get dictionary of available Claude models.

        Returns:
            Dictionary mapping model IDs to display names.
        """
        return CLAUDE_MODELS.copy()

    def _handle_error(self, response) -> None:
        """Handle API error responses.

        Args:
            response: httpx Response object.

        Raises:
            AnthropicError: Appropriate error type for the response.
        """
        status_code = response.status_code
        try:
            error_data = response.json()
            error_type = error_data.get("error", {}).get("type", "unknown")
            message = error_data.get("error", {}).get("message", response.text)
        except Exception:
            error_type = "unknown"
            message = response.text

        if status_code == 401:
            raise AnthropicAuthError(message, status_code=status_code, error_type=error_type)
        elif status_code == 429:
            raise AnthropicRateLimitError(message, status_code=status_code, error_type=error_type)
        else:
            raise AnthropicAPIError(message, status_code=status_code, error_type=error_type)

    # =========================================================================
    # Message Operations
    # =========================================================================

    def create_message(
        self,
        model: str,
        max_tokens: int,
        messages: list[dict[str, Any]],
        system: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        stop_sequences: Optional[list[str]] = None,
        tools: Optional[list[dict[str, Any]]] = None,
        tool_choice: Optional[dict[str, Any]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> Message:
        """Create a message using Claude.

        Args:
            model: Model ID (e.g., "claude-sonnet-4-20250514").
            max_tokens: Maximum tokens to generate.
            messages: List of message dicts with role and content.
            system: Optional system prompt.
            temperature: Sampling temperature (0-1).
            top_p: Top-p sampling parameter.
            top_k: Top-k sampling parameter.
            stop_sequences: Stop sequences to end generation.
            tools: Tool definitions for function calling.
            tool_choice: Tool choice configuration.
            metadata: Optional metadata for the request.

        Returns:
            Message object with response.

        Raises:
            AnthropicError: If the API request fails.
        """
        self.logger.info(f"Creating message with model: {model}")

        body: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
        }

        if system:
            body["system"] = system
        if temperature is not None:
            body["temperature"] = temperature
        if top_p is not None:
            body["top_p"] = top_p
        if top_k is not None:
            body["top_k"] = top_k
        if stop_sequences:
            body["stop_sequences"] = stop_sequences
        if tools:
            body["tools"] = tools
        if tool_choice:
            body["tool_choice"] = tool_choice
        if metadata:
            body["metadata"] = metadata

        response = self._client.post("/v1/messages", json=body)

        if not response.is_success:
            self._handle_error(response)

        return Message.model_validate(response.json())

    def count_tokens(
        self,
        model: str,
        messages: list[dict[str, Any]],
        system: Optional[str] = None,
        tools: Optional[list[dict[str, Any]]] = None,
    ) -> int:
        """Count tokens for a set of messages.

        Args:
            model: Model ID.
            messages: List of message dicts.
            system: Optional system prompt.
            tools: Optional tool definitions.

        Returns:
            Token count.

        Raises:
            AnthropicError: If the API request fails.
        """
        self.logger.info(f"Counting tokens for model: {model}")

        body: dict[str, Any] = {
            "model": model,
            "messages": messages,
        }

        if system:
            body["system"] = system
        if tools:
            body["tools"] = tools

        response = self._client.post("/v1/messages/count_tokens", json=body)

        if not response.is_success:
            self._handle_error(response)

        data = response.json()
        return data.get("input_tokens", 0)

    # =========================================================================
    # Model Operations
    # =========================================================================

    def list_models(self) -> list[Model]:
        """List available models from the API.

        Returns:
            List of Model objects.

        Raises:
            AnthropicError: If the API request fails.
        """
        self.logger.info("Listing models from API")

        response = self._client.get("/v1/models")

        if not response.is_success:
            self._handle_error(response)

        data = response.json()
        models_data = data.get("data", [])
        return [Model.model_validate(m) for m in models_data]

    def get_model(self, model_id: str) -> Model:
        """Get information about a specific model.

        Args:
            model_id: Model identifier.

        Returns:
            Model object with details.

        Raises:
            AnthropicError: If the API request fails.
        """
        self.logger.info(f"Getting model info: {model_id}")

        response = self._client.get(f"/v1/models/{model_id}")

        if not response.is_success:
            self._handle_error(response)

        return Model.model_validate(response.json())

    # =========================================================================
    # Agent Execution (Sandbox Mode)
    # =========================================================================

    def execute_agent_task(
        self,
        task: str,
        working_dir: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929",  # Claude Sonnet 4.5 - verified
        max_tokens: int = DEFAULT_MAX_TOKENS,
        system_prompt: Optional[str] = None,
    ) -> AgentExecutionResult:
        """Execute a task using Claude as an agent (sandbox mode).

        This is a simplified agent execution pattern for local single-agent
        workflows. For full agent capabilities, consider using LangChain agents
        or the agentic-control package.

        Args:
            task: The task description.
            working_dir: Working directory for execution context.
            model: Model to use (default: claude-sonnet-4-5-20250929).
            max_tokens: Maximum tokens per response.
            system_prompt: Optional custom system prompt.

        Returns:
            AgentExecutionResult with execution details.

        Note:
            This is a simplified synchronous implementation. For production
            agent workflows with tools and multi-turn conversations, consider
            using LangChain/LangGraph which will be available in the
            vendor_connectors.ai sub-package.
        """
        import time

        self.logger.info(f"Executing agent task: {task[:100]}...")
        start_time = time.time()

        default_system = """You are a helpful AI assistant that executes coding tasks.
When given a task, analyze it carefully and provide a detailed response.
If the task requires code changes, describe exactly what changes should be made."""

        if working_dir:
            default_system += f"\n\nWorking directory: {working_dir}"

        try:
            response = self.create_message(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt or default_system,
                messages=[{"role": "user", "content": task}],
            )

            duration = time.time() - start_time
            total_tokens = response.usage.input_tokens + response.usage.output_tokens

            return AgentExecutionResult(
                success=True,
                output=response.text,
                duration_seconds=duration,
                tokens_used=total_tokens,
            )

        except AnthropicError as e:
            duration = time.time() - start_time
            return AgentExecutionResult(
                success=False,
                output="",
                error=str(e),
                duration_seconds=duration,
            )

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def validate_model(self, model_id: str) -> bool:
        """Check if a model ID is valid.

        Args:
            model_id: Model identifier to validate.

        Returns:
            True if model exists in known models.
        """
        return model_id in CLAUDE_MODELS

    def get_recommended_model(self, use_case: str = "general") -> str:
        """Get recommended model for a use case.

        Args:
            use_case: Use case type ("general", "coding", "fast", "powerful").

        Returns:
            Recommended model ID.
        """
        # Using verified model IDs from Anthropic API
        recommendations = {
            "general": "claude-sonnet-4-5-20250929",  # Claude Sonnet 4.5 - best balance
            "coding": "claude-sonnet-4-5-20250929",  # Claude Sonnet 4.5 - great for code
            "fast": "claude-haiku-4-5-20251001",  # Claude Haiku 4.5 - fastest
            "powerful": "claude-opus-4-5-20251101",  # Claude Opus 4.5 - most capable
        }
        return recommendations.get(use_case, recommendations["general"])

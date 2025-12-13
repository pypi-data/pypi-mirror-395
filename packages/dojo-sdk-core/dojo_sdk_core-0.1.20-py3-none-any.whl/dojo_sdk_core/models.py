import json
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple, TypedDict

from pydantic import BaseModel, Field


# V2 reward types
class StateKeyQuery(TypedDict):
    collection: str
    filter: Dict[str, Any]


StateKey = Dict[str, StateKeyQuery]
ValidatorFunc = Callable[[Dict[str, Any], Dict[str, Any]], Tuple[float, str]]


class ValidateTask(TypedDict):
    state_key: StateKey
    validate_backend: ValidatorFunc
    validate_frontend: ValidatorFunc


class SettingsConfig(BaseModel):
    """Settings configuration."""

    anthropic_api_key: str = Field("", description="Anthropic API key")
    openai_api_key: str = Field("", description="OpenAI API key")
    openai_api_url: str = Field("", description="OpenAI API URL")
    dojo_websocket_endpoint: str = Field("", description="Dojo websocket endpoint")
    dojo_http_endpoint: str = Field("", description="Dojo http endpoint")
    posthog_api_key: str = Field("", description="PostHog API key")
    engine: str = Field("docker", description="Engine to use")
    browserbase_concurrent_limit: int = Field(1, description="Concurrent limit for BrowserBase engine")


class EnvironmentConfig(BaseModel):
    """Environment configuration."""

    type: str = Field(..., description="Environment type (e.g., 'spa')")
    path: str = Field(..., description="Path to environment file")


class InstructionsConfig(BaseModel):
    """Task instructions configuration."""

    user_prompt: str = Field(..., description="Prompt to show to the agent")
    success_criteria: str = Field(..., description="What constitutes success")


class TaskDefinition(BaseModel):
    """Complete task definition."""

    spa: str = Field(..., description="SPA name")
    id: str = Field(..., description="Unique task identifier")
    name: str = Field(..., description="Human-readable task name")
    description: str = Field(..., description="Task description")
    environment: EnvironmentConfig = Field(..., description="Environment configuration")
    initial_state: dict[str, Any] = Field(..., description="Initial state for the environment")
    instructions: InstructionsConfig = Field(..., description="Task instructions")
    reward: Optional[ValidateTask] = Field(
        None,
        description="ValidateTask bundle with state_key, validate_backend, validate_frontend",
    )
    max_steps: int = Field(default=10, description="Maximum number of steps allowed")
    timeout_seconds: int = Field(default=60, description="Task timeout in seconds")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    def model_post_init(self, __context: Any) -> None:
        """Validate that reward is provided."""
        if not self.reward:
            raise ValueError("reward must be provided")

    def get_environment_path(self, base_path: Optional[Path] = None) -> Path:
        """Get absolute path to environment file."""
        if base_path is None:
            base_path = Path.cwd()
        return base_path / self.environment.path

    @classmethod
    def from_hf_row(
        cls, row: dict[str, Any], reward_importer: Optional[Callable[[str], Optional[ValidateTask]]] = None
    ) -> "TaskDefinition":
        """Create a TaskDefinition from a HuggingFace dataset row."""
        initial_state = json.loads(row["initial_state"])
        environment = json.loads(row["environment"])
        instructions = json.loads(row["instructions"])
        metadata = json.loads(row["metadata"])

        reward = None
        if row["reward_function"] and row["reward_function"].strip():
            if reward_importer:
                reward = reward_importer(row["reward_function"])

        return cls(
            id=row["id"],
            spa=row["spa"],
            name=row["name"],
            description=row["description"],
            environment=environment,
            initial_state=initial_state,
            instructions=instructions,
            reward=reward,
            max_steps=row["max_steps"],
            timeout_seconds=row["timeout_seconds"],
            metadata=metadata,
        )

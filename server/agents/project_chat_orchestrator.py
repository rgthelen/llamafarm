import sys
from pathlib import Path

import instructor
from atomic_agents import AgentConfig, AtomicAgent, BaseIOSchema  # type: ignore
from atomic_agents.agents.atomic_agent import (  # type: ignore
    ChatHistory,
    SystemPromptGenerator,
)
from openai import OpenAI

from core.settings import settings  # type: ignore

repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))
from config.datamodel import LlamaFarmConfig, Prompt, Provider  # noqa: E402


class ProjectChatOrchestratorAgentInputSchema(BaseIOSchema):
    """
    Input schema for the project chat orchestrator agent.
    """

    chat_message: str


class ProjectChatOrchestratorAgentOutputSchema(BaseIOSchema):
    """
    Output schema for the project chat orchestrator agent.
    """

    chat_message: str


class ProjectChatOrchestratorAgent(
    AtomicAgent[
        ProjectChatOrchestratorAgentInputSchema,
        ProjectChatOrchestratorAgentOutputSchema,
    ]
):
    def __init__(self, project_config: LlamaFarmConfig):
        history = _get_history(project_config)
        client = _get_client(project_config)
        super().__init__(
            config=AgentConfig(
                client=client,
                model=project_config.runtime.model,
                history=history,
                system_prompt_generator=LFSystemPromptGenerator(
                    project_config=project_config
                ),
                model_api_parameters=project_config.runtime.model_api_parameters,
            )
        )


class LFSystemPromptGenerator(SystemPromptGenerator):
    def __init__(self, project_config: LlamaFarmConfig):
        self.system_prompts = [
            prompt for prompt in project_config.prompts if prompt.role == "system"
        ]
        super().__init__()

    def generate_prompt(self) -> str:
        return "\n".join([prompt.content for prompt in self.system_prompts])


def _prompt_to_content_schema(prompt: Prompt) -> BaseIOSchema:
    if prompt.role == "assistant":
        return ProjectChatOrchestratorAgentOutputSchema(
            chat_message=prompt.content,
        )
    elif prompt.role == "user":
        return ProjectChatOrchestratorAgentInputSchema(
            chat_message=prompt.content,
        )
    else:
        raise ValueError(f"Unsupported role: {prompt.role}")


def _populate_history_with_non_system_prompts(
    history: ChatHistory, project_config: LlamaFarmConfig
):
    for prompt in project_config.prompts:
        # Only add non-system prompts to the history
        if prompt.role != "system":
            history.add_message(
                role=prompt.role,
                content=_prompt_to_content_schema(prompt),
            )


def _get_history(project_config: LlamaFarmConfig) -> ChatHistory:
    history = ChatHistory()
    _populate_history_with_non_system_prompts(history, project_config)
    return history


def _get_client(project_config: LlamaFarmConfig) -> instructor.client.Instructor:
    mode = (
        instructor.mode.Mode[project_config.runtime.instructor_mode.upper()]
        if project_config.runtime.instructor_mode is not None
        else instructor.Mode.TOOLS
    )

    if project_config.runtime.provider == Provider.openai:
        return instructor.from_openai(
            OpenAI(
                api_key=project_config.runtime.api_key,
                base_url=project_config.runtime.base_url,
            ),
            mode=mode,
        )
    if project_config.runtime.provider == Provider.ollama:
        return instructor.from_openai(
            OpenAI(
                api_key=project_config.runtime.api_key or settings.ollama_api_key,
                base_url=project_config.runtime.base_url
                or f"{settings.ollama_host}/v1",
            ),
            mode=mode,
        )
    else:
        raise ValueError(f"Unsupported provider: {project_config.runtime.provider}")


class ProjectChatOrchestratorAgentFactory:
    @staticmethod
    def create_agent(project_config: LlamaFarmConfig) -> ProjectChatOrchestratorAgent:
        return ProjectChatOrchestratorAgent(project_config)

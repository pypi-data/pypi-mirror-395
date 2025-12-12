import os
from typing import Optional, Callable, List

from ag_ui.core import (
    RunAgentInput,
)

from logging import getLogger
from google.adk import Runner
from google.adk.agents import BaseAgent, RunConfig as ADKRunConfig
from google.adk.sessions import BaseSessionService, InMemorySessionService
from google.adk.artifacts import BaseArtifactService, InMemoryArtifactService
from google.adk.memory import BaseMemoryService, InMemoryMemoryService
from google.adk.auth.credential_service.base_credential_service import BaseCredentialService
from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService
from google.adk.apps import App
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.cli.utils.agent_loader import AgentLoader
from google.adk.cli.utils import envs
from google.adk.cli.service_registry import get_service_registry
from google.adk.sessions.session import Session
from ag_ui_adk import ADKAgent
from ag_ui_adk.utils.converters import convert_adk_event_to_ag_ui_message
from ag_ui.core.types import Message

from .validator import AdkParams

logger = getLogger(__name__)

class AgentFactory:
    def __init__(
            self,
            params: AdkParams,
            plugins: Optional[List[BasePlugin]] = [],
            # ADK Services
        ):
        self.params = params
        self.agent_loader = AgentLoader(self.params.adk_agent_dir)
        self.plugins = plugins
        self._create_services_instance()
        self.agents_dict = {}

    def _create_services_instance(self):
        service_registry = get_service_registry()
        agents_dir = self.params.adk_agent_dir
        # Build the Memory service
        if self.params.memory_service_url:
            self.memory_service = service_registry.create_memory_service(
                self.params.memory_service_url, agents_dir=agents_dir
            )
            if not self.memory_service:
                raise Exception(
                    "Unsupported memory service URI: %s" % self.params.memory_service_url
                )
            logger.info(f"Using memory service: {self.params.memory_service_url}")
        else:
            self.memory_service = InMemoryMemoryService()
            logger.info("Using in-memory memory service")

        # Build the Session service
        if self.params.session_service_url:
            session_kwargs = self.params.session_db_kwargs or {}
            self.session_service = service_registry.create_session_service(
                self.params.session_service_url, agents_dir=agents_dir, **session_kwargs
            )
            if not self.session_service:
                # Fallback to DatabaseSessionService if the service registry doesn't
                # support the session service URI scheme.
                from google.adk.sessions.database_session_service import DatabaseSessionService

                self.session_service = DatabaseSessionService(
                    db_url=self.params.session_service_url, **session_kwargs
                )
            logger.info(f"Using session service: {self.params.session_service_url}")
        else:
            self.session_service = InMemorySessionService()
            logger.info("Using in-memory session service")

        # Build the Artifact service
        if self.params.artifact_service_uri:
            self.artifact_service = service_registry.create_artifact_service(
                self.params.artifact_service_uri, agents_dir=agents_dir
            )
            if not self.artifact_service:
                raise Exception(
                    "Unsupported artifact service URI: %s" % self.params.artifact_service_uri
                )
            logger.info(f"Using artifact service: {self.params.artifact_service_uri}")
        else:
            self.artifact_service = InMemoryArtifactService()
            logger.info("Using in-memory artifact service")

        # Build  the Credential service
        self.credential_service = InMemoryCredentialService()

    async def create_agent(self, app_name: str) -> ADKAgent:
        """Returns the cached runner for the given app."""
        # Create new agent
        envs.load_dotenv_for_agent(os.path.basename(app_name), self.params.adk_agent_dir)
        agent_or_app = self.agent_loader.load_agent(app_name)

        if isinstance(agent_or_app, BaseAgent):
            agentic_app = App(
                name=app_name,
                root_agent=agent_or_app,
                plugins=self.plugins,
            )
        else:
            # Combine existing plugins with extra plugins
            agent_or_app.plugins = agent_or_app.plugins + self.plugins
            agentic_app = agent_or_app

        agent = AguiADKAgent(
            adk_agent=agentic_app.root_agent,
            app=agentic_app,
            app_name=app_name,
            session_service=self.session_service,
            artifact_service=self.artifact_service,
            memory_service=self.memory_service,
            credential_service=self.credential_service,
        )
        self.agents_dict[app_name] = agent
        return agent
    
    async def list_agents(self) -> List[str]:
        """Lists available agents in the agent directory."""
        return self.agent_loader.list_agents()
    
    async def list_sessions(self, app_name: str, user_id: str) -> List[Session]:
        """Returns the list of sessions for the given app and user."""
        return await self.session_service.list_sessions(app_name=app_name, user_id=user_id)
    
    async def get_session(self, app_name: str, user_id: str, session_id: str) -> Optional[Session]:
        """Returns the session for the given app, user, and session ID."""
        return await self.session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )
        
    async def delete_session(self, app_name: str, user_id: str, session_id: str) -> None:
        """Deletes the session for the given app, user, and session ID."""
        await self.session_service.delete_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )
        
    async def get_messages(self, app_name: str, user_id: str, session_id: str) -> List[Message]:
        """Returns the messages for the given app, user, and session ID."""
        session = await self.get_session(app_name, user_id, session_id)
        if not session:
            return []
        return [convert_adk_event_to_ag_ui_message(event) for event in session.events]

class AguiADKAgent(ADKAgent):
    """Fixed ADKAgent that properly marks ToolMessages as processed

    This class inherits from ag_ui_adk.ADKAgent and fixes:
    1. ToolMessages not being marked as processed after handling
    2. Old ToolMessages being processed repeatedly

    Usage:
        agent = SmartradeADKAgent(
            adk_agent=my_adk_agent,
            app_name="my_app",
            ...
        )
    """
    def __init__(
        self,
        # ADK Agent instance
        adk_agent: BaseAgent,

        # Plugins
        plugins: Optional[List[BasePlugin]] = None,
        
        # App identification
        app: Optional[App] = None,
        app_name: Optional[str] = None,
        session_timeout_seconds: Optional[int] = 1200,
        app_name_extractor: Optional[Callable[[RunAgentInput], str]] = None,
        
        # User identification
        user_id: Optional[str] = None,
        user_id_extractor: Optional[Callable[[RunAgentInput], str]] = None,
        
        # ADK Services
        session_service: Optional[BaseSessionService] = None,
        artifact_service: Optional[BaseArtifactService] = None,
        memory_service: Optional[BaseMemoryService] = None,
        credential_service: Optional[BaseCredentialService] = None,
        
        # Configuration
        run_config_factory: Optional[Callable[[RunAgentInput], ADKRunConfig]] = None,
        use_in_memory_services: bool = True,
        
        # Tool configuration
        execution_timeout_seconds: int = 600,  # 10 minutes
        tool_timeout_seconds: int = 300,  # 5 minutes
        max_concurrent_executions: int = 10,
        
        # Session cleanup configuration
        cleanup_interval_seconds: int = 300  # 5 minutes default
    ):
        super().__init__(
            adk_agent=adk_agent,
            app_name=app_name,
            session_timeout_seconds=session_timeout_seconds,
            app_name_extractor=app_name_extractor,
            user_id=user_id,
            user_id_extractor=user_id_extractor,
            session_service=session_service,
            artifact_service=artifact_service,
            memory_service=memory_service,
            credential_service=credential_service,
            run_config_factory=run_config_factory,
            use_in_memory_services=use_in_memory_services,
            execution_timeout_seconds=execution_timeout_seconds,
            tool_timeout_seconds=tool_timeout_seconds,
            max_concurrent_executions=max_concurrent_executions,
            cleanup_interval_seconds=cleanup_interval_seconds,
        )
        self.app = app
        self.plugins = plugins

    def _create_runner(self, adk_agent, user_id, app_name):
        """Create a runner for the given app."""
        return Runner(
            app=self.app,
            session_service=self._session_manager._session_service,
            artifact_service=self._artifact_service,
            memory_service=self._memory_service,
            credential_service=self._credential_service,
            plugins=self.plugins,
        )

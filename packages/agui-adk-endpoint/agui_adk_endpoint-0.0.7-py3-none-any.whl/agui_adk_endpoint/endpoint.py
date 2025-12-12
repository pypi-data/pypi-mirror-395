# src/endpoint.py

"""FastAPI endpoint for ADK middleware."""

from logging import getLogger
from typing import Optional
from ag_ui.core import RunAgentInput, BaseEvent
from ag_ui.core.events import EventType
from ag_ui.encoder import EventEncoder
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import StreamingResponse

from .validator import AdkParams
from .factory import AgentFactory

logger = getLogger(__name__)


class AdkFastAPIEndpoint:
    """ADK middleware endpoint."""

    def __init__(self, params: AdkParams, prefix="/adk", plugins=[]):
        self.agent_factory = AgentFactory(params=params, plugins=plugins)
        self.prefix = prefix


    def add_fastapi_endpoint(self, app: FastAPI):
        """Create a fastapi endpoint router for all ADK apps.

        Args:+
            app: FastAPI application instance
        """

        adk_router = APIRouter(prefix=self.prefix)

        @adk_router.post("/{agent_name}/run")
        async def run(agent_name: str, input_data: RunAgentInput, request: Request):
            """ADK middleware endpoint.

            Args:
                agent_name: Name of the agent to run (from path parameter)
                input_data: Agent input data
                request: HTTP request object
            """

            logger.info(f"Input data: {input_data}")

            # Get the accept header from the request
            accept_header = request.headers.get("accept")

            logger.info(f"🚀 Running agent: {agent_name}")

            agent = await self.agent_factory.create_agent(agent_name)

            # Create an event encoder to properly format SSE events
            encoder = EventEncoder(accept=accept_header)

            async def event_generator():
                """Generate events from ADK agent."""
                try:
                    async for event in agent.run(input_data):
                        try:
                            encoded = encoder.encode(event)
                            yield encoded
                        except Exception as encoding_error:
                            # Handle encoding-specific errors
                            logger.error(
                                f"❌ Event encoding error: {encoding_error}",
                                exc_info=True,
                            )
                            # Create a RunErrorEvent for encoding failures
                            from ag_ui.core import EventType, RunErrorEvent

                            error_event = RunErrorEvent(
                                type=EventType.RUN_ERROR,
                                message=f"Event encoding failed: {str(encoding_error)}",
                                code="ENCODING_ERROR",
                            )
                            try:
                                error_encoded = encoder.encode(error_event)
                                yield error_encoded
                            except Exception:
                                # If we can't even encode the error event, yield a basic SSE error
                                logger.error(
                                    "Failed to encode error event, yielding basic SSE error"
                                )
                                yield 'event: error\ndata: {"error": "Event encoding failed"}\n\n'
                            break  # Stop the stream after an encoding error
                except Exception as agent_error:
                    # Handle errors from ADKAgent.run() itself
                    logger.error(f"❌ ADKAgent error: {agent_error}", exc_info=True)
                    # ADKAgent should have yielded a RunErrorEvent, but if something went wrong
                    # in the async generator itself, we need to handle it
                    try:
                        from ag_ui.core import EventType, RunErrorEvent

                        error_event = RunErrorEvent(
                            type=EventType.RUN_ERROR,
                            message=f"Agent execution failed: {str(agent_error)}",
                            code="AGENT_ERROR",
                        )
                        error_encoded = encoder.encode(error_event)
                        yield error_encoded
                    except Exception:
                        # If we can't encode the error event, yield a basic SSE error
                        logger.error(
                            "Failed to encode agent error event, yielding basic SSE error"
                        )
                        yield 'event: error\ndata: {"error": "Agent execution failed"}\n\n'

            return StreamingResponse(
                event_generator(), media_type=encoder.get_content_type()
            )

        app.include_router(adk_router)

def create_endpoint(
        prefix: str = "/adk", 
        plugins=[],
        agent_dir: Optional[str] = None) -> AdkFastAPIEndpoint:
    """Create an ADK endpoint.

    Args:
        agent_dir: Directory containing agent definitions (optional)
    """
    from .validator import validate_parameters
    params = validate_parameters(agent_dir)
    return AdkFastAPIEndpoint(params, prefix=prefix, plugins=plugins)
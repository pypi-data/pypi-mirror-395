import logging
from ag_ui.core import RunAgentInput

logger = logging.getLogger(__name__)

def user_id_extractor(input: RunAgentInput) -> str:
    """Extract user ID from RunAgentInput."""
    try:
        user_id = input.forwarded_props.get("user_id", "anonymous")
    except AttributeError:
        logger.warning("forwarded_props is not a dict-like object.")
        user_id = "anonymous"
    return user_id
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)

class AdkParams(BaseModel):
    adk_agent_dir: str
    memory_service_url: Optional[str] = None
    session_service_url: Optional[str] = None
    artifact_service_uri: Optional[str] = None
    credential_service_url: Optional[str] = None
    session_db_kwargs: dict = {}

    @field_validator('adk_agent_dir')
    @classmethod
    def validate_adk_agent_dir(cls, v: str) -> str:
        """验证 adk_agent_dir 是一个存在的目录路径"""
        if not v:
            raise ValueError('adk_agent_dir 不能为空')

        path = Path(v).expanduser().resolve()

        if not path.exists():
            raise ValueError(f'adk_agent_dir 指定的路径不存在: {v}')

        if not path.is_dir():
            raise ValueError(f'adk_agent_dir 必须是目录，但指向的是文件: {v}')

        return str(path)

def validate_parameters(agent_dir: str = None) -> AdkParams:
    """验证并返回 ADK 参数"""
    load_dotenv()

    adk_agent_dir = os.getenv('ADK_AGENT_DIR')
    if not adk_agent_dir:
        if agent_dir:
            adk_agent_dir = agent_dir
        else:
            raise ValueError('ADK_AGENT_DIR 环境变量未设置')
        
    try:
        import json
        session_db_options = os.getenv('ADK_SESSION_DB_OPTIONS', '{}')
        config = json.loads(session_db_options)
    except Exception as e:
        logger.error(f"解析 ADK_SESSION_DB_OPTIONS 失败: {e}, ADK_SESSION_DB_OPTIONS: {session_db_options}")
        config = {}

    params = AdkParams(
        adk_agent_dir=adk_agent_dir,
        memory_service_url=os.getenv('ADK_MEMORY_SERVICE_URL', None),
        session_service_url=os.getenv('ADK_SESSION_SERVICE_URL', None),
        artifact_service_uri=os.getenv('ADK_ARTIFACT_SERVICE_URI', None),
        credential_service_url=os.getenv('ADK_CREDENTIAL_SERVICE_URL', None),
        session_db_kwargs=config
    )

    return params
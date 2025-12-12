from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoint import create_endpoint

def create_webserver(
        host: str = '127.0.0.1', 
        port: int = 8000,
        agent_dir: Optional[str] = None,
        allow_origins: Optional[list[str]] = None,) -> FastAPI:
    app = FastAPI()

    if allow_origins:
      app.add_middleware(
          CORSMiddleware,
          allow_origins=allow_origins,
          allow_credentials=True,
          allow_methods=["*"],
          allow_headers=["*"],
      )

    # Add AG-UI endpoint
    endpoint = create_endpoint(agent_dir=agent_dir)
    endpoint.add_fastapi_endpoint(app)

    return app


    
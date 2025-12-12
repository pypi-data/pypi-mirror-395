from __future__ import annotations
import os
import sys
from collections.abc import Sequence
from fastapi import FastAPI, APIRouter
from pathlib import Path
from starlette.routing import BaseRoute


from .middlewares import TagflowMiddleware
from .responses import TagResponse
from .utils import autodiscover_modules, VersionedStaticFiles


APP_PATH = Path(os.getcwd()).absolute()
sys.path.append(APP_PATH)

from .config import settings


class App(FastAPI):

    def __init__(
        self,
        debug: bool = False,
        routes: Sequence[BaseRoute] | None = None,
    ) -> None:
        
        super().__init__(debug=debug, default_response_class=TagResponse)

        self.add_middleware(TagflowMiddleware)

        self.mount(
            "/static",
            VersionedStaticFiles(directory=Path(APP_PATH) / "static"),
            name="static",
        ) 

        router = APIRouter()

        self.discovered_modules = autodiscover_modules(router, f"{APP_PATH}/app")

        self.include_router(router)



app = App()

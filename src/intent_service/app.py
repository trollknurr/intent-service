from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from intent_service.adapter.output.lr_jina_intent_model import LRJinaIntentModel
from intent_service.config import Config
from intent_service.service.intent_service import IntentService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    config = Config()
    infer_model = LRJinaIntentModel(config.MODEL)
    intent_service = IntentService(infer_model)
    app.state.intent_service = intent_service
    yield
    del app.state.intent_service


def build_app() -> FastAPI:
    app = FastAPI(
        title="Intent Service",
        description="A service for intent detection",
        version="0.1.0",
        lifespan=lifespan,
    )

    from intent_service.adapter.input.http_intent_api import router as http_intent_api_router

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"label": "TEXT_EMPTY", "message": '"text" is empty.'})

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=500, content={"label": "INTERNAL_ERROR", "message": str(exc)})

    app.include_router(http_intent_api_router)
    return app


def get_intent_service(req: Request) -> IntentService:
    return req.app.state.intent_service

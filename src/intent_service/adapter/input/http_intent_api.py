from fastapi import APIRouter, Depends, status
from fastapi.responses import PlainTextResponse
from fastapi_utils.cbv import cbv
from pydantic import BaseModel, Field

from intent_service.app import get_intent_service
from intent_service.domain.models import IntentPrediction
from intent_service.port.input.intent import Intent

router = APIRouter()


class IntentRequest(BaseModel):
    text: str = Field(..., description="The text to get the intent for", min_length=1)


class IntentResponse(BaseModel):
    intents: list[IntentPrediction]


@cbv(router)
class HttpIntentAPI(Intent):
    def __init__(self, intent_service: Intent = Depends(get_intent_service)) -> None:
        self.intent_service = intent_service

    @router.post("/intent")
    def get_intent_handler(self, request: IntentRequest) -> IntentResponse:
        return IntentResponse(intents=self.get_intent(request.text))

    def get_intent(self, text: str) -> list[IntentPrediction]:
        return self.intent_service.get_intent(text)

    @router.get(
        "/ready",
        responses={
            200: {"description": "Model is ready", "content": {"text/plain": {"example": "OK"}}},
            423: {"description": "Model is not ready", "content": {"text/plain": {"example": "Not ready"}}},
        },
    )
    def is_model_ready_handler(self) -> PlainTextResponse:
        if self.is_model_ready():
            return PlainTextResponse("OK", status_code=status.HTTP_200_OK)
        return PlainTextResponse("Not ready", status_code=status.HTTP_423_LOCKED)

    def is_model_ready(self) -> bool:
        return self.intent_service.is_model_ready()

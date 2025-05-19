from intent_service.domain.models import IntentPrediction
from intent_service.port.input.intent import Intent
from intent_service.port.output.intent_model import IntentModel


class IntentService(Intent):
    def __init__(self, intent_model: IntentModel) -> None:
        self.intent_model = intent_model

    def get_intent(self, text: str) -> list[IntentPrediction]:
        return self.intent_model.infer(text)

    def is_model_ready(self) -> bool:
        return self.intent_model.is_ready()

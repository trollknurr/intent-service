import abc

from intent_service.domain.models import IntentPrediction


class Intent(abc.ABC):
    @abc.abstractmethod
    def get_intent(self, text: str) -> list[IntentPrediction]:
        pass

    @abc.abstractmethod
    def is_model_ready(self) -> bool:
        pass

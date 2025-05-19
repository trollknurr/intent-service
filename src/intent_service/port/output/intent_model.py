import abc

from intent_service.domain.models import IntentPrediction


class IntentModel(abc.ABC):
    @abc.abstractmethod
    def infer(self, query: str) -> list[IntentPrediction]:
        pass

    @abc.abstractmethod
    def is_ready(self) -> bool:
        pass

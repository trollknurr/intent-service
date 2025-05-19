import pickle

from sklearn.linear_model import LogisticRegression
from transformers import AutoModel

from intent_service.config import ModelConfig
from intent_service.domain.models import IntentPrediction
from intent_service.port.output.intent_model import IntentModel


class LRJinaIntentModel(IntentModel):
    def __init__(self, config: ModelConfig) -> None:
        self.embedder = AutoModel.from_pretrained(config.EMBEDDING_MODEL, trust_remote_code=True)
        self.embedder.to(config.EMBEDDING_DEVICE)
        self.embedder.eval()

        with open(config.LR_PATH, "rb") as f:
            self.lr_model: LogisticRegression = pickle.load(f)

    def infer(self, query: str) -> list[IntentPrediction]:
        vector = self.embedder.encode(query, task="classification")
        probas = self.lr_model.predict_proba([vector])
        return [
            IntentPrediction(label=label, confidence=confidence)
            for label, confidence in zip(self.lr_model.classes_, probas[0])
        ]

    def is_ready(self) -> bool:
        return self.lr_model is not None and self.embedder is not None

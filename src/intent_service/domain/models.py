from pydantic import BaseModel


class IntentPrediction(BaseModel):
    label: str
    confidence: float

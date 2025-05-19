from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    EMBEDDING_MODEL: str = Field(default="./weights/jina-emb")
    EMBEDDING_DEVICE: str = Field(default="cpu")
    LR_PATH: str = Field(default="./weights/lr_jina_model.pkl")


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    ENV: str = Field(default="dev")
    LOG_LEVEL: str = Field(default="INFO")
    MODEL: ModelConfig = Field(default_factory=ModelConfig)

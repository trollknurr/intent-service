from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from intent_service.app import build_app


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return build_app()


@pytest.fixture(scope="session")
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client

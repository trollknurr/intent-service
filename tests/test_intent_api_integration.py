from fastapi import status
from fastapi.testclient import TestClient


def test_empty_text_returns_400(client: TestClient) -> None:
    # Act
    response = client.post("/intent", json={"text": ""})

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"label": "TEXT_EMPTY", "message": '"text" is empty.'}


def test_intent_detection(client: TestClient) -> None:
    # Arrange
    test_text = "What's the weather like today?"

    # Act
    response = client.post("/intent", json={"text": test_text})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "intents" in response_data
    intents = response_data["intents"]
    assert intents
    intent = intents[0]
    assert "label" in intent
    assert "confidence" in intent

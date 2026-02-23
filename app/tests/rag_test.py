import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rag_endpoint_success():
    response = client.post(
        "/rag/rag",
        params={"query": "What are the potential risks?"}
    )
    
    assert response.status_code == 200
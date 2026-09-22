import httpx
import pytest
from fastapi.testclient import TestClient

from app import services
from app.main import app
from app.schemas import LLMAssessment


@pytest.fixture
def client(monkeypatch):
    # Impede chamadas reais caso um teste esqueça de simular o LLM.
    def unexpected_llm_call(trip):
        raise AssertionError("Este teste não deve chamar o LLM.")

    monkeypatch.setattr(
        services, "assess_with_llm", unexpected_llm_call
    )

    with TestClient(app) as test_client:
        yield test_client


def mock_assessment(monkeypatch, policy_ids):
    def fake_assess(trip):
        return LLMAssessment(violated_policy_ids=policy_ids)

    monkeypatch.setattr(services, "assess_with_llm", fake_assess)


def test_approves_valid_trip(client, monkeypatch, valid_payload):
    mock_assessment(monkeypatch, [])

    response = client.post(
        "/travel-requests/evaluate", json=valid_payload
    )

    assert response.status_code == 200
    assert response.json() == {
        "accepted": True,
        "violated_policies": [],
    }


def test_rejects_over_budget(client, monkeypatch, valid_payload):
    valid_payload["estimated_budget"] = "6000.00"
    mock_assessment(monkeypatch, ["POL-002"])

    response = client.post(
        "/travel-requests/evaluate", json=valid_payload
    )

    assert response.status_code == 200
    assert response.json() == {
        "accepted": False,
        "violated_policies": [
            "POL-002: Orçamento total máximo de R$ 5.000,00 excedido."
        ],
    }


def test_reports_all_violations(client, monkeypatch, valid_payload):
    valid_payload.update(
        estimated_budget="6000.00",
        return_date="2026-11-01T09:00:00-03:00",
        destination="Rio de Janeiro",
    )

    # A ordem do LLM pode ser diferente da ordem da política.
    mock_assessment(monkeypatch, ["POL-003", "POL-001", "POL-002"])

    response = client.post(
        "/travel-requests/evaluate", json=valid_payload
    )

    assert response.status_code == 200
    body = response.json()
    assert body["accepted"] is False
    assert [
        message.split(":")[0]
        for message in body["violated_policies"]
    ] == ["POL-001", "POL-002", "POL-003"]


@pytest.mark.parametrize(
    ("budget", "llm_ids"),
    [
        ("6000.00", []),             # LLM deixou passar uma violação.
        ("3500.00", ["POL-002"]),    # LLM inventou uma violação.
    ],
)
def test_disagreement_returns_503(
    client, monkeypatch, valid_payload, budget, llm_ids
):
    valid_payload["estimated_budget"] = budget
    mock_assessment(monkeypatch, llm_ids)

    response = client.post(
        "/travel-requests/evaluate", json=valid_payload
    )

    assert response.status_code == 503
    assert "accepted" not in response.json()


def test_duplicate_rules_return_503(
    client, monkeypatch, valid_payload
):
    valid_payload["estimated_budget"] = "6000.00"
    mock_assessment(monkeypatch, ["POL-002", "POL-002"])

    response = client.post(
        "/travel-requests/evaluate", json=valid_payload
    )

    assert response.status_code == 503
    assert "accepted" not in response.json()


def test_timeout_returns_503(client, monkeypatch, valid_payload):
    def fake_timeout(trip):
        raise httpx.ReadTimeout("Simulated timeout")

    monkeypatch.setattr(services, "assess_with_llm", fake_timeout)

    response = client.post(
        "/travel-requests/evaluate", json=valid_payload
    )

    assert response.status_code == 503
    assert "accepted" not in response.json()
    assert "Simulated timeout" not in response.text


def test_invalid_input_does_not_call_llm(client, valid_payload):
    valid_payload["estimated_budget"] = "-100.00"

    response = client.post(
        "/travel-requests/evaluate", json=valid_payload
    )

    assert response.status_code == 422
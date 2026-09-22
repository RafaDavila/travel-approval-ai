import httpx
from google.genai import errors
from pydantic import ValidationError

from app.llm import assess_with_llm
from app.policy import check_policy
from app.schemas import TravelDecision, TravelRequest


POLICY_MESSAGES = {
    "POL-001": "POL-001: Duração máxima de 15 dias excedida.",
    "POL-002": "POL-002: Orçamento total máximo de R$ 5.000,00 excedido.",
    "POL-003": "POL-003: Origem e destino devem ser diferentes.",
}


class EvaluationUnavailableError(Exception):
    """A avaliação não pôde ser concluída com confiança."""


def evaluate_trip(trip: TravelRequest) -> TravelDecision:
    expected_ids = check_policy(trip)

    try:
        assessment = assess_with_llm(trip)
    except (
        errors.APIError,
        httpx.HTTPError,
        ValidationError,
        RuntimeError,
        OSError,
    ) as exc:
        raise EvaluationUnavailableError(
            "Não foi possível concluir a avaliação. Tente novamente mais tarde."
        ) from exc

    received_ids = assessment.violated_policy_ids

    if len(received_ids) != len(set(received_ids)):
        raise EvaluationUnavailableError(
            "A avaliação retornou regras duplicadas."
        )

    if set(received_ids) != set(expected_ids):
        raise EvaluationUnavailableError(
            "Houve divergência na avaliação. É necessária revisão manual."
        )

    return TravelDecision(
        accepted=not expected_ids,
        violated_policies=[
            POLICY_MESSAGES[policy_id]
            for policy_id in expected_ids
        ],
    )
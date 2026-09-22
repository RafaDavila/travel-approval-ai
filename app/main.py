from fastapi import FastAPI, HTTPException

from app.schemas import TravelDecision, TravelRequest
from app.services import EvaluationUnavailableError, evaluate_trip


app = FastAPI(
    title="Travel Approval AI",
    description=(
        "API para avaliação de solicitações de viagem "
        "com LLM e política fictícia de demonstração."
    ),
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/travel-requests/evaluate",
    response_model=TravelDecision,
    tags=["Travel"],
    responses={
        503: {"description": "Avaliação indisponível ou inconsistente."},
    },
)
def evaluate_travel_request(trip: TravelRequest) -> TravelDecision:
    try:
        return evaluate_trip(trip)
    except EvaluationUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
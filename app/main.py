from fastapi import FastAPI

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
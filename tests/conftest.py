import pytest


@pytest.fixture
def valid_payload():
    return {
        "employee_name": "David Duarte",
        "department": "Financeiro",
        "origin": "Rio de Janeiro",
        "destination": "Recife",
        "departure_date": "2026-10-01T09:00:00-03:00",
        "return_date": "2026-10-05T18:00:00-03:00",
        "estimated_budget": "3500.00",
    }
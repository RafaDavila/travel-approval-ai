import pytest

from app.policy import check_policy
from app.schemas import TravelRequest


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        ({}, []),
        (
            {
                "estimated_budget": "5000.00",
                "return_date": "2026-10-16T09:00:00-03:00",
            },
            [],
        ),
        (
            {"estimated_budget": "5000.01"},
            ["POL-002"],
        ),
        (
            {"return_date": "2026-10-16T09:00:01-03:00"},
            ["POL-001"],
        ),
        (
            {"destination": "  RIO DE JANEIRO  "},
            ["POL-003"],
        ),
        (
            {
                "estimated_budget": "6000.00",
                "return_date": "2026-11-01T09:00:00-03:00",
                "destination": "Rio de Janeiro",
            },
            ["POL-001", "POL-002", "POL-003"],
        ),
        (
            {"return_date": "2026-10-16T12:00:00Z"},
            [],
        ),
    ],
)
def test_check_policy(valid_payload, changes, expected):
    valid_payload.update(changes)
    trip = TravelRequest(**valid_payload)

    assert check_policy(trip) == expected
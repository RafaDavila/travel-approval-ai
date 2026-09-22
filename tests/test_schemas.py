from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas import TravelRequest


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


def test_valid_request(valid_payload):
    trip = TravelRequest(**valid_payload)

    assert trip.estimated_budget == Decimal("3500.00")
    assert trip.departure_date.utcoffset() is not None


def test_strips_whitespace(valid_payload):
    valid_payload["employee_name"] = "  David Duarte  "

    trip = TravelRequest(**valid_payload)

    assert trip.employee_name == "David Duarte"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("employee_name", "   "),
        ("department", ""),
        ("origin", ""),
        ("destination", "   "),
        ("estimated_budget", "0"),
        ("estimated_budget", "-100"),
        ("estimated_budget", "100.123"),
        ("estimated_budget", "NaN"),
        ("estimated_budget", "Infinity"),
        ("departure_date", "data-invalida"),
        ("departure_date", "2026-10-01T09:00:00"),
        ("return_date", "2026-10-05T18:00:00"),
        ("return_date", "2026-10-01T09:00:00-03:00"),
        ("return_date", "2026-09-30T09:00:00-03:00"),
    ],
)
def test_rejects_invalid_values(valid_payload, field, value):
    valid_payload[field] = value

    with pytest.raises(ValidationError):
        TravelRequest(**valid_payload)


def test_rejects_missing_field(valid_payload):
    del valid_payload["destination"]

    with pytest.raises(ValidationError):
        TravelRequest(**valid_payload)


def test_rejects_unknown_field(valid_payload):
    valid_payload["unexpected_field"] = "value"

    with pytest.raises(ValidationError):
        TravelRequest(**valid_payload)


def test_policy_violations_are_not_input_errors(valid_payload):
    valid_payload["estimated_budget"] = "6000.00"
    valid_payload["return_date"] = "2026-11-01T09:00:00-03:00"
    valid_payload["destination"] = valid_payload["origin"]

    trip = TravelRequest(**valid_payload)

    assert trip.estimated_budget == Decimal("6000.00")
    assert trip.origin == trip.destination
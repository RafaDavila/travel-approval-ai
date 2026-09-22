from datetime import UTC, timedelta
from decimal import Decimal

from app.schemas import TravelRequest


MAX_TRIP_DURATION = timedelta(days=15)
MAX_ESTIMATED_BUDGET = Decimal("5000.00")


def check_policy(trip: TravelRequest) -> list[str]:
    violations: list[str] = []

    departure = trip.departure_date.astimezone(UTC)
    return_date = trip.return_date.astimezone(UTC)

    if return_date - departure > MAX_TRIP_DURATION:
        violations.append("POL-001")

    if trip.estimated_budget > MAX_ESTIMATED_BUDGET:
        violations.append("POL-002")

    if trip.origin.strip().casefold() == trip.destination.strip().casefold():
        violations.append("POL-003")

    return violations
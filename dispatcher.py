"""Builder 1 implements the student's policy here.

Policy (POLICY.md / PLAN.md), applied in order:
  1. No eligible car            -> WAIT (Decision(None, reason)).
  2. Exactly one eligible car   -> select it.
  3. Both eligible              -> prefer the car already moving in the request's
                                   direction over an idle car.
  4. Still tied                 -> smaller floor distance abs(floor - request.floor).
  5. Still tied                 -> A (alphabetical ID).
Load is used only through rules.eligible_ids (capacity check).
"""
from models import Elevator, Request, Decision
from rules import eligible_ids, MAX_LOAD_KG, ASSUMED_PASSENGER_KG


def _exclusion_reason(elevator: Elevator, request: Request) -> str:
    """Describe why an elevator was not eligible (explanation only, not selection)."""
    if elevator.load_kg + ASSUMED_PASSENGER_KG > MAX_LOAD_KG:
        return (f"{elevator.id} is full ({elevator.load_kg} kg + {ASSUMED_PASSENGER_KG} kg "
                f"> {MAX_LOAD_KG} kg)")
    if elevator.direction != request.direction:
        return (f"{elevator.id} is moving {elevator.direction}, opposite to the "
                f"{request.direction} call")
    return f"floor {request.floor} is not on {elevator.id}'s remaining {elevator.direction} route"


def choose_elevator(elevators: tuple[Elevator, Elevator], request: Request) -> Decision:
    """Choose one eligible elevator according to POLICY.md; never mutate inputs."""
    eligible = eligible_ids(elevators, request)
    candidates = [e for e in elevators if e.id in eligible]

    # Rule 1: none eligible -> WAIT.
    if not candidates:
        details = "; ".join(_exclusion_reason(e, request) for e in elevators)
        return Decision(None, f"Rule 1: no elevator can serve this call now ({details}). "
                              f"Defer the assignment.")

    # Rule 2: exactly one eligible -> select it.
    if len(candidates) == 1:
        chosen = candidates[0]
        excluded = [e for e in elevators if e.id != chosen.id]
        details = "; ".join(_exclusion_reason(e, request) for e in excluded)
        return Decision(chosen.id, f"Rule 2: {chosen.id} is the only eligible elevator "
                                   f"({details}).")

    # Rule 3: prefer a car already moving in the request's direction over an idle car.
    moving = [e for e in candidates if e.direction == request.direction]
    idle = [e for e in candidates if e.direction == "idle"]
    if len(moving) == 1 and len(idle) == 1:
        chosen, other = moving[0], idle[0]
        return Decision(chosen.id, f"Rule 3: both eligible; {chosen.id} is already moving "
                                   f"{request.direction} with floor {request.floor} on its "
                                   f"remaining route, so it is "
                                   f"preferred over idle {other.id}.")

    # Rule 4: both moving or both idle -> smaller floor distance.
    state = f"moving {request.direction}" if moving else "idle"
    first, second = candidates
    d1 = abs(first.floor - request.floor)
    d2 = abs(second.floor - request.floor)
    if d1 != d2:
        chosen, other = (first, second) if d1 < d2 else (second, first)
        dc, do = min(d1, d2), max(d1, d2)
        return Decision(chosen.id, f"Rule 4: both eligible and both {state}; {chosen.id} is "
                                   f"{dc} floor(s) from floor {request.floor} versus "
                                   f"{other.id}'s {do}.")

    # Rule 5: still tied -> alphabetical ID.
    chosen = min(candidates, key=lambda e: e.id)
    return Decision(chosen.id, f"Rule 5: both eligible, both {state} and both {d1} floor(s) "
                               f"from floor {request.floor}; tie broken alphabetically -> "
                               f"{chosen.id}.")

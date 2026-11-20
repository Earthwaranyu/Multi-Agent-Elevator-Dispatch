# My dispatch policy

Fill in this template yourself before asking the builders to implement it. Short bullets and a small table are enough. You may discuss ideas or ask AI to challenge them, but make and explain your own choices.

## Priorities

- What I prioritise: Using an elevator that is already moving in the caller's direction, so its existing journey is shared and the idle elevator stays free for other calls.
- My exact selection rule: 
  1. If no elevator is eligible → WAIT (Decision(None, reason)).
  2. If only one is eligible → select it.
  3. If both are eligible → prefer the one already moving in the request's direction over an idle one.
  4. If both are still equal (both moving, or both idle) → select the one with the smaller
     floor distance: abs(elevator.floor - request.floor).
- My deterministic tie-breaker: If the distance is also equal → select A (alphabetical ID).
- A tradeoff I accept: The person currently in the elevator may need to stop 1 more time before they go to the destination. For the caller, they need to wait for that elevator one more stop to come.

## Predictions before implementation

Use S1, one of S2/S3, and one valid scenario you create in scenarios.py. For your own case, change something meaningful: location, direction, load or scheduled stops. Name it S6.

| Scenario | My expected selection | Why it follows my policy | Benefit and cost / who is affected |
|---|---|---|---|
| S1 | A | Both eligible; A is moving down past floor 5, B is idle → rule 3 picks A. | Benefit: B stays idle and free. Cost: caller waits for A to come 3 floors instead of B's 1; ~2 passengers in A get an extra stop. |
| S2 | A | Same as S1. A's 325 kg + 65 = 390 ≤ 520, so it is eligible, and my rule does not use load beyond that → rule 3 picks A. | Benefit: B stays free. Cost: about 5 passengers (325/65) are delayed by the extra stop. This is the clearest cost of my policy. |
| S6: both cars moving down | B | Both eligible and both moving down, so rule 3 ties → rule 4: B is 1 floor away, A is 3 → B. | Benefit: caller gets the nearer car, and no idle car is activated. Cost: B's ~3 passengers get an extra stop instead of A's ~2. |

## Another defensible policy

- An alternative priority: Fastest pickup. Always choose the eligible car with the smallest floor distance.
- A scenario where it could choose differently, and why: In S1 it would pick B (1 floor away instead of 3). The caller gets picked up sooner and A's passengers are not delayed, but the idle car is activated.

If your predicted choices contradict your general rule, resolve that before implementation. If review later changes your mind, note the revision in EVIDENCE.md and update the policy and code together.

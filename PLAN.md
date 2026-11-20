# My agent plan

- Dispatcher builder owns dispatcher.py: Implement choose_elevator using rules.eligible_ids and my
  POLICY.md, in this order: 
  
  (1) none eligible → Decision(None, reason) = WAIT;

  (2) one eligible → pick it;

  (3) both eligible → prefer the car already moving in the request's direction over an idle car;

  (4) still tied → smaller floor distance abs(floor - request.floor); 

  (5) still tied → A.

  The reason must say which rule decided. Do not use load except through eligibility. Do not mutate inputs.
- Display builder owns app.py: Implement run_scenarios per SPEC.md R4: for each scenario in order,
  print its name, both elevators' floor/direction/load_kg/stops and the request, call choose_elevator
  exactly once, print "Selected: A", "Selected: B" or "Selected: WAIT" plus the reason, and return
  the decisions as a list. No selection logic in app.py.
- Reviewer is read-only after both outputs are integrated: Check SPEC rules R1–R5, whether the code
  follows my POLICY.md rule order (S1 → A by rule 3, S2 → A by rule 3, S6 → B by rule 4), whether
  the reasons are accurate, and one tradeoff (e.g. S2: ~5 passengers delayed because load is ignored).
- Handoff steps: Use one Claude Code session in elevator_lab with python3 to delegate to two separate
  subagents. Give both builders SPEC.md, POLICY.md, PLAN.md, AGENTS.md and all Python files. Wait for
  both, inspect git diff (only dispatcher.py and app.py should change), run the tests, then start a
  separate reviewer session.
- Final check: Run python3 -m unittest -v (expect 6 OK) and python3 app.py, and compare the S1, S2
  and S6 selections and reasons with my predictions (A, A, B). Record results in EVIDENCE.md and
  investigate any mismatch before changing code or policy.

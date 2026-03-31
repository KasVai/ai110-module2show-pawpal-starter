# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling Features

The PawPal+ scheduler goes beyond simple task tracking with intelligent scheduling capabilities:

- **Priority-Based Ranking**: Tasks are ranked by priority level (high → medium → low), ensuring critical pet care tasks are scheduled first
- **Task Sorting & Filtering**: Sort tasks by duration (ascending/descending) or filter by specific pet to organize the daily plan
- **Recurring Task Auto-Recurrence**: Tasks automatically regenerate with updated due dates when marked complete, eliminating manual re-entry for daily/weekly care routines
- **Time Conflict Detection**: Identifies when multiple tasks are scheduled at overlapping times for the same or different pets, with warnings to prevent booking conflicts
- **Due Date Tracking**: Each task tracks a specific due date using Python's `datetime` and `timedelta` for accurate multi-day planning
- **Greedy Schedule Generation**: Fills the available time window by prioritizing high-value tasks first, maximizing care coverage within realistic daily constraints

Example: If a dog needs a 20-minute morning walk and 15-minute feeding, both flagged as high-priority, the scheduler ranks the walk first. If a cat also needs a 10-minute feeding at the same time, a conflict warning alerts the owner to reschedule.

Testing PawPal+: 
- Command to run tests: python -m pytest

Description of what tests cover: 
- Completion and addition of tasks 
- Sorting correctness 
- Dealing with recurrences 
- Detecting conflicts within tasks 
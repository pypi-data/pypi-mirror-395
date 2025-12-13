<p align="center">
  <img src="https://raw.githubusercontent.com/Versailles-Information-Systems/trellis-process/main/trellis-logo.png" alt="trellis logo" width="400">
</p>

# trellis-process

_A lightweight process tracker for long-running, distributed workflows._

`trellis-process` gives you a small, reusable **Process / ProcessStep** domain model
you can use to track business workflows across services and bounded contexts.

It works great for:

- High-level journeys (e.g. **referral lifecycle**)
- Sub-processes (e.g. **authorization flow** or **notification delivery**)
- Any long-running process where multiple steps must eventually complete
- Operations that need **timeout and retry** handling

Trellis is intentionally **storage-agnostic**: you bring your own database
(PostgreSQL, DynamoDB, etc.) and wire it via a repository interface. The core
library focuses on the **domain model** and invariants.

---

## Features

- ✅ Generic `Process` + `ProcessStep` model
- ✅ **Step-level timeout and retry** support (based on Vaughn Vernon's pattern)
- ✅ Supports multiple `process_type`s (e.g. `"ReferralJourney"`, `"ClaimAdjudication"`)
- ✅ Tracks required steps, state (`pending`, `in_progress`, `completed`, `failed`)
- ✅ Simple API: `start_step`, `complete_step`, `fail_step`
- ✅ `TimeoutCheckerService` for automatic timeout detection
- ✅ Storage-agnostic: integrate with Postgres, DynamoDB, etc.
- ✅ In-memory repositories for demos and unit tests

---

## Installation

```bash
pip install trellis-process
```

With DynamoDB support:
```bash
pip install trellis-process[dynamodb]
```

---

## Quick Start

### Basic Process Tracking

```python
from trellis_process import Process, ProcessStep, ProcessService
from trellis_process import InMemoryProcessRepository

repo = InMemoryProcessRepository()
service = ProcessService(repo)

# Create a process with steps
process = service.start_process(
    tenant_id="tenant-1",
    process_type="ReferralNotification",
    aggregate_type="Referral",
    aggregate_id="ref-123",
    steps=[
        ProcessStep(name="send_email"),
        ProcessStep(name="send_in_app"),
    ],
)

# Mark steps as completed
service.complete_step(process, "send_email")
service.complete_step(process, "send_in_app")

assert process.is_completed()
```

### With Timeout and Retry

```python
from trellis_process import (
    Process, ProcessStep, ProcessService,
    TimeoutCheckerService, ProcessStepTimedOut,
    InMemoryProcessRepository, InMemoryStepTrackerRepository,
)

process_repo = InMemoryProcessRepository()
tracker_repo = InMemoryStepTrackerRepository()
service = ProcessService(process_repo, tracker_repo)

# Create process with timeout-enabled steps
process = service.start_process(
    tenant_id="tenant-1",
    process_type="CaseCreation",
    aggregate_type="Referral",
    aggregate_id="ref-123",
    steps=[
        ProcessStep(name="create_case", timeout_ms=30000, retries_permitted=3),
    ],
)

# Start the step (creates tracker)
service.start_step(process, "create_case")

# Set up timeout checker (run on a schedule)
def handle_timeout(event: ProcessStepTimedOut):
    if event.has_fully_timed_out():
        service.fail_step(process, event.step_name, "Max retries exceeded")
    else:
        # Retry the operation
        retry_create_case(process)

checker = TimeoutCheckerService(tracker_repo, handle_timeout)

# Run periodically (e.g., every 30 seconds)
checker.check_for_timed_out_steps()
```

---

## Architecture

```
Process (container)
├── ProcessStep: "send_email"     → StepTracker (timeout=30s, retries=3)
├── ProcessStep: "send_in_app"    → StepTracker (timeout=10s, retries=2)
└── ProcessStep: "create_case"    → StepTracker (timeout=60s, retries=5)
```

- **Process**: Container for steps, tracks overall state
- **ProcessStep**: Individual step with optional timeout config
- **StepTracker**: Infrastructure object that monitors timeout and retry state
- **TimeoutCheckerService**: Scans for timed-out trackers, publishes events

---

## API Reference

### ProcessStep

```python
ProcessStep(
    name="step_name",
    timeout_ms=30000,        # Optional: timeout per attempt (ms)
    retries_permitted=3,     # Optional: number of retries
)
```

### Process

```python
process = Process.start(
    tenant_id="tenant-1",
    process_type="MyWorkflow",
    aggregate_type="MyAggregate",
    aggregate_id="id-123",
    steps=[...],
)

process.start_step("step_name")      # Returns StepTracker if timeout configured
process.complete_step("step_name")
process.fail_step("step_name", "error message")
process.is_completed()
process.has_failed()
```

### ProcessService

```python
service = ProcessService(process_repo, tracker_repo)  # tracker_repo optional

service.start_process(...)
service.start_step(process, "step_name")
service.complete_step(process, "step_name")
service.fail_step(process, "step_name", "error")
```

### TimeoutCheckerService

```python
checker = TimeoutCheckerService(tracker_repo, publish_event)
checker.check_for_timed_out_steps()  # Run on schedule
```

---

## License

MIT

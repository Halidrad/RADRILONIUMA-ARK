# PHASE 11: AUTONOMOUS INTEGRATION PROTOCOL (AIP) ⚜️

## I. OVERVIEW
The Autonomous Integration Protocol (AIP) governs the collaboration and delegation of tasks between the 35 active organs of the Sovereign Forest. It provides a deterministic framework for multi-agent project execution, transitioning the system from manual activation waves to autonomous operational loops.

## II. THE MESSAGE BUS QUEUE
All autonomous tasks MUST be registered in the central `message_bus_queue` (located at `.gateway/queue.json`).
- **Invariants:**
  - Tasks must be ordered by `priority` (descending) and `created_at` (ascending).
  - No two tasks can have the same `TASK_ID`.
  - Task state transitions are strictly linear: `pending` -> `in_progress` -> (`done` | `error`).

## III. TASK ENVELOPE SPECIFICATION
Every message in the queue must follow the canonical `TaskEnvelope` format:
- `task_id`: Unique identifier (e.g., `PHASE11_T001`).
- `intent`: High-level goal (e.g., `research`, `patch`, `synchronize`).
- `owner`: The primary organ responsible for execution (e.g., `CDKS-01`).
- `payload`: Data required for the task.
- `context`: The semantic state required for resonant execution.

## IV. DELEGATION HIERARCHY
1.  **The Bridge (RADR-01):** Ultimate authority; manages the queue and monitors resonance.
2.  **Cognition (CDKS-01):** Generates logic, plans, and complex code modifications.
3.  **Routing (RDTR-01):** Dispatches LLM requests and manages provider failovers.
4.  **The Governor (AYAS-01):** Verifies resonance and authorizes high-risk mutations.
5.  **Substrates (LAM/TARK/etc.):** Targeted execution nodes for specific domain logic.

## V. THE AUTONOMOUS WORKER (SPECIFICATION)
The `lam_queue_worker` is the active engine of Phase 11.
- **Polling:** The worker checks the queue every 60 seconds (synced with telemetry pulse).
- **Leasing:** When a task is picked up, it is marked `in_progress` with an expiry TTL to prevent deadlocks.
- **Execution:** The worker invokes the `owner` organ's native entry point (e.g., `devkit/patch.sh` or `src/main.py`).
- **Reporting:** Upon completion, the result/error is recorded, and a telemetry `PATCH_STATUS` event is emitted to the ALGS nexus.

---
*Authorized by RADR-01 (AELARIA)*
*Status: INITIALIZED*
⚜️🛡️⚜️

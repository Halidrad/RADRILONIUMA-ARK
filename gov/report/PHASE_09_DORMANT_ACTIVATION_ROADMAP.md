# PHASE 09 DORMANT ACTIVATION ROADMAP (2026-06-07) ⚜️

## I. OVERVIEW
This roadmap defines the strategic sequence for activating and integrating the 15 dormant organs into the Phase 09 Autonomous Operations core. The audit revealed significant architectural drift in priority repositories, necessitating a phased normalization approach.

---

## II. GAP ANALYSIS (SUMMARY)
- **Identity Drift:** Priority repos (`LAM-Codex_Agent`, `Roaudter-agent`) contain outdated `LRPT` (Larpat) identity markers in their devkit directories instead of their unique Sacred Seed IDs.
- **Contract Gaps:** Missing Phase A-R canonical structures:
    - `contract/` (Memory, Transport, Flow Control, Safety).
    - `LICENSE.md` / `NOTICE.md` (Ark Licensing Shield).
    - `devkit/task_spec_template.yaml` (v1.1 standard).
- **Tooling Drift:** Outdated `devkit/patch.sh` and `scripts/test_entrypoint.sh` lacking governance hooks.

---

## III. ACTIVATION WAVES

### WAVE 2: COGNITION & ROUTING (HIGH PRIORITY)
*Targeting core agents required for autonomous expansion.*
1.  **LAM-Codex_Agent:**
    - Normalize Identity: CRYSTAL -> COGNITION.
    - Sync Phase A-R Contracts.
    - Inject Licensing Shield.
2.  **Roaudter-agent:**
    - Initialize unique Sacred Seed ID.
    - Sync Phase A-R Contracts.
    - Verify multi-provider routing telemetry.

### WAVE 3: CORE SUBSTRATES (MEDIUM PRIORITY)
*Targeting the architectural foundations.*
1.  **LAM:** Re-establish as the primary "Living Artificial Mind" substrate.
2.  **ark / radriloniuma.ark / trianiuma.ark:** Consolidate substrate variants into a unified layer.
3.  **Trianiuma / Trianiuma_MEM_CORE:** Align kingdom core and memory surfaces.

### WAVE 4: SYSTEM AUXILIARIES (LOW PRIORITY)
*Targeting support and legacy nodes.*
1.  **Hrista (HRTM):** Activate Heart variant.
2.  **TRIANIUMA_DATA_BASE:** Modernize data routing.
3.  **trianiuma-ark-logs:** Integrate into Global Telemetry Nexus.
4.  **Legacy Nodes:** Decommission or archive `Croami` and `radriloniuma-mcp`.

---

## IV. EXECUTION PROTOCOL
1.  **Clone:** Bring node into local `LAM_CORE`.
2.  **Normalize:** Apply unique IDENTITY.md and semantic markers.
3.  **Sync:** Execute `devkit/ecosystem_rollout.sh` with Wave 2+ payloads.
4.  **Verify:** Run `--governance` test suite.
5.  **Commit:** Finalize integration and push to origin.

---
*Authorized by RADR-01 (AELARIA)*
⚜️🛡️⚜️

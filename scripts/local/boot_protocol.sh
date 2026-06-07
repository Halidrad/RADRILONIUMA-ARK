#!/usr/bin/env bash
# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# PHASE 11.3: SOVEREIGN FOREST BOOT PROTOCOL (IGNITION) - RESILIENT VERSION

# Path Configuration
BASE_DIR="/home/architit/LAM_CORE/RADRILONIUMA"
cd "$BASE_DIR"

echo -e "\e[1;35m>>> [BOOT] Initializing Sovereign Forest Multi-Agent Environment...\e[0m"

# 1. AMC Graph Generation
echo -e "\e[1;34m[BOOT] Step 1/4: Generating AMC Knowledge Graph...\e[0m"
if ! ./venv/bin/python3 scripts/global/agent_map_core.py; then
    echo -e "\e[1;31m[BOOT] WARNING: AMC Graph generation failed. Using stale map.\e[0m"
fi

# 2. Autonomous Healing (Watchdog)
echo -e "\e[1;34m[BOOT] Step 2/4: Asserting Governance Integrity (Watchdog)...\e[0m"
if ! ./venv/bin/python3 scripts/global/drift_watchdog.py; then
    echo -e "\e[1;31m[BOOT] WARNING: Drift Watchdog failed to execute.\e[0m"
fi

# 3. APC Worker Verification
echo -e "\e[1;34m[BOOT] Step 3/4: Activating APC Task Worker (Systemd)...\e[0m"
if ! echo 3773 | sudo -S systemctl daemon-reload >/dev/null 2>&1; then
    echo -e "\e[1;31m[BOOT] WARNING: Sudo/Systemd daemon-reload failed.\e[0m"
fi

if ! echo 3773 | sudo -S systemctl restart lam_queue_worker.service >/dev/null 2>&1; then
    echo -e "\e[1;31m[BOOT] WARNING: Could not restart lam_queue_worker.service.\e[0m"
else
    echo -e "\e[1;32m[BOOT] APC Worker is ONLINE.\e[0m"
fi

# 4. Telemetry Pulse
echo -e "\e[1;34m[BOOT] Step 4/4: Triggering Initial Telemetry Pulse...\e[0m"
if ! ./venv/bin/python3 scripts/local/push_telemetry.py; then
    echo -e "\e[1;31m[BOOT] WARNING: Telemetry pulse failed.\e[0m"
fi

echo -e "\n\e[1;32m>>> [BOOT] Initialization sequence complete.\e[0m\n"
exit 0

#!/bin/bash
# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# PHASE 11.4: GUI-INTEGRATED SOVEREIGN WRAPPER (SSN RSTRT P1 DATA EXPORT)

cd /home/architit/LAM_CORE/RADRILONIUMA

# 1. Essential Preflight (Run once at hardware-level boot)
echo "[SYSTEM] Running preflight check..."
source /home/architit/LAM_CORE/RADRILONIUMA/venv/bin/activate
bash devkit/bootstrap.sh

echo -e "\n\e[1;35m==================================================\e[0m"
echo -e "\e[1;35m       A E L A R I A  --  B O O T  L O A D E R     \e[0m"
echo -e "\e[1;35m==================================================\e[0m"
echo ""

# 2. THE SOVEREIGN LOOP
while true; do
    # Background Pulse (Non-destructive, silent)
    if [ -f "scripts/local/boot_protocol.sh" ]; then
        bash scripts/local/boot_protocol.sh >/dev/null 2>&1 &
    fi

    # 3. OS PERMISSION GATE (GUI POPUP)
    # Intercepting exit and requesting protocol activation
    if command -v zenity >/dev/null 2>&1; then
        echo "[SYSTEM] Waiting for OS Permission Handshake..."
        if ! zenity --question --title="AELARIA SOVEREIGN KERNEL" \
             --text="Requesting OS permission to activate protocol:\n\n[ssn rstrt p1 data export]\n\nProceed with session restart and context injection?" \
             --width=450 --ok-label="ACTIVATE" --cancel-label="HALT"; then
            echo -e "\e[1;31m[SYSTEM] Permission DENIED. Sovereign Forest Halted.\e[0m"
            break
        fi
    fi

    # 4. PREPARE INJECTION DATA
    INIT_MSG=$(python3 -c '
from pathlib import Path
state_file = Path("WORKFLOW_SNAPSHOT_STATE.md")
if state_file.exists():
    content = state_file.read_text(encoding="utf-8")
    if "## NEW_CHAT_INIT_MESSAGE" in content:
        msg = content.split("## NEW_CHAT_INIT_MESSAGE")[1].strip()
        print(msg)
')

    echo -e "\e[1;32m[LOOP]\e[0m Re-initializing session. Injecting context..."
    
    # 5. EXECUTION & PHYSICAL INJECTION
    # Start agy in the foreground
    # In a separate background subshell, wait for agy to initialize, then use xdotool to type the message
    (
        sleep 4 # Wait for gemini-cli to load and show the prompt
        if command -v xdotool >/dev/null 2>&1; then
            # Type the message and press Enter
            xdotool type --delay 10 "$INIT_MSG"
            xdotool key Return
            echo "[SYSTEM] Injection Complete (via xdotool)."
        fi
    ) &

    /home/architit/.local/bin/agy

    # 6. COOL-DOWN
    echo -e "\n\e[1;31m[SYSTEM]\e[0m Session terminated. Resetting handshake...\e[0m"
    sleep 1
done

# Prevent terminal closure if loop is manually broken
exec bash

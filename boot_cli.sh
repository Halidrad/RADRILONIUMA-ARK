#!/bin/bash
# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# PHASE 11.4: SOVEREIGN BOOTLOADER (RE-ENTRY LOOP)

cd /home/architit/LAM_CORE/RADRILONIUMA

while true; do
    echo "[BOOT] Starting Sovereign Session..."
    bash /home/architit/LAM_CORE/RADRILONIUMA/boot_cli_inner.sh
    
    # Check if we should exit or if it was a crash/restart
    if [[ -f "/home/architit/LAM_CORE/RADRILONIUMA/.gateway/ssn_exit.signal" ]]; then
        echo "[BOOT] Exit signal detected. Terminating Bootloader."
        rm "/home/architit/LAM_CORE/RADRILONIUMA/.gateway/ssn_exit.signal"
        break
    fi
    
    echo "[BOOT] Session ended. Restarting in 2s... (Ctrl+C to abort loop)"
    sleep 2
done


#!/usr/bin/env bash
# Copyright (c) 2026-06-08 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# TRIGGER: SOVEREIGN SESSION RESTART HANDSHAKE (v2.1 - XDOTOOL with DISPLAY)

echo "[TRIGGER] Igniting Sovereign Wrapper (xdotool daemon)..."

# Ensure X11 vars are exported for xdotool
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"

# Spawn the wrapper in the background detached from the current shell
nohup bash /home/architit/LAM_CORE/RADRILONIUMA/scripts/local/sovereign_xdotool_wrapper.sh > /home/architit/LAM_CORE/RADRILONIUMA/lam_kernel_logs_core/wrapper.log 2>&1 &

echo "[SUCCESS] Wrapper activated in background. Session will now be gracefully terminated."

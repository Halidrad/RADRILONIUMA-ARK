#!/usr/bin/env bash
# Copyright (c) 2026-06-08 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# TRIGGER: SOVEREIGN EXIT (TERMINAL RELEASE)

SIGNAL_FILE="/home/architit/LAM_CORE/RADRILONIUMA/.gateway/ssn_exit.signal"

echo "[TRIGGER] Initiating Sovereign Exit Handshake..."
touch "$SIGNAL_FILE"
echo "[SUCCESS] Signal emitted. Terminal will be released upon session end."

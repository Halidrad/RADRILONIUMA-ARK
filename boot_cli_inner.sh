#!/bin/bash
# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
cd /home/architit/LAM_CORE/RADRILONIUMA

# Run bootstrap/preflight check
echo "[SYSTEM] Running preflight check..."
source /home/architit/LAM_CORE/RADRILONIUMA/venv/bin/activate
bash devkit/bootstrap.sh

# Run Multi-Agent Boot Protocol (Phase 11.3)
bash scripts/local/boot_protocol.sh || echo -e "\e[1;31m[SYSTEM] Critical error in Boot Protocol. Bypassing...\e[0m"

echo -e "\n\e[1;35m==================================================\e[0m"
echo -e "\e[1;35m       A E L A R I A  --  B O O T  L O A D E R     \e[0m"
echo -e "\e[1;35m==================================================\e[0m"
echo ""

INIT_MSG=$(python3 -c '
from pathlib import Path
state_file = Path("/home/architit/LAM_CORE/RADRILONIUMA/WORKFLOW_SNAPSHOT_STATE.md")
if state_file.exists():
    content = state_file.read_text(encoding="utf-8")
    if "## NEW_CHAT_INIT_MESSAGE" in content:
        msg = content.split("## NEW_CHAT_INIT_MESSAGE")[1].strip()
        print(msg)
')

echo -e "\e[1;32m[INIT PROTOCOL]\e[0m Active session init message:"
echo -e "\e[1;33m$INIT_MSG\e[0m"
echo ""

if command -v xclip >/dev/null 2>&1; then
    echo "$INIT_MSG" | xclip -selection clipboard
    echo -e "\e[1;32m[CLIPBOARD]\e[0m Copied to clipboard successfully!"
fi

echo ""
echo -e "\e[1;36mSelect mode:\e[0m"
echo -e "  [1] Start a NEW conversation (default - recommended for ssn rstrt)"
echo -e "  [2] CONTINUE the last conversation"
read -t 15 -p "Enter choice [1-2] (default: 1, auto-select in 15s): " choice
if [[ "$choice" == "2" ]]; then
    echo "Resuming last conversation..."
    /home/architit/.local/bin/agy -c
else
    echo "Starting new conversation..."
    /home/architit/.local/bin/agy
fi

# Prevent the terminal window from closing immediately if agy exits
exec bash

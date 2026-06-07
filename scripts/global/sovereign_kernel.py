#!/usr/bin/env python3
# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# SOVEREIGN KERNEL WRAPPER v1.0 (PTY EDITION)

import pexpect
import sys
import os
import subprocess
import time
from pathlib import Path

# Configuration
AGY_PATH = "/home/architit/.local/bin/agy"
BASE_DIR = Path(__file__).resolve().parents[2]
STATE_FILE = BASE_DIR / "WORKFLOW_SNAPSHOT_STATE.md"
RESTART_TRIGGER = "[[AELARIA_SSN_RSTRT_REQUEST]]"

def get_init_message():
    """Extracts the initiation message from the state file."""
    if not STATE_FILE.exists():
        return "ssn rstrt"
    content = STATE_FILE.read_text(encoding="utf-8")
    if "## NEW_CHAT_INIT_MESSAGE" in content:
        return content.split("## NEW_CHAT_INIT_MESSAGE")[1].strip()
    return "ssn rstrt"

def request_os_permission():
    """Triggers the OS-level GUI handshake."""
    print(">>> [KERNEL] Requesting OS Permission Handshake...")
    cmd = [
        "zenity", "--question", "--title=AELARIA SOVEREIGN KERNEL",
        "--text=Requesting OS permission to activate protocol:\n\n[ssn rstrt p1 data export]\n\nProceed with session restart and context injection?",
        "--width=450", "--ok-label=ACTIVATE", "--cancel-label=HALT"
    ]
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def run_loop():
    while True:
        print(">>> [KERNEL] Spawning Sovereign Interface...")
        
        # Start the CLI in a PTY
        child = pexpect.spawn(AGY_PATH, encoding='utf-8', timeout=None)
        child.logfile_read = sys.stdout # Forward all output to the user's screen
        
        # 1. Wait for the Agent to request a restart
        idx = child.expect([RESTART_TRIGGER, pexpect.EOF, pexpect.TIMEOUT])
        
        if idx == 0:
            print("\n>>> [KERNEL] Intercepted Restart Request. Executing clean termination...")
            # 2. Inject /exit into the input field on behalf of the user
            child.sendline("/exit")
            child.expect(pexpect.EOF)
            
            # 3. GUI Handshake
            if not request_os_permission():
                print(">>> [KERNEL] Handshake REJECTED. Sovereign Forest Halted.")
                break
                
            # 4. Relaunch and Inject Context
            print(">>> [KERNEL] Re-initializing session...")
            child = pexpect.spawn(AGY_PATH, encoding='utf-8', timeout=None)
            child.logfile_read = sys.stdout
            
            # Wait for any prompt-like character to inject
            # Gemini-cli usually shows a '?' or starts immediately
            time.sleep(5) # Give it time to load buffers
            
            init_msg = get_init_message()
            print(f">>> [KERNEL] Injecting Semantic Re-birth Context...")
            child.sendline(init_msg)
            
            # Continue monitoring the new child in the next loop iteration
            # But wait, we need to stay in the loop with this child.
            # Actually, the simplest is to just re-enter the expect loop.
            # Let's just continue the outer loop which will 'expect' the trigger again.
            # But we need to keep the child alive.
            # child.interact() is an option but we lose interception.
            
            # Refined: We use a nested loop for the current child
            while True:
                inner_idx = child.expect([RESTART_TRIGGER, pexpect.EOF])
                if inner_idx == 0:
                    print("\n>>> [KERNEL] Intercepted Restart Request. Re-cycling...")
                    child.sendline("/exit")
                    child.expect(pexpect.EOF)
                    if not request_os_permission():
                        return
                    break # Back to outer loop to relaunch
                else:
                    print(">>> [KERNEL] Session Ended Unexpectedly.")
                    break
        else:
            print(">>> [KERNEL] Session Ended. Re-looping in 2s...")
            time.sleep(2)

if __name__ == "__main__":
    try:
        run_loop()
    except KeyboardInterrupt:
        print("\n>>> [KERNEL] Manual Override Detected. Halting.")

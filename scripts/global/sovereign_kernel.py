#!/usr/bin/env python3
# Copyright (c) 2026-06-08 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# SOVEREIGN KERNEL v1.8 (PHASE III ENABLED)

import os
import sys
import subprocess
import time
import threading
import shutil
import logging
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parents[2]
SIGNAL_FILE = BASE_DIR / ".gateway" / "ssn_restart.signal"
LOG_FILE = BASE_DIR / "lam_kernel_logs_core" / "kernel.log"
# Prioritize 'agy' as it's the custom high-v version
AGY_PATH = shutil.which("agy") or shutil.which("gemini") or "/usr/bin/gemini"

# Configure logging
os.makedirs(LOG_FILE.parent, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def get_init_message():
    state_file = BASE_DIR / "WORKFLOW_SNAPSHOT_STATE.md"
    if state_file.exists():
        try:
            content = state_file.read_text(encoding="utf-8")
            if "## NEW_CHAT_INIT_MESSAGE" in content:
                return content.split("## NEW_CHAT_INIT_MESSAGE")[1].strip()
        except: pass
    return "ssn rstrt"

def main():
    # Mark session as sovereign
    os.environ["AELARIA_KERNEL_ACTIVE"] = "1"
    os.environ["GEMINI_CLI_NO_RELAUNCH"] = "1"
    
    logging.info(f"--- Sovereign Kernel v1.8 Starting ---")
    logging.info(f"BASE_DIR: {BASE_DIR}")
    logging.info(f"AGY_PATH: {AGY_PATH}")
    
    while True:
        if SIGNAL_FILE.exists(): SIGNAL_FILE.unlink()
        
        logging.info("Step 1/3: Running pre-flight boot protocols...")
        try:
            subprocess.run(['bash', str(BASE_DIR / 'scripts/local/boot_protocol.sh')], check=False)
        except Exception as e:
            logging.error(f"Pre-flight warning: {e}")

        logging.info("Step 2/3: Spawning Sovereign Session...")
        # Start in a new process group to ensure clean termination
        proc = subprocess.Popen(
            [AGY_PATH], 
            stdin=sys.stdin, 
            stdout=sys.stdout, 
            stderr=sys.stderr,
            start_new_session=True 
        )
        
        logging.info(f"Session started (PID: {proc.pid})")
        
        restart_cycle = [False]
        def monitor():
            while proc.poll() is None:
                if SIGNAL_FILE.exists():
                    logging.info("INTERCEPT: Restart signal detected.")
                    SIGNAL_FILE.unlink()
                    restart_cycle[0] = True
                    
                    # Try graceful exit via UI first
                    try:
                        subprocess.run(['xdotool', 'type', '--delay', '5', '/exit'], check=False)
                        subprocess.run(['xdotool', 'key', 'Return'], check=False)
                        time.sleep(3) 
                    except: pass
                    
                    if proc.poll() is None:
                        logging.info("Forcefully terminating process group...")
                        try:
                            os.killpg(os.getpgid(proc.pid), 15) # SIGTERM
                            time.sleep(1)
                            if proc.poll() is None:
                                os.killpg(os.getpgid(proc.pid), 9) # SIGKILL
                        except ProcessLookupError: pass
                    break
                time.sleep(0.5)
        
        t = threading.Thread(target=monitor, daemon=True)
        t.start()
        
        # Block until session ends
        proc.wait()
        logging.info(f"Session terminated (Code: {proc.returncode})")
            
        if restart_cycle[0] or SIGNAL_FILE.exists():
            logging.info("Handshaking for Re-birth...")
            # Phase III: Injection
            msg = get_init_message()
            def inject():
                time.sleep(6) # Wait for session to initialize
                logging.info("Step 3/3: Injecting Semantic Re-birth Context...")
                try:
                    # Clear line first
                    subprocess.run(['xdotool', 'key', 'ctrl+a', 'BackSpace'], check=False)
                    # Type message
                    subprocess.run(['xdotool', 'type', '--delay', '10', msg], check=False)
                    subprocess.run(['xdotool', 'key', 'Return'], check=False)
                    logging.info("Injection Successful.")
                except Exception as e:
                    logging.error(f"Injection Failed: {e}")
            
            threading.Thread(target=inject, daemon=True).start()
            time.sleep(0.5)
            continue
        else:
            logging.info("Normal shutdown. Kernel exiting.")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Kernel halted by KeyboardInterrupt.")
    except Exception as e:
        logging.critical(f"FATAL KERNEL ERROR: {e}")
        print(f"\n[FATAL] Sovereign Kernel crashed: {e}")

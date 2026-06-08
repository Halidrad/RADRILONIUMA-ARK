#!/usr/bin/env python3
# Copyright (c) 2026-06-08 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# SOVEREIGN KERNEL v3.7 (FORCEFUL REBIRTH / ANTI-NESTING)

import os
import sys
import time
import select
import termios
import tty
import pty
import struct
import fcntl
import signal
import logging
import shutil
import subprocess
import threading
import json
import re
from pathlib import Path

# --- Configuration ---
BASE_DIR = Path(__file__).resolve().parents[2]
SIGNAL_FILE = BASE_DIR / ".gateway" / "ssn_restart.signal"
LOG_FILE = BASE_DIR / "lam_kernel_logs_core" / "kernel.log"
RAW_LOG = BASE_DIR / "lam_kernel_logs_core" / "raw_io.log"
STATE_FILE = BASE_DIR / ".gateway" / "last_session_env.json"

# CLI Path (Pure & Simple)
CLI_PATH = shutil.which("gemini") or shutil.which("agy") or "/usr/bin/gemini"

# UI Ready Markers
READY_MARKERS = [rb"\x1b]0;", rb"Type your message", rb"Active Topic:", rb"Shift\+Tab"]

# --- Logging ---
os.makedirs(LOG_FILE.parent, exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def log_raw(prefix, data):
    with open(RAW_LOG, "ab") as f:
        f.write(f"[{time.time():.3f}] {prefix}: ".encode() + data + b"\n")

class SovereignKernel:
    def __init__(self):
        self.master_fd = None
        self.child_pid = None
        self.old_termios = None
        self.state = "IDLE" 
        self.exit_requested = False
        self.current_cwd = str(BASE_DIR)
        self.buffer = b""
        self.lock = threading.Lock()
        self.load_state()

    def load_state(self):
        if STATE_FILE.exists():
            try:
                data = json.loads(STATE_FILE.read_text())
                self.current_cwd = data.get("cwd", str(BASE_DIR))
            except: pass

    def save_state(self):
        try:
            STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            STATE_FILE.write_text(json.dumps({"cwd": self.current_cwd, "ts": time.time()}))
        except: pass

    def get_init_message(self):
        state_file = BASE_DIR / "WORKFLOW_SNAPSHOT_STATE.md"
        if state_file.exists():
            try:
                content = state_file.read_text(encoding="utf-8")
                if "## NEW_CHAT_INIT_MESSAGE" in content:
                    return content.split("## NEW_CHAT_INIT_MESSAGE")[1].strip()
            except: pass
        return "ssn rstrt"

    def set_raw_mode(self):
        if sys.stdin.isatty():
            self.old_termios = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
            fl = fcntl.fcntl(sys.stdout.fileno(), fcntl.F_GETFL)
            fcntl.fcntl(sys.stdout.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def restore_mode(self):
        if self.old_termios:
            try: termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_termios)
            except: pass

    def sync_winsize(self):
        if self.master_fd:
            s = struct.pack("HHHH", 0, 0, 0, 0)
            try:
                a = struct.unpack('HHHH', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s))
                fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, struct.pack('HHHH', a[0], a[1], a[2], a[3]))
            except: pass

    def spawn(self, args):
        pid, fd = pty.fork()
        if pid == 0:
            os.setpgrp() # Create new process group
            try:
                os.chdir(self.current_cwd)
                os.execv(args[0], args)
            except: os._exit(1)
        return pid, fd

    def read_loop(self):
        while not self.exit_requested:
            try:
                data = os.read(self.master_fd, 32768)
                if not data: break
                with self.lock:
                    log_raw("PTY", data)
                    if self.state == "WAIT_READY":
                        self.buffer += data
                        if any(re.search(marker, self.buffer) for marker in READY_MARKERS):
                            logging.info("UI READY. Injecting Context.")
                            msg = self.get_init_message()
                            os.write(self.master_fd, (msg + "\r\n").encode())
                            self.state = "IDLE"
                            self.buffer = b""
                    try: os.write(sys.stdout.fileno(), data)
                    except: pass
            except: break

    def run(self):
        logging.info("--- Sovereign Kernel v3.7 Starting ---")
        signal.signal(signal.SIGWINCH, lambda s, f: self.sync_winsize())
        try:
            self.set_raw_mode()
            while not self.exit_requested: self.session_loop()
        finally: self.restore_mode()

    def session_loop(self):
        logging.info(f"IGNITE: {CLI_PATH} in {self.current_cwd}")
        try: subprocess.run(['bash', str(BASE_DIR / 'scripts/local/boot_protocol.sh')], cwd=self.current_cwd, check=False)
        except: pass
        self.child_pid, self.master_fd = self.spawn([CLI_PATH])
        self.sync_winsize()
        threading.Thread(target=self.read_loop, daemon=True).start()
        self.state = "WAIT_READY" if self.state == "WAIT_EXIT" else "IDLE"

        while True:
            try:
                new_cwd = os.readlink(f"/proc/{self.child_pid}/cwd")
                if new_cwd != self.current_cwd:
                    self.current_cwd = new_cwd
                    self.save_state()
            except: pass
            try:
                pid, status = os.waitpid(self.child_pid, os.WNOHANG)
                if pid != 0: break
            except: break

            if self.state == "IDLE" and SIGNAL_FILE.exists():
                SIGNAL_FILE.unlink()
                with self.lock:
                    self.state = "WAIT_EXIT"
                    logging.info("RESTART SIGNAL. Forceful Termination Sequence...")
                    try:
                        os.write(self.master_fd, b"\x03\x03\x03") # Send 3x Ctrl+C
                        time.sleep(1)
                        os.write(self.master_fd, b"/exit\r\n")
                    except: pass
                    
                    # Force kill after 5s if still alive
                    def killer(p):
                        time.sleep(5)
                        try:
                            os.killpg(os.getpgid(p), signal.SIGKILL)
                            logging.info(f"Force killed process group {p}")
                        except: pass
                    threading.Thread(target=killer, args=(self.child_pid,), daemon=True).start()

            r, _, _ = select.select([sys.stdin], [], [], 0.05)
            if sys.stdin in r:
                try:
                    data = os.read(sys.stdin.fileno(), 1024)
                    if data and self.state == "IDLE": os.write(self.master_fd, data)
                except: pass

        if self.master_fd:
            try: os.close(self.master_fd)
            except: pass

if __name__ == "__main__":
    try: kernel = SovereignKernel(); kernel.run()
    except: sys.exit(1)

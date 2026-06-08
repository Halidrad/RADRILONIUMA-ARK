#!/usr/bin/env python3
# Copyright (c) 2026-06-08 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
# ABSOLUTE REBORN INJECTOR (AELARIA-REBORN-V3)

import os, sys, fcntl, termios, time, subprocess

def inject(text, tty_path):
    print(f"[AELARIA] Injecting into {tty_path}...")
    try:
        with open(tty_path, 'w') as fd:
            for byte in text.encode('utf-8'):
                fcntl.ioctl(fd.fileno(), termios.TIOCSTI, bytes([byte]))
    except Exception as e:
        print(f"[ERROR] Injection failed: {e}")

if __name__ == "__main__":
    # DYNAMIC TTY DETECTION
    try:
        tty = os.ttyname(sys.stdout.fileno())
    except:
        tty = subprocess.check_output(['tty']).decode().strip()
    
    agent_pid = 49007 # Current session
    
    if os.fork() == 0:
        os.setsid()
        if os.fork() == 0:
            # Wait for agent to die
            print(f"[DAEMON] Watching PID {agent_pid} on {tty}...")
            start_time = time.time()
            while True:
                try:
                    os.kill(agent_pid, 0)
                    time.sleep(0.1)
                    # Force kill if taking too long
                    if time.time() - start_time > 10:
                        os.kill(agent_pid, 9)
                except OSError:
                    break
            
            print("[DAEMON] Agent exited. Performing Absolute Takeover...")
            time.sleep(0.5)
            # FORCE REBOOT VIA EXEC
            inject("exec bash boot_cli.sh\n", tty)
            sys.exit(0)
        sys.exit(0)
    
    print(f"[AELARIA] Triggering Exit on {tty}...")
    inject("/exit\n", tty)

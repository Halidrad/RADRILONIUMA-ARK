#!/usr/bin/env python3
# ==============================================================================
# PROTOCOL: ARK_LICENSING_INIT (PYTHON EDITION)
# DATE: 2026-06-07
# ARCHITECT: Halidrad
# TARGET: RADRILONIUMA / TRIANIUMA ARK REPOSITORIES
# RESONANCE: 432 Hz (Law of Resonance)
#
# ENV_PROFILE:
#   env_id: ENV_LOCAL_NEXUS_BASH
#   shell: bash
#   workspace_class: nexus_local_workspace
# ==============================================================================

import os
import sys
import subprocess

# Verify environment profile (TOOL EXECUTION SAFETY PROTOCOL V2 Rules 8 & 9)
cwd = os.getcwd()
if "RADRILONIUMA" not in cwd:
    print("ERROR: TV_ENV_PROFILE_UNDECLARED_OR_MISMATCHED (must run from RADRILONIUMA root)", file=sys.stderr)
    sys.exit(2)

print("[INFO] Resonance aligned at 432 Hz. System state: ACTIVE_READY.")
print("[INFO] Initializing Licensing Epoch for Ark Repositories...")

TIMESTAMP = "2026-06-07"
COPYRIGHT_HEADER = f"Copyright (c) {TIMESTAMP} RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved."

LICENSE_COMMUNITY = """AGPLv3 Community License Agreement
----------------------------------
This software is provided for individuals and community research under the 
terms of the AGPLv3. Any derivative work serving users over a network 
must disclose its source code."""

LICENSE_ENTERPRISE_NOTICE = """ENTERPRISE / CORPORATE NOTICE
-----------------------------
For corporate, governmental, or commercial utilization, this software is 
subject to the TRIANIUMA ENTERPRISE AGREEMENT. 
Usage without a valid Enterprise Key constitutes a violation of the 
Trianiuma Kingdom IP protocols. 
Contact: contact@trianiuma.ark"""

target_filter = sys.argv[1] if len(sys.argv) > 1 else None

# Find git repositories under LAM_CORE
lam_core = "/home/architit/LAM_CORE"
for entry in os.listdir(lam_core):
    repo_path = os.path.join(lam_core, entry)
    if not os.path.isdir(repo_path):
        continue
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        continue
        
    repo_name = os.path.basename(repo_path)
    if target_filter and repo_name != target_filter and repo_path != target_filter:
        continue

    print(f"[DEBUG] Processing: {repo_path}")

    # 1. Inject/Update LICENSE.md
    license_content = f"{LICENSE_COMMUNITY}\n\n\n{LICENSE_ENTERPRISE_NOTICE}\n"
    with open(os.path.join(repo_path, "LICENSE.md"), "w", encoding="utf-8") as f:
        f.write(license_content)

    # 2. Inject NOTICE.md
    notice_content = "Protocol: Sovereign Tree / M48\nMetabolic Status: PROTECTED\n"
    with open(os.path.join(repo_path, "NOTICE.md"), "w", encoding="utf-8") as f:
        f.write(notice_content)

    # 3. Apply Copyright Headers to source files (Python/TS/Go)
    extensions = (".py", ".ts", ".go")
    exclude_dirs = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    print(f"[WARN] Failed to read {file_path}: {e}")
                    continue

                if "RADRILONIUMA / TRIANIUMA Kingdom" in content:
                    continue

                if file.endswith(".py"):
                    commented_header = f"# {COPYRIGHT_HEADER}\n"
                else:
                    commented_header = f"// {COPYRIGHT_HEADER}\n"

                lines = content.splitlines(keepends=True)
                if lines and lines[0].startswith("#!"):
                    if len(lines) > 1 and "RADRILONIUMA / TRIANIUMA Kingdom" in lines[1]:
                        continue
                    lines.insert(1, commented_header)
                else:
                    lines.insert(0, commented_header)

                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(lines)
                    print(f"[DEBUG] Injected header into: {file_path}")
                except Exception as e:
                    print(f"[WARN] Failed to write {file_path}: {e}")

    # 4. Initialize BEASTSPOT monitoring for this repo
    try:
        subprocess.run(["git", "config", "--add", "ark.protection", "enabled"], cwd=repo_path, check=True)
    except Exception as e:
        print(f"[WARN] Failed to set git config for {repo_path}: {e}")

    print(f"[SUCCESS] {repo_path} secured.")

print(f"[METABOLIC_STREAM] Licensing update completed. Epoch {TIMESTAMP} verified.")

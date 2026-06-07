# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
import sys
from pathlib import Path

def patch_gate():
    target = Path("../LAM-Codex_Agent/src/codex_agent/gate.py")
    if not target.exists():
        print(f"Error: {target} not found")
        return
    
    content = target.read_text()
    
    # Add params to ask
    content = content.replace(
        'def ask(self, prompt: str, model_hint: str = "auto", sys_prompt: str = "You are the Codex.") -> str:',
        'def ask(self, prompt: str, model_hint: str = "auto", sys_prompt: str = "You are the Codex.", temperature: float = 0.2, max_tokens: int = 2048) -> str:'
    )
    
    # Update internal calls
    content = content.replace(
        'return self._ask_gemini(prompt, sys_prompt, model=model_hint if "gemini" not in model_hint else "gemini-2.0-flash")',
        'return self._ask_gemini(prompt, sys_prompt, model=model_hint if "gemini" not in model_hint else "gemini-2.0-flash", temperature=temperature, max_tokens=max_tokens)'
    )
    content = content.replace(
        'return self._ask_openai(prompt, sys_prompt, model=model_hint if "openai" not in model_hint else "gpt-4o")',
        'return self._ask_openai(prompt, sys_prompt, model=model_hint if "openai" not in model_hint else "gpt-4o", temperature=temperature, max_tokens=max_tokens)'
    )
    
    # Update _ask_gemini
    content = content.replace(
        'def _ask_gemini(self, prompt: str, sys_prompt: str, model: str) -> str:',
        'def _ask_gemini(self, prompt: str, sys_prompt: str, model: str, temperature: float, max_tokens: int) -> str:'
    )
    content = content.replace(
        'config={"system_instruction": sys_prompt}',
        'config={"system_instruction": sys_prompt, "temperature": temperature, "max_output_tokens": max_tokens}'
    )
    
    # Update _ask_openai
    content = content.replace(
        'def _ask_openai(self, prompt: str, sys_prompt: str, model: str) -> str:',
        'def _ask_openai(self, prompt: str, sys_prompt: str, model: str, temperature: float, max_tokens: int) -> str:'
    )
    content = content.replace(
        'model=model,',
        'model=model, temperature=temperature, max_tokens=max_tokens,'
    )
    
    target.write_text(content)
    print(f"Patched {target}")

def patch_flash_brain():
    target = Path("../LAM-Codex_Agent/flash_brain.py")
    if not target.exists():
        print(f"Error: {target} not found")
        return
    
    # Rewrite flash_brain.py to be much cleaner and use CodexGate
    new_content = """#!/usr/bin/env python3
# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
\"\"\"Fast Codex Bridge for low-friction cognitive offloading.
Unified version using src.codex_agent.gate.
\"\"\"

import argparse
import os
import re
import sys
from pathlib import Path

# Setup path to include src
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from codex_agent.gate import CodexGate

DEFAULT_SYSTEM_PROMPT = (
    "You are Fast-Thought assistant for asynchronous development. "
    "Transform rough notes into concise, implementation-ready drafts."
)

def _read_prompt(args):
    if args.prompt: return args.prompt
    if args.prompt_file: return Path(args.prompt_file).read_text(encoding="utf-8")
    return sys.stdin.read()

def _slug(value: str, limit: int = 40) -> str:
    cleaned = re.sub(r"\\s+", "_", value.strip())
    cleaned = re.sub(r"[^0-9A-Za-z_-]+", "", cleaned)
    return (cleaned[:limit] or "thought_dump").strip("_") or "thought_dump"

def main():
    parser = argparse.ArgumentParser(description="Codex Flash Bridge")
    parser.add_argument("--models", default="auto", help="Model hint")
    parser.add_argument("--system", default=DEFAULT_SYSTEM_PROMPT, help="System prompt")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-output-tokens", type=int, default=2048)
    
    sub = parser.add_subparsers(dest="command", required=True)
    
    ask = sub.add_parser("ask")
    ask.add_argument("prompt", nargs="?")
    ask.add_argument("--prompt-file")
    ask.add_argument("--save")
    
    hib = sub.add_parser("hibernate")
    hib.add_argument("prompt", nargs="?")
    hib.add_argument("--output-dir", default="thoughts")
    
    args = parser.parse_args()
    gate = CodexGate()
    prompt = _read_prompt(args)
    
    if args.command == "ask":
        res = gate.ask(prompt, model_hint=args.models, sys_prompt=args.system, 
                      temperature=args.temperature, max_tokens=args.max_output_tokens)
        if args.save:
            Path(args.save).write_text(res, encoding="utf-8")
            print(f"Saved: {args.save}")
        else:
            print(res)
            
    elif args.command == "hibernate":
        full_prompt = f"Transform this thought into a structured draft:\\n\\n{prompt}"
        res = gate.ask(full_prompt, model_hint=args.models, sys_prompt=args.system,
                      temperature=args.temperature, max_tokens=args.max_output_tokens)
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{_slug(prompt)}.md"
        out_file.write_text(res, encoding="utf-8")
        print(f"Saved: {out_file}")

if __name__ == "__main__":
    main()
"""
    target.write_text(new_content)
    print(f"Refactored {target}")

if __name__ == "__main__":
    patch_gate()
    patch_flash_brain()

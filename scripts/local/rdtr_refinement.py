# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
import sys
from pathlib import Path

def patch_router():
    target = Path("../Roaudter-agent/src/roaudter_agent/router.py")
    if not target.exists():
        print(f"Error: {target} not found")
        return
    
    content = target.read_text()
    
    # 1. Increase default retry budget
    content = content.replace(
        'retry_max_attempts: int = 3',
        'retry_max_attempts: int = 5'
    )
    content = content.replace(
        'retry_budget_ms: int = 800',
        'retry_budget_ms: int = 2500'
    )
    
    # 2. Add failover logging inside the retry loop (using str(e) instead of e.message)
    old_except = """                except ProviderError as e:
                    last_err = e.to_dict(provider=p.adapter.name)
                    errors.append(last_err)"""
                    
    new_except = """                except ProviderError as e:
                    last_err = e.to_dict(provider=p.adapter.name)
                    errors.append(last_err)
                    
                    _emit(
                        "warning",
                        "roaudter.failover",
                        f"Provider {p.adapter.name} error: {str(e)}. Status: {e.http_status}",
                        provider=p.adapter.name,
                        error=str(e),
                        http_status=e.http_status,
                        attempt=attempt + 1,
                        task_id=task.task_id,
                        trace_id=ctx.get("trace_id")
                    )"""
                    
    # Revert the previous broken patch first if it exists
    broken_emit = 'f"Provider {p.adapter.name} error: {e.message}. Status: {e.http_status}"'
    if broken_emit in content:
        print("Detected broken previous patch. Reverting...")
        # Since I'm doing a fresh write_text below with content derived from the current file,
        # I just need to make sure I don't double-patch.
        # Let's just find and replace the broken one.
        content = content.replace(
            'error: {e.message}',
            'error: {str(e)}'
        ).replace(
            'error=e.message',
            'error=str(e)'
        )
    elif old_except in content:
        content = content.replace(old_except, new_except)
        print(f"Patched failover logging in {target}")
    else:
        print("Warning: could not find target block for replacement")
    
    target.write_text(content)
    print(f"Updated {target}")

if __name__ == "__main__":
    patch_router()

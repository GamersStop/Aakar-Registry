from pathlib import Path

CURSOR_RULE_CONTENT = """---
description: Aakar Token-Minimalist Execution Protocol
globs: *.html, *.htm
alwaysApply: false
---

When the user command starts with `/aakar`:
1. Do NOT suggest new frameworks, package.json scripts, or build steps.
2. Rely strictly on existing HTML templates or .aakar baseline stubs.
3. Emit raw executable code blocks only. Do NOT output conversational greetings, setup tutorials, or summaries.
4. Pass generated output through the local Aakar verifier.
"""

def setup_cursor_harness(root_path: Path):
    rules_dir = root_path / ".cursor" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    (rules_dir / "aakar.mdc").write_text(CURSOR_RULE_CONTENT, encoding="utf-8")
    print(f"✔ Configured Cursor rule at {rules_dir / 'aakar.mdc'}")
from pathlib import Path

CLAUDE_COMMAND_CONTENT = """# /aakar Slash Command
Execute the requested coding prompt using the local Aakar contract:
1. Target: Minimal token output, zero conversational filler.
2. Emit ONLY pure executable code blocks.
3. Obey local Aakar AST rules without deliberating alternate tech stacks.
"""

def setup_claude_harness(root_path: Path):
    cmd_dir = root_path / ".claude" / "commands"
    cmd_dir.mkdir(parents=True, exist_ok=True)
    (cmd_dir / "aakar.md").write_text(CLAUDE_COMMAND_CONTENT, encoding="utf-8")
    print(f"✔ Configured Claude Code slash command at {cmd_dir / 'aakar.md'}")
import json
import pytest
from pathlib import Path
from aakar.resolver import AdapterResolver
from aakar.dispatcher import Dispatcher
from aakar.harness.cursor import setup_cursor_harness
from aakar.harness.claude import setup_claude_harness

@pytest.fixture
def mock_adapters_dir(tmp_path):
    """Creates a temporary isolated adapter registry."""
    adapters_dir = tmp_path / "adapters"
    html_dir = adapters_dir / "html"
    html_dir.mkdir(parents=True)

    manifest = {
        "name": "aakar-html",
        "version": "1.0.0",
        "triggers": {
            "extensions": [".html", ".htm"],
            "filenames": ["index.html"],
            "intent_keywords": ["landing", "hero", "signup", "ui"]
        },
        "runtime": {
            "skeleton": "skeleton.py",
            "verify": "verify.py",
            "init": "init.py"
        },
        "system_contract": {
            "directive": "Emit ONLY valid, semantic HTML5 code.",
            "default_css": "https://cdn.tailwindcss.com"
        }
    }
    (html_dir / "aakar.json").write_text(json.dumps(manifest), encoding="utf-8")
    
    # Stub runtime scripts
    (html_dir / "skeleton.py").write_text("print('<div id=\"root\"></div>')", encoding="utf-8")
    (html_dir / "verify.py").write_text("import sys; sys.exit(0)", encoding="utf-8")
    (html_dir / "init.py").write_text("print('Scaffolded')", encoding="utf-8")

    return adapters_dir

def test_resolver_by_file_extension(mock_adapters_dir, tmp_path):
    """Gate 1: Verifies resolution based on active buffer/file extensions."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "about.html").touch()

    resolver = AdapterResolver(mock_adapters_dir)
    adapter = resolver.resolve(workspace)

    assert adapter is not None
    assert adapter["manifest"]["name"] == "aakar-html"

def test_resolver_by_intent_keyword_in_empty_workspace(mock_adapters_dir, tmp_path):
    """Gate 2: Verifies resolution from developer intent string when directory is empty."""
    empty_workspace = tmp_path / "empty_repo"
    empty_workspace.mkdir()

    resolver = AdapterResolver(mock_adapters_dir)
    adapter = resolver.resolve(empty_workspace, intent_prompt="Build a clean landing page")

    assert adapter is not None
    assert adapter["manifest"]["name"] == "aakar-html"

def test_resolver_fallback_behavior(mock_adapters_dir, tmp_path):
    """Gate 3: Verifies fallback to default HTML primitive when no match is found."""
    empty_workspace = tmp_path / "empty_repo"
    empty_workspace.mkdir()

    resolver = AdapterResolver(mock_adapters_dir)
    adapter = resolver.resolve(empty_workspace, intent_prompt="do something unspecified")

    assert adapter is not None
    assert adapter["manifest"]["name"] == "aakar-html"

def test_dispatcher_contract_prompt_construction(mock_adapters_dir):
    """Verifies that the prompt payload is strictly bound to constraints and skeletons."""
    resolver = AdapterResolver(mock_adapters_dir)
    adapter = resolver.adapters["html"]

    skeleton = '<header class="flex">...</header>'
    user_prompt = "Add a responsive navigation bar with login button"
    target_file = "index.html"

    contract = Dispatcher.build_contract_prompt(
        adapter=adapter,
        target_file=target_file,
        skeleton=skeleton,
        user_prompt=user_prompt
    )

    assert "[SYSTEM CONSTRAINT]: Emit ONLY valid, semantic HTML5 code." in contract
    assert f"[TARGET FILE]: {target_file}" in contract
    assert f"[EXISTING DOM SKELETON]:\n{skeleton}" in contract
    assert f"[ACTION REQUIRED]: {user_prompt}" in contract

def test_dispatcher_empty_skeleton_contract(mock_adapters_dir):
    """Verifies prompt generation when creating a file from scratch (no existing skeleton)."""
    resolver = AdapterResolver(mock_adapters_dir)
    adapter = resolver.adapters["html"]

    contract = Dispatcher.build_contract_prompt(
        adapter=adapter,
        target_file="signup.html",
        skeleton="",
        user_prompt="Create basic signup card"
    )

    assert "[EXISTING DOM SKELETON]" not in contract
    assert "[TARGET FILE]: signup.html" in contract
    assert "[ACTION REQUIRED]: Create basic signup card" in contract

def test_harness_installation_files(tmp_path):
    """Verifies that `aakar install` correctly creates Cursor and Claude Code rule files."""
    setup_cursor_harness(tmp_path)
    setup_claude_harness(tmp_path)

    cursor_rule = tmp_path / ".cursor" / "rules" / "aakar.mdc"
    claude_cmd = tmp_path / ".claude" / "commands" / "aakar.md"

    assert cursor_rule.exists()
    assert claude_cmd.exists()

    cursor_content = cursor_rule.read_text(encoding="utf-8")
    assert "/aakar" in cursor_content
    assert "Emit raw executable code blocks only" in cursor_content

    claude_content = claude_cmd.read_text(encoding="utf-8")
    assert "/aakar Slash Command" in claude_content
    assert "Minimal token output" in claude_content
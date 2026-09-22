import json
from pathlib import Path

class AdapterResolver:
    def __init__(self, adapters_dir: Path):
        self.adapters_dir = adapters_dir
        self.adapters = self._load_manifests()

    def _load_manifests(self) -> dict[str, dict]:
        manifests = {}
        if not self.adapters_dir.exists():
            return manifests
        for manifest_file in self.adapters_dir.glob("*/aakar.json"):
            try:
                data = json.loads(manifest_file.read_text(encoding="utf-8"))
                manifests[manifest_file.parent.name] = {
                    "path": manifest_file.parent,
                    "manifest": data
                }
            except Exception:
                continue
        return manifests

    def resolve(self, workspace_path: Path, intent_prompt: str = "") -> dict | None:
        files = list(workspace_path.iterdir()) if workspace_path.exists() else []

        # Gate 1: Check existing files in workspace
        for file in files:
            for name, adapter in self.adapters.items():
                triggers = adapter["manifest"].get("triggers", {})
                if file.suffix in triggers.get("extensions", []):
                    return adapter
                if file.name in triggers.get("filenames", []):
                    return adapter

        # Gate 2: Deterministic keyword match on user prompt
        prompt_lower = intent_prompt.lower()
        for name, adapter in self.adapters.items():
            triggers = adapter["manifest"].get("triggers", {})
            for kw in triggers.get("intent_keywords", []):
                if kw in prompt_lower:
                    return adapter

        # Gate 3: Default fallback
        return self.adapters.get("html")
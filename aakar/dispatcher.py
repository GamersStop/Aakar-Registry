import subprocess
from pathlib import Path

class Dispatcher:
    @staticmethod
    def extract_skeleton(adapter: dict, target_file: Path) -> str:
        skeleton_script = adapter["path"] / adapter["manifest"]["runtime"]["skeleton"]
        if not skeleton_script.exists() or not target_file.exists():
            return ""
        
        result = subprocess.run(
            ["python", str(skeleton_script), str(target_file)],
            capture_output=True,
            text=True
        )
        return result.stdout if result.returncode == 0 else ""

    @staticmethod
    def build_contract_prompt(adapter: dict, target_file: str, skeleton: str, user_prompt: str) -> str:
        manifest = adapter["manifest"]
        directive = manifest.get("system_contract", {}).get("directive", "")
        
        parts = [
            f"[SYSTEM CONSTRAINT]: {directive}",
            f"[TARGET FILE]: {target_file}"
        ]
        if skeleton.strip():
            parts.append(f"[EXISTING DOM SKELETON]:\n{skeleton.strip()}")
        parts.append(f"[ACTION REQUIRED]: {user_prompt.strip()}")
        return "\n\n".join(parts)

    @staticmethod
    def verify_candidate(adapter: dict, candidate_code: str) -> tuple[bool, str]:
        verify_script = adapter["path"] / adapter["manifest"]["runtime"]["verify"]
        if not verify_script.exists():
            return True, "Verifier missing, bypassed."
        
        result = subprocess.run(
            ["python", str(verify_script)],
            input=candidate_code,
            capture_output=True,
            text=True
        )
        passed = result.returncode == 0
        diagnostics = result.stdout if passed else result.stderr
        return passed, diagnostics
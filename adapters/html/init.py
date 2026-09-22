import os
import sys
from pathlib import Path

def scaffold_workspace(target_dir: Path) -> str:
    template_path = Path(__file__).parent / "templates" / "baseline.html"
    index_file = target_dir / "index.html"
    
    if not index_file.exists():
        content = template_path.read_text(encoding="utf-8")
        index_file.write_text(content, encoding="utf-8")
        return "Created index.html with Tailwind CDN baseline (0 tokens used)."
    return "index.html already exists. Skipping scaffold."

if __name__ == "__main__":
    work_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    msg = scaffold_workspace(work_dir)
    print(msg)
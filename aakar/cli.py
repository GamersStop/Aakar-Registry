import argparse
import subprocess
import sys
from pathlib import Path
from aakar.resolver import AdapterResolver
from aakar.dispatcher import Dispatcher
from aakar.harness.cursor import setup_cursor_harness
from aakar.harness.claude import setup_claude_harness

ADAPTERS_PATH = Path(__file__).resolve().parent.parent / "adapters"

def cmd_init(args):
    resolver = AdapterResolver(ADAPTERS_PATH)
    adapter = resolver.resolve(Path.cwd(), args.intent or "")
    if not adapter:
        print("No suitable Aakar adapter found.")
        sys.exit(1)
        
    init_script = adapter["path"] / adapter["manifest"]["runtime"]["init"]
    subprocess.run(["python", str(init_script), str(Path.cwd())])

def cmd_prepare(args):
    target = Path(args.file)
    resolver = AdapterResolver(ADAPTERS_PATH)
    adapter = resolver.resolve(Path.cwd(), args.prompt)
    if not adapter:
        print("No adapter found.")
        sys.exit(1)

    skeleton = Dispatcher.extract_skeleton(adapter, target) if target.exists() else ""
    contract_prompt = Dispatcher.build_contract_prompt(adapter, target.name, skeleton, args.prompt)
    
    print("\n--- [AAKAR CONSTRAINED PROMPT (Pass to Model)] ---")
    print(contract_prompt)
    print("--------------------------------------------------\n")

def cmd_verify(args):
    resolver = AdapterResolver(ADAPTERS_PATH)
    adapter = resolver.resolve(Path.cwd())
    code = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    
    passed, msg = Dispatcher.verify_candidate(adapter, code)
    if passed:
        print("PASS: Code conforms to structural rules.")
        sys.exit(0)
    else:
        print(f"FAIL:\n{msg}", file=sys.stderr)
        sys.exit(1)

def cmd_install(args):
    cwd = Path.cwd()
    setup_cursor_harness(cwd)
    setup_claude_harness(cwd)
    print("Aakar harness setup complete. Activate with `/aakar`.")

def main():
    parser = argparse.ArgumentParser(prog="aakar", description="Token-Minimalist AI Engine Harness")
    subparsers = parser.add_subparsers(dest="subcommand")

    # aakar init
    p_init = subparsers.add_parser("init", help="Scaffold greenfield workspace using active adapter")
    p_init.add_argument("--intent", default="", help="Intent string (e.g. 'landing page')")

    # aakar prepare
    p_prep = subparsers.add_parser("prepare", help="Generate minimal constrained prompt from file & intent")
    p_prep.add_argument("file", help="Target file to modify or create")
    p_prep.add_argument("prompt", help="User instruction")

    # aakar verify
    p_ver = subparsers.add_parser("verify", help="Run local compiler/syntax gate on file or stdin")
    p_ver.add_argument("file", default="-", nargs="?", help="File path or '-' for stdin")

    # aakar install
    subparsers.add_parser("install", help="Inject /aakar commands into Cursor and Claude Code")

    args = parser.parse_args()
    if args.subcommand == "init":
        cmd_init(args)
    elif args.subcommand == "prepare":
        cmd_prepare(args)
    elif args.subcommand == "verify":
        cmd_verify(args)
    elif args.subcommand == "install":
        cmd_install(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
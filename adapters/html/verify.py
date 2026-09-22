import sys
from html.parser import HTMLParser

class StructuralHTMLValidator(HTMLParser):
    VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"
    }

    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.VOID_TAGS:
            self.stack.append((tag.lower(), self.getpos()))

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{tag}> at line {self.getpos()[0]}")
            return
        last_tag, pos = self.stack.pop()
        if last_tag != tag:
            self.errors.append(
                f"Mismatched tag: expected </{last_tag}> (opened line {pos[0]}), found </{tag}> at line {self.getpos()[0]}"
            )

    def validate(self):
        while self.stack:
            tag, pos = self.stack.pop()
            self.errors.append(f"Unclosed tag <{tag}> opened at line {pos[0]}")
        return len(self.errors) == 0, self.errors

def run_verification(code: str) -> tuple[bool, list[str]]:
    validator = StructuralHTMLValidator()
    try:
        validator.feed(code)
        validator.close()
        return validator.validate()
    except Exception as e:
        return False, [str(e)]

if __name__ == "__main__":
    raw_code = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1], encoding="utf-8").read()
    valid, issues = run_verification(raw_code)
    if not valid:
        print("Aakar HTML Verification FAILED:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        sys.exit(1)
    print("Verification passed (Exit 0).")
    sys.exit(0)
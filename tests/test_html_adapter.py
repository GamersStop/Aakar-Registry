import pytest
from adapters.html.verify import run_verification
from adapters.html.skeleton import extract_skeleton

def test_html_verifier_catches_unclosed_tag():
    invalid_html = "<div><section><p>Unclosed paragraph</section></div>"
    valid, errors = run_verification(invalid_html)
    assert not valid
    assert any("Mismatched tag" in err for err in errors)

def test_html_verifier_passes_valid_dom():
    valid_html = "<main class='container'><div id='hero'><input type='text'/><br></div></main>"
    valid, errors = run_verification(valid_html)
    assert valid
    assert len(errors) == 0

def test_skeleton_pruner_strips_inner_text():
    raw_html = """
    <div id="content" class="p-4">
        <h1>Heading Title</h1>
        <p>This is a long paragraph that wastes model prompt tokens unnecessarily.</p>
    </div>
    """
    skeleton = extract_skeleton(raw_html)
    assert "Heading Title" not in skeleton
    assert "wastes model prompt tokens" not in skeleton
    assert '<div id="content" class="p-4">' in skeleton
    assert "<h1>" in skeleton
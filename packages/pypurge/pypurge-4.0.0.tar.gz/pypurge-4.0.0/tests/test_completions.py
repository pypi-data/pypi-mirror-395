import pytest
import argparse
from pypurge.modules.args import parse_args, get_parser
from pypurge.modules.completions import generate_completion_script

def test_completions_flag_structure(capsys):
    """Test that --completions flag is accepted."""
    try:
        args = parse_args(["--completions", "bash"])
        assert args.completions == "bash"
    except SystemExit:
        pytest.fail("parse_args raised SystemExit, implying --completions is not recognized.")

def test_generate_bash_completion():
    """Test generation of bash completion script."""
    parser = get_parser()
    script = generate_completion_script("bash", parser)
    assert "_pypurge_completion() {" in script
    assert "complete -F _pypurge_completion pypurge" in script
    # Check for presence of some known flags
    assert "--preview" in script
    assert "--help" in script

def test_generate_zsh_completion():
    """Test generation of zsh completion script."""
    parser = get_parser()
    script = generate_completion_script("zsh", parser)
    assert "#compdef pypurge" in script
    assert "_describe 'command' opts" in script
    assert "--preview" in script

def test_generate_fish_completion():
    """Test generation of fish completion script."""
    parser = get_parser()
    script = generate_completion_script("fish", parser)
    # Check correct syntax for short and long flags
    assert "complete -c pypurge -l preview" in script
    assert "complete -c pypurge -s p" in script
    assert "complete -c pypurge -l help" in script

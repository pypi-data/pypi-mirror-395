# src/pypurge/modules/completions.py

import argparse

def generate_completion_script(shell: str, parser: argparse.ArgumentParser) -> str:
    """
    Generates a shell completion script for the given shell and parser.
    Currently supports bash, zsh, and fish.
    """
    if shell == "bash":
        return _generate_bash(parser)
    elif shell == "zsh":
        return _generate_zsh(parser)
    elif shell == "fish":
        return _generate_fish(parser)
    else:
        return ""

def _get_opts(parser: argparse.ArgumentParser) -> list[str]:
    opts = []
    for action in parser._actions:
        opts.extend(action.option_strings)
    return opts

def _generate_bash(parser: argparse.ArgumentParser) -> str:
    opts = " ".join(_get_opts(parser))
    return f"""
_pypurge_completion() {{
    local cur prev opts
    COMPREPLY=()
    cur="${{COMP_WORDS[COMP_CWORD]}}"
    prev="${{COMP_WORDS[COMP_CWORD-1]}}"
    opts="{opts}"

    if [[ ${{cur}} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${{opts}}" -- ${{cur}}) )
        return 0
    fi
}}
complete -F _pypurge_completion pypurge
"""

def _generate_zsh(parser: argparse.ArgumentParser) -> str:
    # A simple zsh completion
    opts = " ".join(_get_opts(parser))
    return f"""
#compdef pypurge

_pypurge() {{
    local -a opts
    opts=({opts})
    _describe 'command' opts
}}
_pypurge "$@"
"""

def _generate_fish(parser: argparse.ArgumentParser) -> str:
    # A simple fish completion
    opts = _get_opts(parser)
    lines = []
    for opt in opts:
        if opt.startswith("--"):
            flag = f"-l {opt[2:]}"
        else:
            flag = f"-s {opt[1:]}"
        lines.append(f"complete -c pypurge {flag} -d 'Option {opt}'")
    return "\n".join(lines)

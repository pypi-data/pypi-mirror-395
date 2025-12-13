#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unified help command for the jps-cookiecutter-utils CLI suite.

This Typer app displays a beautifully formatted overview of all entry-point
commands in the package, using the same visual style as the original
`jps-code-repository-utils-help`.

Usage:
    jps-cookiecutter-utils-help
"""

from __future__ import annotations

import textwrap

import typer

# ----------------------------------------------------------------------
# Typer app
# ----------------------------------------------------------------------
app = typer.Typer(
    add_completion=False,
    help="Show an overview of all available jps-cookiecutter-utils commands.",
    no_args_is_help=True,
)


# ANSI colour codes (identical to original)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


@app.command()
def main() -> None:
    """Display the package command overview."""
    help_text = textwrap.dedent(
        f"""
    jps-cookiecutter-utils — Available Commands
    ===============================================

    {GREEN}jps-cookiecutter-utils-bootstrap{RESET}
        Bootstrap a brand-new Python project from a standardized Cookiecutter-style
        template. Creates directory layout, copies files, replaces placeholders,
        validates input, and optionally generates a GitHub initialization script.

        Key features:
        • Interactive prompts for missing values (author, email, org, summary)
        • Supports --infile with key=value defaults
        • Validates infile syntax with --validate
        • Checks for existing GitHub repo (via `gh` CLI)
        • Generates executable `github_project_init_*.sh` script
        • Full logging to timestamped file in /tmp

        Example:
            {YELLOW}jps-cookiecutter-utils-bootstrap --outdir ./projects --code-repository jps-new-utils --verbose{RESET}

        Common flags:
            --infile bootstrap-infile      # defaults to current dir
            --validate                    # validate infile and exit
            --private                     # generate private GitHub repo
            --log-file <path>             # override default log location

    {GREEN}jps-cookiecutter-utils-help{RESET}
        Displays this overview of all available commands.

    ----------------------------------------------------
    Tip: Run each command with '--help' to see detailed options.
    """
    ).strip() + "\n"

    # Typer automatically respects terminal width and ANSI colors
    typer.echo(help_text)


if __name__ == "__main__":
    app()
#!/usr/bin/env python3
"""Bootstrap a new Python project from template files.

A Typer-based CLI tool to bootstrap a new Python project from template files.
It creates a standard directory structure, copies templates, and performs
placeholder substitution, with robust logging and interactive prompts for
missing values.

Logging policy (per spec):
- STDERR handler prints only WARNING and above.
- File handler writes INFO, WARNING, ERROR, CRITICAL using the provided format.
- Verbose progress messages are printed to STDOUT (not via logging).

Usage examples:
    jps-bootstrap --outdir . --code-repository jps-some-project
    jps-bootstrap --outdir ./projects --code-repository jps-new-utils --verbose
"""

from __future__ import annotations

import getpass
import logging
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import typer

# --------------------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------------------

APP_NAME: str = "jps-bootstrap"
EMOJI_STEPS: List[str] = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

# Placeholders we support and their human-friendly prompts
PLACEHOLDER_KEYS: Tuple[str, ...] = (
    "CODE-REPOSITORY",  # hyphenated (e.g., jps-cookiecutter-utils)
    "CODE_REPOSITORY",  # underscored (derived automatically from CODE-REPOSITORY)
    "AUTHOR",
    "AUTHOR-EMAIL",
    "CODE-REPO-ORG",
    "CODE-REPOSITORY-SUMMARY",
)


# Mapping from key (without braces) to placeholder token in files
def to_token(key: str) -> str:
    """Return the placeholder token (with braces) for a given key.

    Args:
        key (str): Placeholder key.

    Returns:
        str: Placeholder token formatted as {{__KEY__}}.
    """
    return "{{__" + key + "__}}"


DEFAULT_INFILE_NAME: str = "bootstrap-infile"

# --------------------------------------------------------------------------------------
# Typer app
# --------------------------------------------------------------------------------------

app = typer.Typer(add_completion=False, help="Bootstrap a new project from templates.")


# --------------------------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------------------------


def configure_logging(log_file: Path) -> None:
    """Configure logging with a file handler (INFO+) and stderr handler (WARNING+).

    Args:
        log_file (Path): Path to the log file to write logs to.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Ensure no duplicate handlers if called multiple times
    for h in list(logger.handlers):
        logger.removeHandler(h)

    # File handler: INFO and above
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    fmt = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"
    file_handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(file_handler)

    # STDERR handler: WARNING and above
    stderr_handler = logging.StreamHandler(stream=sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(stderr_handler)


# --------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------


def parse_infile(infile: Path) -> Dict[str, Optional[str | bool]]:
    """Parse a key=value infile into a dictionary.

    Accepts lines like:
        CODE-REPOSITORY=jps-sample-utils
        AUTHOR=Jane Doe
        AUTHOR-EMAIL=jane@example.com

    Empty lines and lines starting with # are ignored.

    Args:
        infile (Path): Path to the infile.

    Returns:
        Dict[str, str]: Parsed key-value mappings (keys should match PLACEHOLDER_KEYS).
    """
    values: Dict[str, Optional[str | bool]] = {}
    if not infile.exists():
        return values

    with infile.open("r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                logging.warning("Ignoring malformed line in %s: %s", infile, raw.rstrip("\n"))
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            if key in PLACEHOLDER_KEYS:
                values[key] = val
            else:
                logging.warning("Unknown key in %s: %s", infile, key)
    return values


def validate_infile_syntax(infile: Path) -> bool:
    """Validate the syntax and content of a bootstrap infile.

    This validation ensures that:
        1. The infile exists and contains valid key=value pairs.
        2. All required placeholder keys are present.
        3. No unknown keys are defined.
        4. All values are non-empty.

    A summary report is written to `bootstrap_infile_validation.txt`
    in the current working directory.

    Args:
        infile (Path): Path to the bootstrap infile to validate.

    Returns:
        bool: True if validation passes, False otherwise.
    """
    report_path = Path.cwd() / "bootstrap_infile_validation.txt"
    results: List[str] = []
    passed = True

    if not infile.exists():
        msg = f"🚫 Infile not found: {infile}"
        typer.secho(msg, err=True)
        logging.error(msg)
        report_path.write_text(msg, encoding="utf-8")
        return False

    # Parse key-value pairs
    values = parse_infile(infile)
    results.append(f"Bootstrap Infile Validation Report\n{'=' * 40}")
    results.append(f"File: {infile}")
    results.append("")

    if not values:
        msg = f"🚫 No valid key=value pairs found in {infile}"
        typer.secho(msg, err=True)
        logging.error(msg)
        results.append(msg)
        report_path.write_text("\n".join(results), encoding="utf-8")
        return False

    # Detect missing, extra, and empty values
    missing = [k for k in PLACEHOLDER_KEYS if k not in values]
    extra = [k for k in values if k not in PLACEHOLDER_KEYS]
    empty = [k for k, v in values.items() if isinstance(v, str) and not v.strip()]

    if missing:
        msg = f"🚫 Missing required keys: {', '.join(missing)}"
        typer.secho(msg, err=True)
        logging.error(msg)
        results.append(msg)
        passed = False

    if extra:
        msg = f"⚠️  Unknown keys detected: {', '.join(extra)}"
        typer.secho(msg)
        logging.warning(msg)
        results.append(msg)

    if empty:
        msg = f"⚠️  Empty values found for: {', '.join(empty)}"
        typer.secho(msg)
        logging.warning(msg)
        results.append(msg)
        passed = False

    # Record summary
    if passed:
        success_msg = (
            f"✅ Infile validation successful — all required keys present and non-empty.\n"
            f"Timestamp: {__import__('datetime').datetime.now().isoformat()}"
        )
        typer.echo(success_msg)
        logging.info(success_msg)
        results.append(success_msg)
    else:
        results.append("❌ Validation failed due to missing or empty values.")

    # Write the validation report
    report_content = "\n".join(results)
    report_path.write_text(report_content, encoding="utf-8")
    logging.info("Infile validation report written to: %s", report_path)
    typer.echo(f"📄 Infile validation report written to: {report_path}")

    return passed


def derive_code_repository_underscore(code_repo_hyphen: str) -> str:
    """Derive the underscored repository name from a hyphenated one.

    Args:
        code_repo_hyphen (str): Hyphenated repository name.

    Returns:
        str: Underscored repository name.
    """
    return code_repo_hyphen.replace("-", "_")


def announce(verbose: bool, step_no: int, message: str) -> None:
    """Print a progress announcement to STDOUT when verbose is True; always log INFO.

    Args:
        verbose (bool): Whether to print to STDOUT.
        step_no (int): Step number for emoji indexing.
        message (str): Message to display/log.
    """
    emoji = EMOJI_STEPS[step_no - 1] if 0 < step_no <= len(EMOJI_STEPS) else "➡️"
    if verbose:
        typer.echo(f"{emoji}  {message}")
    logging.info(message)


def create_project_structure(project_root: Path) -> None:
    """Create the standard project directory structure.

    Args:
        project_root (Path): Root of the new project.
    """
    for rel in ("src", "tests", "docs", ".github/workflow"):
        path = project_root / rel
        path.mkdir(parents=True, exist_ok=True)
        logging.info("Ensured directory exists: %s", path)


def discover_templates_dir() -> Path:
    """Discover the templates/ directory relative to this script.

    By convention, this script resides at: <repo>/src/scripts/bootstrap.py
    Therefore, templates should be at:     <repo>/templates

    Returns:
        Path: Path to the templates directory.

    Raises:
        FileNotFoundError: If templates directory is not found.
    """
    # Allow override via environment variable, if desired (optional)
    # env_override = Path(typer.get_app_dir(APP_NAME))  # not used; kept for future expansion

    here = Path(__file__).resolve()
    repo_root = here.parents[2]  # <repo>
    templates_dir = repo_root / "templates"
    if not templates_dir.exists():
        # Fallback if structure differs (e.g., running from a wheel or different layout)
        alt = Path.cwd() / "templates"
        if alt.exists():
            return alt
        raise FileNotFoundError(f"Could not find templates directory near {here}")
    return templates_dir


def iter_copied_paths(root: Path) -> Iterable[Path]:
    """Yield all file paths under a root directory (recursively).

    Args:
        root (Path): Root directory to walk.

    Yields:
        Iterable[Path]: File paths under the root.
    """
    for p in root.rglob("*"):
        if p.is_file():
            yield p


def copy_templates(template_dir: Path, project_root: Path) -> List[Path]:
    """Copy template files and folders from `template_dir` to `project_root`.

    Args:
        template_dir (Path): Source templates directory.
        project_root (Path): Destination project root.

    Returns:
        List[Path]: List of all files that were copied (absolute paths).
    """
    copied_files: List[Path] = []

    def _copy_item(src: Path, dst: Path) -> None:
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied_files.append(dst.resolve())
            logging.info("Copied: %s -> %s", src, dst)

    for src in template_dir.rglob("*"):
        rel = src.relative_to(template_dir)
        dst = project_root / rel
        _copy_item(src, dst)

    return copied_files


def build_placeholder_map(
    code_repo_hyphen: str,
    supplied: Dict[str, str],
) -> Dict[str, str]:
    """Construct the full placeholder map, deriving underscored name automatically.

    Args:
        code_repo_hyphen (str): Hyphenated repository name from CLI.
        supplied (Dict[str, str]): Values collected from infile/CLI/prompts.

    Returns:
        Dict[str, str]: Mapping from placeholder-token -> value.
    """
    # Ensure hyphen and underscore forms are in 'supplied'
    supplied = dict(supplied)  # copy
    supplied["CODE-REPOSITORY"] = code_repo_hyphen
    supplied["CODE_REPOSITORY"] = derive_code_repository_underscore(code_repo_hyphen)

    token_map: Dict[str, str] = {}
    for key in PLACEHOLDER_KEYS:
        val = supplied.get(key, "")
        token_map[to_token(key)] = val
    return token_map


def files_with_any_placeholder(files: Iterable[Path], token_map: Dict[str, str]) -> List[Path]:
    """Return only files that contain at least one placeholder token.

    Args:
        files (Iterable[Path]): Iterable of file paths to check.
        token_map (Dict[str, str]): Mapping of placeholder tokens to values.

    Returns:
        List[Path]: Files that contain any of the placeholder tokens.
    """
    tokens = tuple(token_map.keys())
    hits: List[Path] = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            logging.warning("Skipping unreadable file %s: %s", f, e)
            continue
        if any(t in text for t in tokens):
            hits.append(f)
    return hits


def replace_placeholders_in_files(files: Iterable[Path], token_map: Dict[str, str]) -> None:
    """Replace placeholder tokens in the given files in-place.

    Files that do not contain placeholders are not modified.

    Args:
        files (Iterable[Path]): Files to scan.
        token_map (Dict[str, str]): Placeholder-token-to-value mapping.
    """
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception as e:
            logging.warning("Skipping unreadable file %s: %s", f, e)
            continue

        original = text
        for token, value in token_map.items():
            text = text.replace(token, value)

        if text != original:
            f.write_text(text, encoding="utf-8")
            logging.info("Updated placeholders in: %s", f)


def github_repo_exists(org: str, repo: str) -> bool:
    """Check whether a GitHub repository already exists using gh CLI.

    Args:
        org (str): GitHub organization or username.
        repo (str): Repository name.

    Returns:
        bool: True if the repository exists, False otherwise.
    """
    logging.info(
        f"Checking if GitHub repo exists: {org}/{repo} with gh CLI: gh repo view {org}/{repo}"
    )
    result = subprocess.run(
        ["gh", "repo", "view", f"{org}/{repo}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def create_github_init_script(
    project_root: Path,
    values: Dict[str, str],
) -> Path | None:
    """Create a GitHub project initialization bash script for the new project.

    The script contains all the required git and GitHub commands to initialize,
    configure, and push the new repository. Commands are echoed for readability
    before execution.

    Args:
        project_root (Path): Path to the root directory of the newly created project.
        values (Dict[str, str]): Placeholder values including author, email, repo info, etc.

    Returns:
        Path: Path to the generated GitHub project initialization script.
    """
    repo_hyphen = values.get("CODE-REPOSITORY", "unknown-repo")
    org = values.get("CODE-REPO-ORG", "unknown-org")

    if github_repo_exists(org, repo_hyphen):
        msg = f"⚠️  Repository {org}/{repo_hyphen} already exists on GitHub."
        typer.secho(msg, fg="yellow")
        logging.warning(msg)
        return None

    repo_underscore = values.get("CODE_REPOSITORY", repo_hyphen.replace("-", "_"))
    author = values.get("AUTHOR", "unknown")
    author_email = values.get("AUTHOR-EMAIL", "unknown@example.com")

    # Determine visibility
    visibility = "--private" if values.get("PRIVATE_REPO") == "true" else "--public"
    visibility_label = "private" if values.get("PRIVATE_REPO") == "true" else "public"

    # Prepare script filename in the current working directory
    script_name = f"github_project_init_{repo_underscore}.sh"
    github_script = Path.cwd() / script_name

    # If script exists, delete it.
    if github_script.exists():
        github_script.unlink()
        logging.info("Overwriting existing script: %s", github_script)

    # Template for the initialization script
    script_content = f"""#!/usr/bin/env bash
# --------------------------------------------------------------------
# GitHub project initialization script for {repo_underscore}
# Generated automatically by jps-cookiecutter-utils
# --------------------------------------------------------------------

set -euo pipefail

echo "🚀 Initializing project: {repo_hyphen}"
"""
    script_content += f"""
echo "👤 Author: {author} <{author_email}>"
echo "🏷️ GitHub Org: {org}"
echo "🔒 Repository Visibility: {visibility_label}"
echo ""

echo "📁 Changing directory to project location..."
cd {project_root} || exit 1

echo "📂 Creating standard directories..."
mkdir -p src tests docs .github/workflow

echo "🔧 Initializing Git repository..."
git init -b main

echo "➕ Staging files for initial commit..."
git add .

echo "👤 Setting Git author configuration..."
git config user.name \"{author}\" && git config user.email \"{author_email}\"

echo "💬 Creating initial commit..."
git commit -m \"feat: initialize {repo_hyphen} project structure\"

echo "🌐 Creating GitHub repository via gh CLI..."
gh repo create {org}/{repo_hyphen} {visibility} --source=. --remote=origin

echo "🚀 Pushing initial commit to remote main branch..."
git push -u origin main

echo ""
echo "✅ GitHub project initialization complete!"
echo "🌐 Repository URL: https://github.com/{org}/{repo_hyphen}"
"""

    # Write the file
    github_script.write_text(script_content, encoding="utf-8")

    # Make it executable
    github_script.chmod(0o755)

    # Log and notify
    logging.info("Created GitHub initialization script: %s", github_script)

    return github_script


def prompt_missing_values(values: Dict[str, str]) -> Dict[str, str]:
    """Prompt the user for any missing placeholder values (except CODE* which are derived/provided).

    Args:
        values (Dict[str, str]): Existing values (from infile and/or CLI).

    Returns:
        Dict[str, str]: Updated values including responses from user prompts.
    """
    out = dict(values)
    prompts = {
        "AUTHOR": "Author full name",
        "AUTHOR-EMAIL": "Author email",
        "CODE-REPO-ORG": "GitHub org/user",
        "CODE-REPOSITORY-SUMMARY": "Short project summary",
    }
    for key, label in prompts.items():
        if not out.get(key):
            out[key] = typer.prompt(f"Enter {label}")
            logging.info("Collected value for %s", key)
    return out


def validate_code_repository(name: Optional[str]) -> None:
    """Validate the hyphenated code repository name.

    Args:
        name (str): Proposed repository name.

    Raises:
        SystemExit: If the name is invalid.
    """
    import re

    if not name:
        typer.secho("🚫 --code-repository was not defined.", err=True)
        raise SystemExit(2)
    if len(name) < 3:
        typer.secho("🚫 --code-repository must be at least 3 characters.", err=True)
        raise SystemExit(2)
    pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]$")
    if not pattern.match(name):
        typer.secho(
            "🚫 --code-repository may only contain letters, digits, dot, underscore, and hyphen; must start/end with alphanumeric.",  # noqa
            err=True,
        )
        raise SystemExit(2)


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------


@app.command()
def main(
    outdir: Path = typer.Option(
        ...,
        "--outdir",
        help="Output directory root. Project is created under this path as <outdir>/<code-repository>.",
    ),
    code_repository: str | None = typer.Option(
        None,
        "--code-repository",
        help="Hyphenated repository name, e.g., jps-cookiecutter-utils. "
        "If not provided, the value will be read from the infile.",
    ),
    author: str | None = typer.Option(None, "--author", help="Author full name."),
    author_email: str | None = typer.Option(None, "--author-email", help="Author email."),
    code_repo_org: str | None = typer.Option(
        None, "--code-repo-org", help="GitHub organization or username."
    ),
    code_repo_summary: str | None = typer.Option(
        None, "--code-repo-summary", help="Short project summary."
    ),
    infile: Path = typer.Option(
        Path(DEFAULT_INFILE_NAME),
        "--infile",
        help="Path to key=value infile with placeholder defaults.",
    ),
    private_repo: bool = typer.Option(
        False,
        "--private",
        help="Mark the new GitHub repository as private when generating initialization script.",
    ),
    validate_infile: bool = typer.Option(
        False,
        "--validate",
        help="Validate the bootstrap infile and exit without creating a project.",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", help="Show step-by-step progress with emojis."
    ),
    log_file: Path | None = typer.Option(
        None, "--log-file", help="Optional log file path. Defaults to <project_dir>/bootstrap.log."
    ),
) -> None:
    """Bootstrap a new project under <outdir>/<code-repository> from templates.

    Args:
        outdir (Path): Output directory root.
        code_repository (Optional[str]): Repository name.
        author (Optional[str]): Author full name.
        author_email (Optional[str]): Author email address.
        code_repo_org (Optional[str]): GitHub organization or username.
        code_repo_summary (Optional[str]): Short project summary.
        infile (Path): Path to key=value infile with placeholder defaults.
        private_repo (bool): Whether to create a private repository.
        validate_infile (bool): Validate infile and exit.
        verbose (bool): Enable step-by-step output.
        log_file (Optional[Path]): Optional path for the log file.

    Raises:
        SystemExit: On invalid input, validation failure, or aborted bootstrap.
    """
    # Configure logging in a temp, timestamped directory
    user = getpass.getuser()
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    tmp_log_dir = Path(f"/tmp/{user}/jps-cookiecutter-utils/bootstrap/{timestamp}")
    tmp_log_dir.mkdir(parents=True, exist_ok=True)
    final_log_file = tmp_log_dir / "bootstrap.log"

    announce(verbose, 1, f"Configuring logging. Bootstrap log: {final_log_file}")
    configure_logging(final_log_file)
    logging.info("Logging initialized. Bootstrap log: %s", final_log_file)

    # Read infile & collect values
    announce(verbose, 2, f"Reading defaults from infile: {infile}")
    values = parse_infile(infile)

    if validate_infile:
        typer.echo(f"🔍 Validating bootstrap infile: {infile}")
        success = validate_infile_syntax(infile)
        if success:
            typer.echo("✅ Infile validation completed successfully.")
            raise SystemExit(0)
        else:
            typer.secho("❌ Infile validation failed.", err=True)
            raise SystemExit(1)

    # ----------------------------------------------------------------------
    # Handle CODE-REPOSITORY value from infile vs. CLI
    # ----------------------------------------------------------------------
    infile_repo = values.get("CODE-REPOSITORY")

    # Case 1: Neither provided
    if not infile_repo and not code_repository:
        typer.secho(
            "🚫 Missing required repository name. "
            "Specify --code-repository or define CODE-REPOSITORY in the infile.",
            fg="red",
        )
        raise SystemExit(1)

    # Case 2: Both provided but different
    if infile_repo and code_repository and infile_repo != code_repository:
        typer.secho(
            f"🚫 Conflict: CODE-REPOSITORY in infile ({infile_repo}) "
            f"does not match --code-repository value ({code_repository}).",
            fg="red",
        )
        raise SystemExit(1)

    # Case 3: Use infile value if CLI not provided
    if not code_repository and infile_repo:
        code_repository = str(infile_repo)

    # Validate code-repository and assert non-None for type-safety
    validate_code_repository(code_repository)
    assert code_repository is not None

    # Compute final project root: <outdir>/<code_repository>
    project_root = (outdir / code_repository).resolve()

    # ----------------------------------------------------------------------
    # Validate project output directory state
    # ----------------------------------------------------------------------
    if project_root.exists():
        contents = list(project_root.iterdir())
        if contents:
            typer.secho(
                f"🚫 Output directory already exists and is not empty: {project_root}",
                fg="red",
            )
            logging.error("Output directory exists and is not empty: %s", project_root)
            raise SystemExit(1)
        else:
            typer.secho(
                f"⚠️  Output directory already exists but is empty — continuing: {project_root}",
                fg="yellow",
            )
            logging.warning("Output directory exists but is empty: %s", project_root)
    else:
        project_root.mkdir(parents=True, exist_ok=True)
        logging.info("Created new output directory: %s", project_root)

    # ----------------------------------------------------------------------
    # Overlay CLI-provided values
    # ----------------------------------------------------------------------
    if author:
        values["AUTHOR"] = author
    if author_email:
        values["AUTHOR-EMAIL"] = author_email
    if code_repo_org:
        values["CODE-REPO-ORG"] = code_repo_org
    if code_repo_summary:
        values["CODE-REPOSITORY-SUMMARY"] = code_repo_summary
    if code_repository:
        values["CODE-REPOSITORY"] = code_repository

    # Normalize PRIVATE_REPO as string for downstream consistency (Option B)
    values["PRIVATE_REPO"] = "true" if private_repo else "false"

    # Prompt for missing values
    announce(verbose, 3, "Collecting missing values (interactive)")
    clean_values: Dict[str, str] = {k: str(v) for k, v in values.items() if v is not None}
    clean_values = prompt_missing_values(clean_values)

    # Build token map
    token_map = build_placeholder_map(code_repository, clean_values)

    # ----------------------------------------------------------------------
    # Check if the GitHub repository already exists
    # ----------------------------------------------------------------------
    org = clean_values.get("CODE-REPO-ORG", "")
    if org:
        announce(verbose, 4, f"Checking if GitHub repo already exists: {org}/{code_repository}")
        if github_repo_exists(org, code_repository):
            msg = f"⚠️  GitHub repository already exists: {org}/{code_repository}"
            typer.secho(msg, fg="yellow")
            logging.warning(msg)
            # Abort to avoid duplication
            typer.secho(
                "🚫 Aborting bootstrap to prevent overwriting existing GitHub repository.", fg="red"
            )
            raise SystemExit(1)
    else:
        logging.warning("Skipping GitHub repo existence check — CODE-REPO-ORG missing.")

    # Create directory structure
    announce(verbose, 5, "Creating standard directories (src/, tests/, docs/, .github/workflow/)")
    create_project_structure(project_root)

    # Copy templates
    announce(verbose, 6, "Copying templates into project directory")
    try:
        templates_dir = discover_templates_dir()
    except FileNotFoundError as e:
        logging.error("Templates directory not found: %s", e)
        typer.secho(f"🚫 {e}", err=True)
        raise SystemExit(1)

    copied_files = copy_templates(templates_dir, project_root)

    # Substitute placeholders (only in files that contain tokens)
    announce(verbose, 7, "Replacing placeholders in copied files")
    target_files = files_with_any_placeholder(copied_files, token_map)
    replace_placeholders_in_files(target_files, token_map)

    # Validate and summarize project contents
    announce(verbose, 8, "Validating generated project structure")
    if not any(project_root.iterdir()):
        typer.secho("🚫 Project directory is empty — possible copy failure.", err=True)
    else:
        logging.info("Project validation: %d files generated", len(list(project_root.rglob("*"))))

    # Create GitHub initialization script
    announce(verbose, 9, "Creating GitHub project initialization script")
    github_script = create_github_init_script(project_root, clean_values)

    # Done
    announce(verbose, 10, "Project bootstrap complete ✅")
    typer.echo(f"📜 GitHub project initialization script created: {github_script}")
    typer.echo(f"📄 Log written to: {final_log_file}")
    typer.echo(f"📂 Project directory: {project_root}")


if __name__ == "__main__":
    app()

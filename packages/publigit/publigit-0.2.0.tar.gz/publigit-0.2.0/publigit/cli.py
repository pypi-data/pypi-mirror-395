from __future__ import annotations
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

from .pypirc import parse_args, pypirc_has

PYPROJECT = Path("pyproject.toml")
DIST_DIR = Path("dist")
HISTORY = Path("HISTORY.md")

def die(msg: str, code: int = 1) -> None:
    print(f"\nERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def run(cmd: list[str] | tuple[str, ...], **kw) -> None:
    print(f"\n$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True, **kw)


def run_capture(cmd: list[str] | tuple[str, ...]) -> str:
    r = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return r.stdout.strip()

#ensure packages are installed
def ensure_pkg(mod: str, *pkgs: str):

    try:
        __import__(mod)
    except Exception:
        run([sys.executable, "-m", "pip", "install", *pkgs])

#pyproject.toml helpers
def load_pyproject(pyproject: Path) -> tuple[str, str]:
    if not pyproject.exists():
        die(f"pyproject.toml not found at {pyproject.resolve()}")
    try:
        import tomllib
    except Exception as e:
        die("tomllib not available. Use Python ≥3.11 or `pip install tomli`.\n" + repr(e))
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    proj = data.get("project") or {}
    name = proj.get("name")
    version = proj.get("version")
    if not name or not version:
        die("`[project].name` or `[project].version` missing in pyproject.toml")
    return name, version

#PyPI helpers
def get_pypi_latest(name: str) -> str | None:
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            info = json.load(r)
        return info.get("info", {}).get("version")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    except Exception:
        raise

def pep440_is_higher(local: str, remote: str) -> bool:
    try:
        from packaging.version import Version
        return Version(local) > Version(remote)
    except Exception:
        import re
        def parts(v: str): return tuple(int(x) for x in re.findall(r"\d+", v) or [0])
        return parts(local) > parts(remote)

#Git helpers
def git_is_repo() -> bool:
    try:
        out = run_capture(["git", "rev-parse", "--is-inside-work-tree"])
        return out.strip().lower() == "true"
    except Exception:
        return False

def git_current_branch() -> str | None:
    try:
        return run_capture(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    except Exception:
        return None

def git_remote_exists(name: str = "origin") -> bool:
    try:
        remotes = run_capture(["git", "remote"])
        return name in remotes.split()
    except Exception:
        return False

def git_tag_exists(tag: str) -> bool:
    try:
        tags = run_capture(["git", "tag", "--list", tag])
        return bool(tags)
    except Exception:
        return False

#Release notes / HISTORY
def prompt_release_notes() -> str:
    print("\nEnter release notes (finish with an empty line):")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "" and lines:
            break
        lines.append(line)
    notes = "\n".join(lines).strip()
    return notes or "No description provided."


def ensure_history_header() -> None:
    if not HISTORY.exists():
        HISTORY.write_text("# Changelog\n\n", encoding="utf-8")


def append_history(version: str, notes: str) -> None:
    ensure_history_header()
    entry = f"## {version} — {date.today().isoformat()}\n\n{notes}\n\n"
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"Updated {HISTORY}.")


def first_line(text: str) -> str:
    return (text.splitlines()[0] if text else "").strip()



def main() -> None:
    args = parse_args()  # ⬅️ this now sets args.pypirc_path and validates it

    # 1️⃣ Read project info
    name, version = load_pyproject(PYPROJECT)
    print(f"Project: {name}\nLocal  : {version}")

    # 2️⃣  Check PyPI version
    latest = None
    if not args.skip_version_check:
        try:
            latest = get_pypi_latest(name)
        except Exception as e:
            die(f"Failed to query PyPI for {name}: {e!r}")

        if latest is None:
            print("PyPI   : (no release yet)")
        else:
            print(f"PyPI   : {latest}")
            if not pep440_is_higher(version, latest):
                die(f"Version in pyproject.toml ({version}) is NOT higher than PyPI ({latest}).")
    else:
        print("PyPI   : (version check skipped)")

    # 3️⃣  Prompt for notes + update HISTORY.md
    notes = prompt_release_notes()
    append_history(version, notes)

    # 5️⃣  Commit (pre-build)
    did_git = False
    current_branch = None
    if git_is_repo():
        try:
            print("\nSyncing to Git (commit only, push after successful upload) …")
            run(["git", "add", "-A"])
            msg_title = f"Release {version}: {first_line(notes) or 'update changelog'}"
            run(["git", "commit", "-m", msg_title])
            did_git = True
            current_branch = git_current_branch()
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git commit skipped or failed: {e}")
    else:
        print("ℹ️  Not a Git repository. Skipping Git steps.")

    # 6️⃣  Clean dist/
    if DIST_DIR.exists():
        print("\nCleaning dist/ …")
        shutil.rmtree(DIST_DIR)

    # 7️⃣  ensure build toolchain
    ensure_pkg("build", "build", "wheel", "setuptools")

    # 8️⃣  Build
    run([sys.executable, "-m", "build"])

    # 9️⃣  Twine check
    ensure_pkg("twine", "twine")
    run([sys.executable, "-m", "twine", "check", "dist/*"])

    # 🔟  Upload (env creds → .pypirc → ~/.pypirc)
    if args.dry_run:
        print("\n(DRY RUN) Skipping upload and git push/tag.")
        return

    env_has_creds = bool(os.environ.get("TWINE_USERNAME") and os.environ.get("TWINE_PASSWORD"))
    repo_url = "https://test.pypi.org/legacy/" if args.testpypi else "https://upload.pypi.org/legacy/"
    section  = "testpypi" if args.testpypi else "pypi"

    twine_cmd: list[str] = []

    if env_has_creds:
        # Option A: ENV creds (highest priority) → ignore any .pypirc
        print(f"\nUploading to {'TestPyPI' if args.testpypi else 'PyPI'} (env creds; ignoring any .pypirc) …")
        twine_cmd = [
            sys.executable, "-m", "twine", "upload",
            "--config-file", os.devnull,
            "--repository-url", repo_url,
            "dist/*",
        ]

        # sanity for env creds
        if not os.environ.get("TWINE_USERNAME") or not os.environ.get("TWINE_PASSWORD"):
            print("\nMissing TWINE_USERNAME/TWINE_PASSWORD in environment.")
            print("Example (PowerShell):")
            print("  $env:TWINE_USERNAME='__token__'")
            print("  $env:TWINE_PASSWORD='pypi-AgEI...'")
            sys.exit(2)

    else:
        # Option B: use the path already resolved by parse_args() in pypirc.py
        explicit_cfg = getattr(args, "pypirc_path", None)   # Path chosen & validated in parse_args
        if explicit_cfg:
            print(f"\nUploading via .pypirc: {explicit_cfg} …")
            twine_cmd = [
                sys.executable, "-m", "twine", "upload",
                "--config-file", str(explicit_cfg),
                "--repository", section,
                "dist/*",
            ]
        else:
            # Option C: fallback to ~/.pypirc if section exists
            if pypirc_has(section):
                print(f"\nUploading via ~/.pypirc [{section}] …")
                twine_cmd = [
                    sys.executable, "-m", "twine", "upload",
                    "--repository", section,
                    "dist/*",
                ]
            else:
                target = "TestPyPI" if args.testpypi else "PyPI"
                die(
                    f"TWINE_USERNAME/TWINE_PASSWORD not set, no .pypirc resolved, "
                    f"and ~/.pypirc lacks [{section}].\n"
                    f"Set env creds, set PUBLIGIT_PYPIRC / pass --pypirc <path>, "
                    f"or configure ~/.pypirc for {target}."
                )

    run(twine_cmd)

    # 1️⃣1️⃣ Git tagging + push
    if did_git:
        tag = f"v{version}"
        try:
            print("\nTagging release …")
            if git_tag_exists(tag):
                print(f"ℹ️  Tag {tag} already exists; skipping tag creation.")
            else:
                run(["git", "tag", "-a", tag, "-m", f"Release {version}\n\n{notes}"])

            # NEW: ensure GitHub repo + 'origin' remote via PyGithub (option 3)
            # Uses project `name` from pyproject.toml as repo name.
            if git_is_repo():
                ensure_github_repo_pygithub(name, private=False)

            if current_branch and git_remote_exists("origin"):
                print("Pushing branch and tags to origin …")
                run(["git", "push", "origin", current_branch])
                run(["git", "push", "origin", tag])
                print("✅ GitHub sync complete.")
            else:
                print("⚠️  No 'origin' remote or branch unknown; skipping push.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git tagging/push failed: {e}")



def ensure_github_repo_pygithub(
    repo_name: str,
    private: bool = False,
    token_env: str = "GITHUB_TOKEN",
) -> None:
    """
    Ensure a GitHub repo exists for the current user, and add 'origin' if missing.

    - Uses PyGithub (installed on demand via ensure_pkg).
    - Expects a personal access token in `token_env` (default: GITHUB_TOKEN).
    - If the repo already exists, it is reused.
    - If git remote 'origin' is missing, it will be created (SSH URL).
    """
    token = os.getenv(token_env)
    if not token:
        print(f"\nℹ️  {token_env} not set; skipping GitHub repo creation.")
        return

    # Ensure PyGithub is available
    ensure_pkg("github", "PyGithub")

    from github import Github, GithubException  # type: ignore[import]

    gh = Github(token)

    try:
        user = gh.get_user()
        login = user.login
        full_name = f"{login}/{repo_name}"
        print(f"\nEnsuring GitHub repo exists: {full_name} …")

        try:
            repo = gh.get_repo(full_name)
            print(f"ℹ️  GitHub repo '{full_name}' already exists.")
        except GithubException as e:
            if e.status == 404:
                print(f"Creating GitHub repo '{full_name}' (private={private}) …")
                repo = user.create_repo(
                    repo_name,
                    private=private,
                    auto_init=False,
                    has_issues=True,
                    has_wiki=True,
                )
                print(f"✅ Created GitHub repo: {repo.full_name}")
            else:
                print(f"⚠️  Failed to access GitHub repo '{full_name}': {e}")
                return

        # Ensure local git remote 'origin' is configured
        if not git_remote_exists("origin"):
            ssh_url = repo.ssh_url or repo.clone_url
            print(f"Adding git remote 'origin' -> {ssh_url}")
            try:
                run(["git", "remote", "add", "origin", ssh_url])
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Failed to add 'origin' remote: {e}")
        else:
            print("ℹ️  Git remote 'origin' already exists; not modifying.")

    except Exception as e:  # very defensive to avoid killing the release
        print(f"⚠️  Unexpected error while ensuring GitHub repo: {e}")

if __name__ == "__main__":
    main()

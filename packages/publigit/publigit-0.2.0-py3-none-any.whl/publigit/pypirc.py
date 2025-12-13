import argparse
import os
from pathlib import Path
import configparser


def pick_pypirc(args):
    """Determine which .pypirc file to use, with detailed feedback."""
    # 1. Explicit --pypirc argument
    if getattr(args, "pypirc", None):
        cfg = Path(args.pypirc).expanduser().resolve()
        print(f"\nFound explicit --pypirc argument: {cfg}")
        return cfg

    # 2. Environment variable override
    env_cfg = os.getenv("PUBLIGIT_PYPIRC")
    if env_cfg:
        cfg = Path(env_cfg).expanduser().resolve()
        print(f"\nFound .pypirc from PUBLIGIT_PYPIRC env var: {cfg}")
        return cfg

    # 3. Bundled fallback — look in repo root and package dir
    pkg_dir = Path(__file__).resolve().parent          # e.g. D:\Pycharm\Publigit\publigit
    repo_root = pkg_dir.parent                         # e.g. D:\Pycharm\Publigit

    cand_repo = repo_root / ".pypirc"                  # repo root
    cand_pkg = pkg_dir / ".pypirc"                     # package dir

    if cand_repo.exists():
        print(f"\nUsing Publigit-bundled .pypirc (repo root): {cand_repo}")
        return cand_repo
    elif cand_pkg.exists():
        print(f"\nUsing Publigit-bundled .pypirc (package dir): {cand_pkg}")
        return cand_pkg

    # 4. Final fallback — user home
    home_cfg = Path.home() / ".pypirc"
    print(f"\nNo explicit .pypirc found. Falling back to user home: {home_cfg}")
    return home_cfg


def validate_pypirc(cfg: Path):
    """Print parse result (non-fatal)."""
    if not cfg.exists():
        print(f"⚠️  .pypirc file not found: {cfg}")
        return
    try:
        cp = configparser.ConfigParser()
        cp.read(cfg)
        sections = ", ".join(cp.sections()) or "(no sections)"
        print(f"Parsed successfully. Sections: {sections}")
    except Exception as e:
        print(f"⚠️  Failed to parse {cfg}: {e}")


def parse_args():
    """Parse CLI arguments and verify .pypirc usability."""
    p = argparse.ArgumentParser()
    p.add_argument("--testpypi", action="store_true")
    p.add_argument("--skip-version-check", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--pypirc", type=str, help="Path to a .pypirc file to use instead of ~/.pypirc")
    args = p.parse_args()

    # Resolve which .pypirc to use and validate it
    args.pypirc_path = pick_pypirc(args)
    validate_pypirc(args.pypirc_path)
    return args

def pypirc_has(section: str) -> bool:
    """
    Check if ~/.pypirc contains the given section (e.g. 'pypi' or 'testpypi').
    """
    cfg = Path.home() / ".pypirc"
    if not cfg.exists():
        return False
    cp = configparser.ConfigParser()
    cp.read(cfg)
    return cp.has_section(section)
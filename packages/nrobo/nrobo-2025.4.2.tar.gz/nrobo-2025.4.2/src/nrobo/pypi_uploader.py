#!/usr/bin/env python3
"""
Auto‑fetch latest version from PyPI/TestPyPI,
bump version, build package, upload — with optional smoke‑test before real PyPI upload.

Usage:
  python build_and_publish.py [--level patch|minor|major] [--test] [--smoke] [--dry]
"""

import shutil
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
import requests
import tomlkit
from packaging.version import parse as parse_version
from termcolor import cprint

from nrobo.utils.update_version_utils import update_version_file

PYPROJECT = Path("pyproject.toml").resolve()
PACKAGE_NAME = "nrobo"
VERSION_FILE = Path("src").resolve() / PACKAGE_NAME / "version.py"


def bump_version(version: str, level: str = "patch") -> str:
    major, minor, patch = map(int, version.split("."))
    if level == "major":
        major += 1
        minor = patch = 0
    elif level == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def get_latest_pypi_version(package: str, test=False) -> str:
    url = (
        f"https://test.pypi.org/pypi/{package}/json"
        if test
        else f"https://pypi.org/pypi/{package}/json"
    )
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("info", {}).get("version", "0.0.0")
    except Exception as e:
        cprint(f"⚠️ Could not fetch latest version: {e}", "yellow")
    return "0.0.0"


def clear_dist_folder():
    dist_path = Path("dist")
    if dist_path.exists() and dist_path.is_dir():
        cprint("🧹 Clearing old dist/ directory...", "cyan")
        shutil.rmtree(dist_path)


def build_package():
    cprint("\n🔧 Building package...", "cyan")
    subprocess.run([sys.executable, "-m", "build"], check=True)


def upload_package(repo: str):
    cprint(f"\n📤 Uploading to {repo}...", "cyan")
    subprocess.run(
        [sys.executable, "-m", "twine", "upload", "--repository", repo, "dist/*"],
        check=True
    )


def smoke_test_install(package_name: str):
    """
    Simple smoke‑test: install the newly published package from TestPyPI
    in a fresh venv and try to import it.
    """
    cprint(f"\n🧪 Running smoke test install for: {package_name}", "cyan")
    venv_dir = Path(".tmp_test_env")
    # cleanup if exists
    if venv_dir.exists():
        shutil.rmtree(venv_dir)
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    pip = venv_dir / ("Scripts" if sys.platform.startswith("win") else "bin") / "pip"
    python = venv_dir / ("Scripts" if sys.platform.startswith("win") else "bin") / "python"

    subprocess.run([str(pip), "install", "--upgrade", "pip"], check=True)
    install_cmd = [
        str(pip),
        "install",
        "--index-url", "https://test.pypi.org/simple/",
        "--extra-index-url", "https://pypi.org/simple",
        package_name
    ]
    result = subprocess.run(install_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        cprint(f"❌ Failed to install from TestPyPI:\n{result.stderr}", "red")
        return False

    # Try import
    test_code = f"import {package_name}; print({package_name}.__version__)"
    result = subprocess.run([str(python), "-c", test_code], capture_output=True, text=True)
    if result.returncode != 0:
        cprint(f"❌ Import test failed:\n{result.stderr}", "red")
        return False

    cprint("✅ Smoke test passed!", "green")
    return True


def main():
    parser = ArgumentParser(description="Build and upload nrobo to PyPI/TestPyPI.")
    parser.add_argument(
        "--level", choices=["patch", "minor", "major"], default="patch"
    )
    parser.add_argument("--test", action="store_true", help="Upload to TestPyPI instead of PyPI")
    parser.add_argument("--smoke", action="store_true", help="After test upload, install & test package before real PyPI upload")
    parser.add_argument("--dry", action="store_true", help="Dry‑run (no build/upload)")
    parser.add_argument("--no-git-log", action="store_true", help="Skip showing git log")

    args = parser.parse_args()

    # Load current version
    doc = tomlkit.parse(PYPROJECT.read_text())
    local_version = doc["project"]["version"]

    latest_version = get_latest_pypi_version(PACKAGE_NAME, test=args.test)
    cprint(f"\n📦 Latest on {'TestPyPI' if args.test else 'PyPI'}: {latest_version}", "green")
    cprint(f"🧩 Local version: {local_version}", "cyan")

    if parse_version(local_version) <= parse_version(latest_version):
        new_version = bump_version(latest_version, args.level)
        cprint(f"⬆️  Bumping to version: {new_version}", "magenta")
    else:
        new_version = local_version
        cprint(f"✅ Local version is newer — staying at {local_version}", "green")

    update_version_file(version_file_path=VERSION_FILE, new_version=new_version)

    if not args.no_git_log:
        subprocess.run(["git", "log", "--oneline", "HEAD~5..HEAD"])

    if args.dry:
        cprint("💡 Dry‑run: exiting without build/upload", "yellow")
        return

    # persist version in pyproject
    doc["project"]["version"] = new_version
    PYPROJECT.write_text(tomlkit.dumps(doc))

    clear_dist_folder()
    build_package()

    repo = "testpypi" if args.test else "pypi"

    upload_package(repo)

    # If uploaded to TestPyPI and smoke‑test requested: test install
    if args.test and args.smoke:
        ok = smoke_test_install(PACKAGE_NAME)
        if not ok:
            cprint("❌ Smoke test failed — aborting real PyPI upload", "red")
            sys.exit(1)

        # If smoke‑test passed, then upload to real PyPI
        cprint("\n✅ Smoke‑test succeeded — uploading to real PyPI now.", "cyan")

        # Confirm upload
        cprint(f"\n⚠️ Ready to upload version {new_version} to {repo}.", "red")
        confirm = input("Do you want to continue? (y/N): ").strip().lower()
        if confirm not in ("y", "yes"):
            cprint("❌ Upload cancelled.", "red")
            return

        upload_package("pypi")

    cprint(f"\n🎉 Done. Version {new_version} uploaded to {repo}.", "green")


if __name__ == "__main__":
    main()

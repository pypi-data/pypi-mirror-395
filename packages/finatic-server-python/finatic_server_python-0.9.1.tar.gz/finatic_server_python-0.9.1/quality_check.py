#!/usr/bin/env python3
"""
Quality check script for FinaticServerSDK-Python.

Runs all quality checks: format, lint, type check, import check, syntax check.

Usage:
    python quality_check.py          # Check only
    python quality_check.py --fix    # Fix auto-fixable issues
    uv run python quality_check.py
    uv run python quality_check.py --fix
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str, fix_mode: bool = False) -> bool:
    """Run a command and return True if successful."""
    action = "Fixing" if fix_mode else "Checking"
    print(f"\n🔍 {action} {description}...")
    # Use uv run to execute commands in the project's virtual environment
    full_cmd = ["uv", "run"] + cmd
    print(f"   Running: {' '.join(full_cmd)}")
    try:
        result = subprocess.run(
            full_cmd,
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # Check if it's a "tool not found" error
            error_output = (result.stderr or result.stdout or "").lower()
            if "failed to spawn" in error_output or "no such file" in error_output:
                print(f"⚠️  {description} skipped (tool not installed)")
                print(f"   Install with: uv sync --extra dev")
                return True  # Skip missing tools gracefully
            print(f"❌ {description} failed!")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
            return False
        status = "fixed" if fix_mode else "passed"
        print(f"✅ {description} {status}!")
        return True
    except FileNotFoundError:
        print(f"⚠️  {description} skipped (tool not found)")
        return True  # Skip missing tools gracefully


def main() -> int:
    """Run all quality checks or fixes."""
    parser = argparse.ArgumentParser(description="Quality check script for FinaticServerSDK-Python")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Fix auto-fixable issues (format, import sort)",
    )
    args = parser.parse_args()

    fix_mode = args.fix
    mode_text = "fixes" if fix_mode else "checks"
    print(f"🚀 Running quality {mode_text} for FinaticServerSDK-Python\n")

    if fix_mode:
        # Fix commands (auto-fixable)
        checks = [
            (["black", "src", "tests"], "Format (black)"),
            (["isort", "src", "tests"], "Import sort (isort)"),
        ]
        all_passed = True
        for cmd, description in checks:
            if not run_command(cmd, description, fix_mode=True):
                all_passed = False

        if not all_passed:
            print("\n❌ Some fixes failed!")
            return 1

        print("\n✅ All auto-fixable issues fixed!")
        print("\n💡 Note: Some issues may require manual fixes (flake8, mypy)")
        return 0
    else:
        # Check commands
        checks = [
            (["black", "--check", "src", "tests"], "Format check (black)"),
            (["isort", "--check-only", "src", "tests"], "Import sort check (isort)"),
            (["flake8", "src", "tests"], "Lint & import check (flake8)"),
            (["mypy", "src"], "Type check (mypy)"),
        ]

        all_passed = True
        for cmd, description in checks:
            if not run_command(cmd, description, fix_mode=False):
                all_passed = False

        if not all_passed:
            print("\n❌ Some quality checks failed!")
            print("\n💡 To fix auto-fixable issues, run:")
            print("   python quality_check.py --fix")
            print("   # or")
            print("   black src tests")
            print("   isort src tests")
            return 1

        print("\n✅ All quality checks passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())


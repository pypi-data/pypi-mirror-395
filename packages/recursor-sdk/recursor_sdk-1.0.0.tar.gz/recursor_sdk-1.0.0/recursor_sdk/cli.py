#!/usr/bin/env python3
"""
Recursor SDK CLI - Publishing and management tools
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result


def check_dependencies():
    """Check if required tools are installed"""
    tools = {
        "python3": "python3 --version",
        "build": "python3 -m pip show build",
        "twine": "python3 -m pip show twine",
    }
    
    missing = []
    for tool, check_cmd in tools.items():
        result = run_command(check_cmd, check=False)
        if result.returncode != 0:
            missing.append(tool)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("📦 Install with: python3 -m pip install build twine")
        sys.exit(1)
    
    print("✅ All dependencies installed")


def build_package():
    """Build the package"""
    print("🔨 Building package...")
    run_command("python3 -m build")
    print("✅ Build complete")


def check_package():
    """Check package with twine"""
    print("🔍 Checking package...")
    result = run_command("python3 -m twine check dist/*")
    if "PASSED" in result.stdout:
        print("✅ Package checks passed")
        return True
    return False


def publish_to_testpypi():
    """Publish to Test PyPI"""
    print("📤 Publishing to Test PyPI...")
    run_command("python3 -m twine upload --repository testpypi dist/*")
    print("✅ Published to Test PyPI!")
    print("📝 Test installation: pip install -i https://test.pypi.org/simple/ recursor-sdk")


def publish_to_pypi():
    """Publish to production PyPI"""
    print("📤 Publishing to PyPI...")
    run_command("python3 -m twine upload dist/*")
    print("✅ Published to PyPI!")
    print("📝 Install with: pip install recursor-sdk")


def clean_build():
    """Clean build artifacts"""
    print("🧹 Cleaning build artifacts...")
    run_command("rm -rf dist/ build/ *.egg-info", check=False)
    print("✅ Clean complete")


def show_version():
    """Show current package version"""
    import re
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "r") as f:
        content = f.read()
    match = re.search(r'version = "([^"]+)"', content)
    if match:
        version = match.group(1)
        print(f"📦 Current version: {version}")
    else:
        print("❌ Could not find version in pyproject.toml")
        sys.exit(1)


def bump_version(part):
    """Bump version number"""
    import re
    
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    
    with open(pyproject_path, "r") as f:
        content = f.read()
    
    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        print("❌ Could not find version in pyproject.toml")
        sys.exit(1)
    
    current_version = match.group(1)
    parts = [int(x) for x in current_version.split(".")]
    
    if part == "major":
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif part == "minor":
        parts[1] += 1
        parts[2] = 0
    elif part == "patch":
        parts[2] += 1
    else:
        print(f"❌ Invalid version part: {part}. Use: major, minor, or patch")
        sys.exit(1)
    
    new_version = ".".join(map(str, parts))
    
    # Update pyproject.toml
    content = re.sub(
        r'version = "[^"]+"',
        f'version = "{new_version}"',
        content
    )
    
    with open(pyproject_path, "w") as f:
        f.write(content)
    
    print(f"✅ Version bumped: {current_version} → {new_version}")


def main():
    parser = argparse.ArgumentParser(
        description="Recursor SDK CLI - Publishing and management tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s build                    # Build the package
  %(prog)s publish --test           # Publish to Test PyPI
  %(prog)s publish                  # Publish to production PyPI
  %(prog)s version                  # Show current version
  %(prog)s version bump patch       # Bump patch version
  %(prog)s clean                    # Clean build artifacts
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Build the package")
    
    # Publish command
    publish_parser = subparsers.add_parser("publish", help="Publish to PyPI")
    publish_parser.add_argument(
        "--test",
        action="store_true",
        help="Publish to Test PyPI instead of production"
    )
    publish_parser.add_argument(
        "--skip-check",
        action="store_true",
        help="Skip package check before publishing"
    )
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check package with twine")
    
    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean build artifacts")
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Version management")
    version_parser.add_argument(
        "action",
        nargs="?",
        choices=["show", "bump"],
        default="show",
        help="Action: show current version or bump version"
    )
    version_parser.add_argument(
        "part",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Version part to bump (major, minor, patch)"
    )
    
    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify setup (check dependencies)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Change to SDK directory
    sdk_dir = Path(__file__).parent.parent
    os.chdir(sdk_dir)
    
    if args.command == "verify":
        check_dependencies()
    
    elif args.command == "build":
        check_dependencies()
        clean_build()
        build_package()
        check_package()
    
    elif args.command == "check":
        check_package()
    
    elif args.command == "clean":
        clean_build()
    
    elif args.command == "version":
        if args.action == "show":
            show_version()
        elif args.action == "bump":
            if not args.part:
                print("❌ Please specify version part: major, minor, or patch")
                sys.exit(1)
            bump_version(args.part)
    
    elif args.command == "publish":
        check_dependencies()
        
        if not args.skip_check:
            if not Path("dist").exists():
                print("📦 No dist/ directory found. Building package first...")
                clean_build()
                build_package()
            
            if not check_package():
                print("❌ Package check failed. Fix issues before publishing.")
                sys.exit(1)
        
        if args.test:
            publish_to_testpypi()
        else:
            # Confirm before publishing to production
            print("⚠️  You are about to publish to PRODUCTION PyPI")
            response = input("Continue? (yes/no): ")
            if response.lower() not in ["yes", "y"]:
                print("❌ Publishing cancelled")
                sys.exit(0)
            publish_to_pypi()


if __name__ == "__main__":
    main()


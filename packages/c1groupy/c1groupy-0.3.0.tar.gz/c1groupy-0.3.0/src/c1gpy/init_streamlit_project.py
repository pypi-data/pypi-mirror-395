#!/usr/bin/env python3
"""Script to initialize a new Streamlit multi-page project with Docker support."""

import argparse
import subprocess
import sys
from pathlib import Path


def get_template_dir() -> Path:
    """Get the path to the template files directory."""
    return Path(__file__).parent / "streamlit_project_files"


def run_command(
    cmd: list[str], cwd: Path, check: bool = True
) -> subprocess.CompletedProcess:
    """Run a command and handle errors."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, check=check, capture_output=True, text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)


def copy_template_file(
    template_path: Path,
    dest_path: Path,
    project_name: str = None,
    author_email: str = None,
) -> None:
    """Copy a template file, optionally replacing placeholders."""
    content = template_path.read_text()

    # Replace placeholders
    if project_name and "{project_name}" in content:
        content = content.format(project_name=project_name)
    if author_email and "{author_email}" in content:
        content = content.replace("{author_email}", author_email)

    dest_path.write_text(content)

    # Preserve executable permissions
    if template_path.stat().st_mode & 0o111:
        dest_path.chmod(0o755)


def create_project_structure(
    project_path: Path, project_name: str, author_email: str
) -> None:
    """Create the project directory structure and files."""
    template_dir = get_template_dir()

    if not template_dir.exists():
        print(f"Error: Template directory not found at {template_dir}", file=sys.stderr)
        sys.exit(1)

    # Create directories
    (project_path / "src" / "app" / "pages").mkdir(parents=True, exist_ok=True)
    (project_path / "tests").mkdir(exist_ok=True)

    # Copy static files (some may need author_email replacement)
    static_files = [
        ".gitignore",
        ".pre-commit-config.yaml",
        "docker-compose.yml",
        "src/entrypoint.sh",
        "src/app/pages/home.py",
        "src/app/pages/1_Page_1.py",
        "src/app/pages/2_Page_2.py",
        "tests/test_example.py",
    ]

    for file_path in static_files:
        src = template_dir / file_path
        dest = project_path / file_path
        if src.exists():
            copy_template_file(src, dest, author_email=author_email)

    # Copy Dockerfile separately (needs author_email)
    src = template_dir / "Dockerfile"
    dest = project_path / "Dockerfile"
    if src.exists():
        copy_template_file(src, dest, author_email=author_email)

    # Copy template files (with placeholder replacement)
    template_files = {
        "pyproject.toml.template": "pyproject.toml",
        "README.md.template": "README.md",
        "src/app/App.py.template": "src/app/App.py",
    }

    for template_name, dest_name in template_files.items():
        src = template_dir / template_name
        dest = project_path / dest_name
        if src.exists():
            copy_template_file(src, dest, project_name, author_email)

    # Create __init__.py files
    (project_path / "src" / "app" / "__init__.py").touch()
    (project_path / "src" / "app" / "pages" / "__init__.py").touch()
    (project_path / "tests" / "__init__.py").touch()


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Initialize a new Streamlit multi-page project with Docker support"
    )
    parser.add_argument("project_name", help="Name of the project to create")
    parser.add_argument(
        "--path",
        default=".",
        help="Path where the project should be created (default: current directory)",
    )
    parser.add_argument(
        "--author-email", default="", help="Author email address for project metadata"
    )

    args = parser.parse_args()

    # Validate project name
    if not args.project_name.replace("-", "").replace("_", "").isalnum():
        print(
            "Error: Project name should only contain alphanumeric characters, hyphens, and underscores",
            file=sys.stderr,
        )
        sys.exit(1)

    # Create project path
    base_path = Path(args.path).resolve()
    project_path = base_path / args.project_name

    if project_path.exists():
        print(f"Error: Directory '{project_path}' already exists", file=sys.stderr)
        sys.exit(1)

    print(f"Creating Streamlit project: {args.project_name}")
    print(f"Location: {project_path}")

    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)

    # Initialize with uv
    print("\nInitializing project with uv...")
    run_command(["uv", "init", "--no-readme", args.project_name], cwd=base_path)

    # Create project structure
    print("\nCreating project structure...")
    create_project_structure(project_path, args.project_name, args.author_email)

    # Initialize git repository
    print("\nInitializing git repository...")
    run_command(["git", "init"], cwd=project_path)
    run_command(["git", "add", "."], cwd=project_path)
    run_command(["git", "commit", "-m", "Initial commit"], cwd=project_path)

    # Install pre-commit hooks
    print("\nInstalling pre-commit hooks...")
    # Check if pre-commit is available
    pre_commit_check = run_command(
        ["which", "pre-commit"], cwd=project_path, check=False
    )

    if pre_commit_check.returncode == 0:
        run_command(["pre-commit", "install"], cwd=project_path)
        print("✅ Pre-commit hooks installed successfully")
    else:
        print("⚠️  pre-commit not found. Install it with: pip install pre-commit")
        print("   Then run: cd {} && pre-commit install".format(args.project_name))

    print(f"\n✅ Project '{args.project_name}' created successfully!")
    print("\nNext steps:")
    print(f"  cd {args.project_name}")
    print("  uv sync")
    print("  uv run streamlit run src/app/App.py")
    print("\nOr use Docker:")
    print(f"  cd {args.project_name}")
    print("  docker-compose up --build")


if __name__ == "__main__":
    main()

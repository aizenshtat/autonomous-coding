"""
Prompt Loading Utilities
========================

Functions for loading prompt templates from the prompts directory.
"""

import shutil
from pathlib import Path


PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(name: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = PROMPTS_DIR / f"{name}.md"
    return prompt_path.read_text()


def get_initializer_prompt() -> str:
    """Load the initializer prompt."""
    return load_prompt("initializer_prompt")


def get_coding_prompt() -> str:
    """Load the coding agent prompt."""
    return load_prompt("coding_prompt")


def copy_spec_to_project(
    project_dir: Path,
    spec_file: str = "app_spec.txt",
    extra_files: list[str] = None
) -> None:
    """
    Copy the spec file and any extra files into the project directory for the agent to read.

    Args:
        project_dir: Project directory path
        spec_file: Name of spec file from prompts/ directory (default: app_spec.txt)
        extra_files: Additional files to copy from prompts/ directory
    """
    if extra_files is None:
        extra_files = []

    # Copy the spec file (always to app_spec.txt in project)
    spec_source = PROMPTS_DIR / spec_file
    spec_dest = project_dir / "app_spec.txt"
    if not spec_dest.exists():
        shutil.copy(spec_source, spec_dest)
        print(f"Copied {spec_source.name} to project directory as app_spec.txt")

    # Copy any extra files
    for extra_file in extra_files:
        extra_source = PROMPTS_DIR / extra_file
        extra_dest = project_dir / extra_file
        if not extra_dest.exists():
            shutil.copy(extra_source, extra_dest)
            print(f"Copied {extra_file} to project directory")

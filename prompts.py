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


def is_dashboard_project(project_dir: Path) -> bool:
    """Check if this is a dashboard monitoring project based on directory name."""
    return "dashboard" in project_dir.name.lower() or "monitor" in project_dir.name.lower()


def copy_spec_to_project(project_dir: Path) -> None:
    """
    Copy the appropriate spec file into the project directory for the agent to read.
    For dashboard projects, also copy AGENT_CONTEXT.md.
    """
    # Determine which spec to use
    if is_dashboard_project(project_dir):
        spec_source = PROMPTS_DIR / "monitoring_dashboard_spec.txt"
        print("📊 Detected dashboard project - using monitoring_dashboard_spec.txt")

        # Copy AGENT_CONTEXT.md for dashboard projects
        context_source = PROMPTS_DIR / "AGENT_CONTEXT.md"
        context_dest = project_dir / "AGENT_CONTEXT.md"
        if not context_dest.exists():
            shutil.copy(context_source, context_dest)
            print("Copied AGENT_CONTEXT.md to project directory")
    else:
        spec_source = PROMPTS_DIR / "app_spec.txt"
        print("🚀 Using standard app_spec.txt")

    # Copy the spec file
    spec_dest = project_dir / "app_spec.txt"
    if not spec_dest.exists():
        shutil.copy(spec_source, spec_dest)
        print(f"Copied {spec_source.name} to project directory")

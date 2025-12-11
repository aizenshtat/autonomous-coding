#!/usr/bin/env python3
"""
Autonomous Coding Agent Demo
============================

A minimal harness demonstrating long-running autonomous coding with Claude.
This script implements the two-agent pattern (initializer + coding agent) and
incorporates all the strategies from the long-running agents guide.

Example Usage:
    python autonomous_agent_demo.py --project-dir ./claude_clone_demo
    python autonomous_agent_demo.py --project-dir ./claude_clone_demo --max-iterations 5
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from agent import run_autonomous_agent


class TeeOutput:
    """Write to both terminal and file simultaneously."""
    def __init__(self, terminal, file):
        self.terminal = terminal
        self.file = file

    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)
        self.flush()

    def flush(self):
        self.terminal.flush()
        self.file.flush()

    def isatty(self):
        return self.terminal.isatty()

# Load environment variables from .env file
load_dotenv()


# Configuration
DEFAULT_MODEL = "claude-opus-4-5"


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Autonomous Coding Agent Demo - Long-running agent harness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use monitoring dashboard spec (auto-creates generations/monitoring_dashboard/)
  python autonomous_agent_demo.py \\
    --spec monitoring_dashboard_spec.txt \\
    --extra-files AGENT_CONTEXT.md

  # Use custom project name
  python autonomous_agent_demo.py \\
    --spec monitoring_dashboard_spec.txt \\
    --project-name my_dashboard \\
    --extra-files AGENT_CONTEXT.md

  # Use explicit project directory
  python autonomous_agent_demo.py --project-dir ./claude_clone

  # Limit iterations for testing
  python autonomous_agent_demo.py \\
    --spec monitoring_dashboard_spec.txt \\
    --max-iterations 5

  # Use a specific model
  python autonomous_agent_demo.py \\
    --spec monitoring_dashboard_spec.txt \\
    --model claude-sonnet-4-5-20250929

Environment Variables:
  CLAUDE_OAUTH_TOKEN    Your Claude OAuth token (required)
        """,
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        default=None,
        help="Directory for the project. If not specified, derives from --spec name. Relative paths automatically placed in generations/ directory.",
    )

    parser.add_argument(
        "--project-name",
        type=str,
        default=None,
        help="Project name (default: derived from spec file name, e.g., monitoring_dashboard_spec.txt -> monitoring_dashboard)",
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of agent iterations (default: unlimited)",
    )

    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )

    parser.add_argument(
        "--spec",
        type=str,
        default="app_spec.txt",
        help="Spec file to use from prompts/ directory (default: app_spec.txt)",
    )

    parser.add_argument(
        "--extra-files",
        type=str,
        nargs="*",
        default=[],
        help="Additional files to copy from prompts/ directory (e.g., AGENT_CONTEXT.md)",
    )

    parser.add_argument(
        "--log-file",
        type=str,
        default="live-output.txt",
        help="Log file name in project directory for real-time output (default: live-output.txt)",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    # Check for OAuth token
    if not os.environ.get("CLAUDE_OAUTH_TOKEN"):
        print("Error: CLAUDE_OAUTH_TOKEN environment variable not set")
        print("\nSet up your token using: claude setup-token")
        print("\nThen set it:")
        print("  export CLAUDE_OAUTH_TOKEN='your-token-here'")
        return

    # Determine project directory
    if args.project_dir:
        # User specified project directory explicitly
        project_dir = args.project_dir
    elif args.project_name:
        # User specified project name
        project_dir = Path(args.project_name)
    else:
        # Derive from spec file name (remove _spec suffix)
        spec_name = args.spec.replace(".txt", "").replace("_spec", "")
        project_dir = Path(spec_name)

    # Automatically place projects in generations/ directory unless already specified
    if not str(project_dir).startswith("generations/"):
        # Convert relative paths to be under generations/
        if project_dir.is_absolute():
            # If absolute path, use as-is
            pass
        else:
            # Prepend generations/ to relative paths
            project_dir = Path("generations") / project_dir

    # Create project directory for log file
    project_dir.mkdir(parents=True, exist_ok=True)

    # Redirect stdout/stderr to log file if specified (tee to both terminal and file)
    if args.log_file:
        log_path = project_dir / args.log_file
        print(f"Logging output to: {log_path}")
        log_file = open(log_path, "w", buffering=1)  # Line buffered
        sys.stdout = TeeOutput(sys.stdout, log_file)
        sys.stderr = TeeOutput(sys.stderr, log_file)

    # Run the agent
    try:
        asyncio.run(
            run_autonomous_agent(
                project_dir=project_dir,
                model=args.model,
                max_iterations=args.max_iterations,
                spec_file=args.spec,
                extra_files=args.extra_files,
            )
        )
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        print("To resume, run the same command again")
    except Exception as e:
        print(f"\nFatal error: {e}")
        raise


if __name__ == "__main__":
    main()

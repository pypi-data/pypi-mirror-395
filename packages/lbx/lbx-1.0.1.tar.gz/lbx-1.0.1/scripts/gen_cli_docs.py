#!/usr/bin/env python3
"""
MkDocs hook to generate CLI documentation from Click commands.

This script processes markdown files containing !!!cli directives and replaces
them with auto-generated command help text.

Syntax:
    !!!cli module.path:command_name

Example:
    !!!cli package.cli:package
"""

from __future__ import annotations

import importlib
import logging
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import click  # type: ignore[import-untyped]
import mkdocs_gen_files  # type: ignore[import-untyped]

if TYPE_CHECKING:
    from collections.abc import Iterator

# =============================================================================
# Constants
# =============================================================================
ROOT_DIR = Path(__file__).parent.parent.resolve()
DOCS_DIR = ROOT_DIR / "docs"
CLI_DIRECTIVE_PATTERN = re.compile(r"^!!!cli\s+([\w\.]+):(\w+)\s*$", re.MULTILINE)
FILE_ENCODING = "utf-8"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


# =============================================================================
# CLI Documentation Generation
# =============================================================================
def format_command_help(cmd: click.Command, prefix: str = "") -> str:
    """
    Recursively format Click command and subcommands as markdown.

    Args:
        cmd: Click command object to document
        prefix: Command prefix for nested commands (e.g., "package vault")

    Returns:
        Formatted markdown string with command help

    Raises:
        RuntimeError: If command context cannot be created
    """
    full_cmd = f"{prefix} {cmd.name}".strip() if cmd.name else prefix.strip()

    if not full_cmd:
        raise RuntimeError("Command must have a name")

    try:
        ctx = click.Context(cmd, info_name=full_cmd)
        help_text = cmd.get_help(ctx)
    except Exception as e:
        raise RuntimeError(f"Failed to get help for command '{full_cmd}': {e}") from e

    parts = [
        f"## `{full_cmd}`\n",
        "```",
        help_text,
        "```\n",
    ]

    # Recursively process subcommands for Groups
    if isinstance(cmd, click.Group):
        try:
            subcommands = sorted(cmd.list_commands(ctx))
            for sub_name in subcommands:
                sub_cmd = cmd.get_command(ctx, sub_name)
                if sub_cmd:
                    parts.append(format_command_help(sub_cmd, full_cmd))
        except Exception as e:
            logger.warning("Failed to process subcommands for '%s': %s", full_cmd, e)

    return "\n".join(parts)


def generate_cli_docs(module_path: str, command_name: str) -> str:
    """
    Import CLI command and generate markdown documentation.

    Args:
        module_path: Python module path (e.g., "package.cli")
        command_name: Command attribute name (e.g., "package")

    Returns:
        Generated markdown documentation

    Raises:
        ImportError: If module cannot be imported
        AttributeError: If command not found in module
        ValueError: If command is not a Click command or inputs are invalid
    """
    if not module_path or not command_name:
        raise ValueError("Both module_path and command_name must be non-empty")

    logger.info("Generating docs for %s:%s", module_path, command_name)

    try:
        module = importlib.import_module(module_path)
    except ImportError as e:
        raise ImportError(f"Cannot import module '{module_path}': {e}") from e

    if not hasattr(module, command_name):
        raise AttributeError(f"Command '{command_name}' not found in module '{module_path}'")

    cli_cmd = getattr(module, command_name)

    if not isinstance(cli_cmd, click.Command):
        raise ValueError(f"'{module_path}:{command_name}' is not a Click command (got {type(cli_cmd).__name__})")

    return format_command_help(cli_cmd)


# =============================================================================
# Markdown Processing
# =============================================================================
def process_cli_directive(match: re.Match[str]) -> str:
    """
    Process a single !!!cli directive and generate documentation.

    Args:
        match: Regex match object containing module_path and command_name

    Returns:
        Generated CLI documentation or error message
    """
    module_path, command_name = match.groups()

    try:
        return generate_cli_docs(module_path, command_name)
    except ImportError as e:
        logger.error("Import error for %s:%s - %s", module_path, command_name, e)
        return f"> **Error:** Module import failed for `{module_path}:{command_name}`\n>\n> {e}"
    except AttributeError as e:
        logger.error("Attribute error for %s:%s - %s", module_path, command_name, e)
        return f"> **Error:** Invalid command `{module_path}:{command_name}`\n>\n> {e}"
    except ValueError as e:
        logger.error("Validation error for %s:%s - %s", module_path, command_name, e)
        return f"> **Error:** Invalid command `{module_path}:{command_name}`\n>\n> {e}"
    except Exception as e:
        logger.exception("Unexpected error generating CLI docs for %s:%s", module_path, command_name)
        return f"> **Error:** Failed to generate docs for `{module_path}:{command_name}`\n>\n> {e}"


def process_markdown(md_path: Path) -> str:
    """
    Read markdown file and replace !!!cli directives with generated docs.

    Args:
        md_path: Path to markdown file

    Returns:
        Processed markdown content

    Raises:
        FileNotFoundError: If markdown file doesn't exist
        UnicodeDecodeError: If file encoding is invalid
        OSError: If file cannot be read
    """
    logger.debug("Processing %s", md_path.relative_to(ROOT_DIR))

    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    if not md_path.is_file():
        raise OSError(f"Path is not a file: {md_path}")

    try:
        content = md_path.read_text(encoding=FILE_ENCODING)
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding,
            e.object,
            e.start,
            e.end,
            f"Invalid {FILE_ENCODING} encoding in {md_path}: {e.reason}",
        ) from e
    except OSError as e:
        raise OSError(f"Failed to read {md_path}: {e}") from e

    if not content:
        logger.warning("Empty file: %s", md_path.relative_to(ROOT_DIR))
        return content

    return CLI_DIRECTIVE_PATTERN.sub(process_cli_directive, content)


def write_docs(original_path: Path, content: str) -> None:
    """
    Write generated documentation to MkDocs virtual file system.

    Args:
        original_path: Original markdown file path
        content: Processed markdown content

    Raises:
        ValueError: If path is outside docs directory or invalid
    """
    if not original_path.is_relative_to(DOCS_DIR):
        raise ValueError(f"Path {original_path} is outside docs directory {DOCS_DIR}")

    rel_path = original_path.relative_to(DOCS_DIR)

    # Prevent path traversal attacks
    if ".." in rel_path.parts:
        raise ValueError(f"Invalid relative path with parent references: {rel_path}")

    logger.debug("Writing to virtual FS: %s", rel_path)

    with mkdocs_gen_files.open(rel_path, "w") as f:
        f.write(content)


# =============================================================================
# File Discovery
# =============================================================================
def read_markdown_file_safely(md_file: Path) -> str | None:
    """
    Safely read markdown file content.

    Args:
        md_file: Path to markdown file

    Returns:
        File content if successful, None if error occurred
    """
    try:
        return md_file.read_text(encoding=FILE_ENCODING)
    except PermissionError as e:
        logger.warning("Permission denied for %s: %s", md_file.relative_to(ROOT_DIR), e)
        return None
    except UnicodeDecodeError as e:
        logger.warning("Encoding error in %s: %s", md_file.relative_to(ROOT_DIR), e)
        return None
    except OSError as e:
        logger.warning("Failed to read %s: %s", md_file.relative_to(ROOT_DIR), e)
        return None


def find_markdown_files_with_cli_directives() -> Iterator[Path]:
    """
    Find all markdown files containing !!!cli directives.

    Yields:
        Paths to markdown files with CLI directives

    Raises:
        NotADirectoryError: If DOCS_DIR doesn't exist or isn't a directory
    """
    if not DOCS_DIR.exists():
        raise NotADirectoryError(f"Documentation directory does not exist: {DOCS_DIR}")

    if not DOCS_DIR.is_dir():
        raise NotADirectoryError(f"Documentation path is not a directory: {DOCS_DIR}")

    for md_file in DOCS_DIR.rglob("*.md"):
        content = read_markdown_file_safely(md_file)
        if content and "!!!cli" in content:
            yield md_file


# =============================================================================
# File Processing
# =============================================================================
def process_single_file(md_file: Path) -> bool:
    """
    Process a single markdown file with CLI directives.

    Args:
        md_file: Path to markdown file

    Returns:
        True if successful, False otherwise
    """
    try:
        new_content = process_markdown(md_file)
        write_docs(md_file, new_content)
        logger.info("✓ Processed %s", md_file.relative_to(ROOT_DIR))
        return True
    except FileNotFoundError as e:
        logger.error("✗ File not found: %s - %s", md_file.relative_to(ROOT_DIR), e)
        return False
    except (UnicodeDecodeError, OSError) as e:
        logger.error("✗ I/O error processing %s - %s", md_file.relative_to(ROOT_DIR), e)
        return False
    except ValueError as e:
        logger.error("✗ Validation error for %s - %s", md_file.relative_to(ROOT_DIR), e)
        return False
    except Exception:
        logger.exception("✗ Unexpected error processing %s", md_file.relative_to(ROOT_DIR))
        return False


# =============================================================================
# Main Entry Point
# =============================================================================
def main() -> int:
    """
    Process all markdown files with !!!cli directives.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    logger.info("Starting CLI documentation generation")
    logger.info("Root directory: %s", ROOT_DIR)
    logger.info("Docs directory: %s", DOCS_DIR)

    try:
        files_processed = 0
        files_failed = 0

        for md_file in find_markdown_files_with_cli_directives():
            if process_single_file(md_file):
                files_processed += 1
            else:
                files_failed += 1

        logger.info(
            "Completed: %d file(s) processed, %d file(s) failed",
            files_processed,
            files_failed,
        )

        # Return error if any files failed
        return 1 if files_failed > 0 else 0

    except NotADirectoryError as e:
        logger.error("Configuration error: %s", e)
        return 1
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        return 130
    except Exception:
        logger.exception("Unexpected error during documentation generation")
        return 1


# =============================================================================
# Script Execution
# =============================================================================
sys.exit(main())

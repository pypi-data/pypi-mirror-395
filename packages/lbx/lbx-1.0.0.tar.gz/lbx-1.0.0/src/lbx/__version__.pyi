# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

# Type stubs for dynamically generated version information (hatch-vcs)

# =============================================================================
# PEP 440-Compliant Version String
# =============================================================================
# Examples:
#   - Release:     "1.0.0"
#   - Development: "1.0.0.dev1+g97717df2f.d20250905"

version: str
__version__: str

# =============================================================================
# Version Tuple (Programmatic Access)
# =============================================================================
# Examples:
#   - Release:     (1, 0, 0)
#   - Development: (1, 0, 0, "dev1", "g97717df2f.d20250905")

version_tuple: tuple[int, int, int] | tuple[int, int, int, str, str]
__version_tuple__: tuple[int, int, int] | tuple[int, int, int, str, str]

# =============================================================================
# Git Commit ID
# =============================================================================
# - Development builds: Short commit hash (e.g., "g97717df2f")
# - Release builds:     None

commit_id: str | None
__commit_id__: str | None

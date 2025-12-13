# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

"""Public Lbx API exposure.

This module re-exports the high-level Lbx vault manager so users can import
it directly from :mod:`lbx` rather than navigating internal packages. The
internal structure remains hidden; only stable API surfaces are exposed here.
"""

from lbx.core import Lbx

__all__ = ["Lbx"]

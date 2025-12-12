from __future__ import annotations

"""repyter public API.

This package exports the main report-building primitives `Report` and `Section`.
The implementation lives in `repyter.report` to keep the public namespace clean.
"""

from .report import Report, Section

__all__ = ["Report", "Section"]
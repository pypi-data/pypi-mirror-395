from __future__ import annotations

"""
Core report-building primitives for the repyter package.

This module exposes two public types:
- Section: a lightweight container for a section title and a list of HTML blocks
- Report: the main orchestrator used to assemble sections and render an HTML file

No external rendering engines are required at runtime other than Jinja2 and
Pandas (for the DataFrame-to-HTML helper). Plotly and Matplotlib are optional
and only needed if you call their respective helpers.
"""

from dataclasses import dataclass, field
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd
from base64 import b64encode
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Optional imports (only used by helper methods). These remain optional to keep
# the core package lightweight. Each helper will raise a friendly RuntimeError
# if the corresponding library is not installed.
try:  # pragma: no cover - availability depends on user environment
    import plotly.io as pio  # type: ignore
except Exception:  # pragma: no cover
    pio = None  # type: ignore

try:  # pragma: no cover - availability depends on user environment
    import matplotlib.pyplot as plt  # type: ignore
except Exception:  # pragma: no cover
    plt = None  # type: ignore


@dataclass
class Section:
    """A logical section of a report containing a title and a list of HTML blocks.

    Attributes
    ----------
    title: str
        Human-readable section title displayed in the output HTML.
    blocks: list[str]
        Ordered list of HTML fragments. Each fragment is appended as-is during
        rendering. Use helpers like `Report.table_from_df` to build safe HTML
        snippets.
    """

    title: str
    blocks: List[str] = field(default_factory=list)


class Report:
    """Report builder that renders to a single self-contained HTML file.

    Usage example
    -------------
    >>> from repyter import Report
    >>> r = Report(title="Example")
    >>> r.set_intro(Report.alert("Generated with repyter"))
    >>> sec = r.add_section("Summary")
    >>> import pandas as pd
    >>> df = pd.DataFrame({"Metric": ["Rows"], "Value": [10]})
    >>> r.add_block(Report.table_from_df(df), section=sec)
    >>> _ = r.render("reports/report.html")

    Notes
    -----
    - Plotly and Matplotlib helpers are optional and only work if those
      libraries are installed. Otherwise a clear RuntimeError is raised.
    - This class is intentionally small and framework-free so it can be used
      directly from Python scripts and debuggers.
    """

    def __init__(
        self,
        template_path: str = str((Path(__file__).parent / "template.html").absolute()),
        use_plotly_cdn: bool = True,
        title: Optional[str] = None,
    ) -> None:
        self.template_path = Path(template_path)
        self.title = title or "Report"
        self.use_plotly_cdn = use_plotly_cdn
        self.sections: List[Section] = []
        self.intro_html: str = ""

        # Prepare a Jinja2 environment bound to the template directory. We load
        # the template at construction time to fail-fast if it is missing.
        self._env = Environment(
            loader=FileSystemLoader(str(self.template_path.parent.resolve())),
            autoescape=select_autoescape(["html", "xml"]),
            enable_async=False,
        )
        self._template = self._env.get_template(self.template_path.name)
        self._current_block: Optional[Section] = None

    # ------------------------- High-level API -------------------------
    def set_intro(self, html: str) -> "Report":
        """Set an introductory HTML fragment displayed at the top of the report.

        Parameters
        ----------
        html: str
            Raw HTML to place above all sections. You are responsible for
            sanitization if the content originates from untrusted sources.
        """
        self.intro_html = html
        return self

    def add_section(self, title: str) -> Section:
        """Create and append a new section.

        The new section becomes the default target for subsequent `add_block`
        calls until another section is added.
        """
        sec = Section(title=title)
        self.sections.append(sec)
        self._current_block = sec
        return sec

    def add_block(self, block: Union[str, pd.DataFrame], section: Optional[Section] = None) -> "Report":
        """Append an HTML block (or DataFrame) to a section.

        Parameters
        ----------
        block: str | pandas.DataFrame
            - If `str`, it is inserted as raw HTML.
            - If `DataFrame`, it is converted to an HTML table using
              `table_from_df` with default formatting.
        section: Section | None
            If omitted, the most recently added section is used.
        """
        if section is None:
            section = self._current_block
        if section is None:
            raise ValueError("No section available. Call add_section() first or pass a section explicitly.")

        if isinstance(block, pd.DataFrame):
            html = self.table_from_df(block)
        else:
            html = block
        section.blocks.append(html)
        return self

    # ---------------------------- Helpers ----------------------------
    @staticmethod
    def table_from_df(df: pd.DataFrame, float_fmt: str = "{:,.4f}") -> str:
        """Convert a DataFrame to a styled HTML table.

        - Float columns are formatted using `float_fmt`.
        - The output uses class "table" (not Pandas' default "dataframe") to
          match CSS in `template.html` and keep tests deterministic across
          Pandas versions.
        """
        fmt_df = df.copy()
        for c in fmt_df.columns:
            if pd.api.types.is_float_dtype(fmt_df[c]):
                fmt_df[c] = fmt_df[c].map(lambda x: float_fmt.format(x) if pd.notna(x) else "")
        html = fmt_df.to_html(index=False, border=0, classes="table")
        # Pandas always prefixes the class list with "dataframe". Normalize it
        # to exactly class="table" for stable styling and testing.
        html = html.replace('class="dataframe table"', 'class="table"')
        html = html.replace('class="dataframe"', 'class="table"')
        return html

    @staticmethod
    def html_block(html: str) -> str:
        """Return raw HTML unchanged (semantic helper)."""
        return html

    @staticmethod
    def plotly_div(fig, width: str = "100%", height: str = "auto") -> str:
        """Return the HTML <div> for a Plotly figure.

        Requires Plotly. If not installed, raises RuntimeError.
        """
        if pio is None:
            raise RuntimeError("plotly is not installed. pip install plotly")
        return pio.to_html(
            fig,
            include_plotlyjs=False,
            full_html=False,
            default_width=width,
            default_height=height,
        )

    @staticmethod
    def mpl_img(fig, fmt: str = "png", dpi: int = 144, alt: str = "figure") -> str:
        """Return a base64-embedded <img> for a Matplotlib figure.

        Requires Matplotlib. If not installed, raises RuntimeError.
        """
        if plt is None:
            raise RuntimeError("matplotlib is not installed. pip install matplotlib")
        buf = BytesIO()
        fig.savefig(buf, format=fmt, dpi=dpi, bbox_inches="tight")
        try:  # best-effort close to free memory in long-running reports
            import matplotlib.pyplot as _plt  # type: ignore
            _plt.close(fig)
        except Exception:  # pragma: no cover - safety net only
            pass
        encoded = b64encode(buf.getvalue()).decode("ascii")
        return (
            f"<figure class='figure'><img class='img' alt='{alt}' "
            f"src='data:image/{fmt};base64,{encoded}' />"
            f"<figcaption class='caption'>{alt}</figcaption></figure>"
        )

    @staticmethod
    def image_src(path: str, alt: str = "image") -> str:
        """Return an HTML <img> tag pointing to a local or remote path."""
        return (
            f"<figure class='figure'><img class='img' alt='{alt}' src='{path}' />"
            f"<figcaption class='caption'>{alt}</figcaption></figure>"
        )

    @staticmethod
    def alert(text: str, kind: str = "") -> str:
        """Return a simple styled alert block.

        Parameters
        ----------
        text: str
            The alert message HTML/text.
        kind: str
            Optional extra CSS class (e.g., "info", "warning").
        """
        kind_cls = f" {kind}" if kind else ""
        return f"<div class='alert{kind_cls}'>{text}</div>"

    # ---------------------------- Rendering --------------------------
    def render(self, out_path: str) -> str:
        """Render the report to `out_path` and return the absolute path.

        The Jinja template receives the following context variables:
        - title
        - generated_at (YYYY-MM-DD HH:MM:SS)
        - sections (list[Section])
        - intro_html (str)
        - use_plotly_cdn (bool)
        - plotly_js_inline (str) — reserved for future inline delivery
        """
        html = self._template.render(
            title=self.title,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sections=self.sections,
            intro_html=self.intro_html,
            use_plotly_cdn=self.use_plotly_cdn,
            plotly_js_inline="",
        )
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        return str(out.resolve())

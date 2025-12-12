# repyter

A tiny, Python-first HTML report builder. Compose sections and blocks in pure Python, render once via Jinja2. Optional helpers let you embed Pandas tables, Plotly figures, and Matplotlib images — all without leaving your Python debugger or notebook.

Note: This package intentionally keeps everything in Python. There are no separate CLI tools or Markdown engines; you build the document programmatically and render to a single HTML file using a Jinja2 template.

## Installation

repyter is a regular Python package. For now, install from source:

```
pip install -e .
```

Requirements:
- Python >= 3.13
- jinja2
- pandas

Optional (only needed if you use the respective helpers):
- plotly
- matplotlib

## Quick start

```python
from repyter import Report
import pandas as pd

report = Report(title="My Analysis Report")

# Intro block shown above all sections
report.set_intro(Report.alert("This report was generated automatically."))

# Section with a Pandas table
sec = report.add_section("Run Summary")
df = pd.DataFrame({
    "Metric": ["Rows", "Features", "Accuracy"],
    "Value": [12_345, 42, 0.9123],
})
report.add_block(Report.table_from_df(df), section=sec)

# Optional: Plotly (if installed)
# import plotly.express as px
# fig = px.line(pd.DataFrame({"x": range(10), "y": [v * 1.5 for v in range(10)]}), x="x", y="y")
# report.add_section("Interactive Chart")
# report.add_block(Report.plotly_div(fig))

# Optional: Matplotlib (if installed)
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(figsize=(4, 3))
# ax.plot([0, 1, 2], [0, 1, 0])
# report.add_section("Static Figure")
# report.add_block(Report.mpl_img(fig, alt="A simple curve"))

# Render to HTML
out_file = report.render("reports/report.html")
print(f"Wrote: {out_file}")
```

Open the file in your browser to view the result.

## Concepts

- Section: a logical grouping with a title and a list of HTML blocks.
- Block: any HTML string. Helpers are provided to generate consistent blocks:
  - `Report.table_from_df(df)`: Pandas DataFrame -> styled HTML table.
  - `Report.plotly_div(fig)`: Plotly figure -> embeddable `<div>` (requires `plotly`).
  - `Report.mpl_img(fig)`: Matplotlib figure -> base64 `<img>` (requires `matplotlib`).
  - `Report.image_src(path)`: simple image by path/URL.
  - `Report.alert(text, kind="")`: styled alert box.

## Template

The default template is `repyter/template.html`. You can pass a custom template path to the `Report` constructor if desired. The template receives:

- `title` (str)
- `generated_at` (str, `YYYY-MM-DD HH:MM:SS`)
- `sections` (list of `Section`)
- `intro_html` (str)
- `use_plotly_cdn` (bool)
- `plotly_js_inline` (str, reserved for inline delivery)

Note: The repository ships with a template; you typically don't need to modify it. The README does not document the template's internals.

## Minimal API reference

```python
from repyter import Report, Section
```

- `Report(template_path: str = default_template, use_plotly_cdn: bool = True, title: str | None = None)`
  - `set_intro(html: str) -> Report`
  - `add_section(title: str) -> Section`
  - `add_block(block: str | pandas.DataFrame, section: Section | None = None) -> Report`
  - `render(out_path: str) -> str`  # returns absolute path
  - Helpers (all `@staticmethod`):
    - `table_from_df(df: pd.DataFrame, float_fmt: str = "{:,.4f}") -> str`
    - `html_block(html: str) -> str`
    - `plotly_div(fig, width: str = "100%", height: str = "auto") -> str`
    - `mpl_img(fig, fmt: str = "png", dpi: int = 144, alt: str = "figure") -> str`
    - `image_src(path: str, alt: str = "image") -> str`
    - `alert(text: str, kind: str = "") -> str`

- `Section(title: str, blocks: list[str])`

## Development

- Running tests (uses pytest):

```
python -m pytest -q
```

- Code style: Follow the simple, explicit style in `repyter/report.py`. Keep public docstrings clear and concise.

- Backwards compatibility: Please avoid adding new features without discussion; this project focuses on a compact Python API for now.

## License

MIT (see `LICENSE`).

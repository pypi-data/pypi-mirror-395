# The light Python report builder.

Converts data into formatted text (**PDF**, **XLSX**, **DOCX**, **HTML**):

```python
data = {'data_source1':[{'col1': 'value row1', ....}, ...],
        'data_source2':[{'col_1': 'valie_row1', ....}, ...],
        }
```

Available formatting (styling options):

```json
"style": {
        "font-family": "Arial",
        "font-size": "10pt",
        "font-weight": "normal",  # bold
        "text-decoration": "",  # underline
        "font-style": "",  # italic
        "color": "black",  # font color
        "background": "white",  # background color
        "border-color": "black",  # border color
        "border-width": "1 1 1 1",
        "padding": "0.05cm 0.05cm 0.05cm 0.05cm",
        "text-align": "left",
        "vertical-align": "top",
  }
```

## Concept

The report definition consists of sections (Report, Pages, Columns, Rows, Cells).  
Each section inherits style from previous and may override some styling options.  
\*see examples in folder **test_data\***

```python
Report:      # top-level report object containing the base style
    Pages:   # page size, margins, and page-level styles
        Columns:    # column widths: fixed, %, or auto-width; supports styles
            Rows:   # row heights: auto, fixed, minimum, or maximum; supports styles
                    # rows may be data-bound and can include subsections:
                    # header, footer, group-header, group-footer
                Cells:  # contain plain text and data placeholders — {col1} (f-strings style)
                        # support aggregate functions — {sum:col1}
                        # support basic HTML formatting: <b> <i> <u> <br>
            Rows:
                Cells:  # cells can be merged (span)
            ...
        Columns:
            ...
    Pages:
        ...
    ...```

---

## Main API (`Q2Report`)

### Initialization

```python
from q2report.q2report import Q2Report

report = Q2Report(style={...})
```

### Adding Pages and Columns

```python
report.add_page(page_width=21, page_height=29.7, page_margin_left=2, page_margin_right=1)
report.add_columns(page_index=0, widths=[5, 5, 5], style={...})
```

### Adding Rows and Cells

```python
rows = report.add_rows(page_index=0, columns_index=0, heights=[1, 1, 1], style={...})
rows.set_cell(0, 0, "{col1}", style={"font-weight": "bold"})
rows.set_cell(1, 0, "{sum:col2}", format="F2")
```

Or directly via report:

```python
report.set_cell(0, 1, "Some value", page_index=0, columns_index=0, rows_index=0)
```

### Data Binding

- Use `{column_name}` in cell data to bind to data source columns.
- Use `{sum:column_name}` for aggregation in table footers or group footers.

### Grouping and Aggregation

```python
rows.add_table_group(
    groupby="col1",
    header=Q2Report_rows(...),
    footer=Q2Report_rows(...)
)
```

### Rendering

```python
report.run(output_file="output.pdf", data=data)
```

- Supported output types: `"html"`, `"pdf"`, `"xlsx"`, `"docx"`

---

## Features

- **Flexible styling**: Inherit and override styles at any level.
- **Data-driven**: Bind data sources to tables, rows, and cells.
- **Aggregates**: Built-in support for `{sum:col}` and similar formulas.
- **Grouping**: Group rows by one or more columns, with group headers/footers.
- **Images**: Embed images using `{q2image(path)}` or cell format `"I"`.
- **Multi-format output**: Export to HTML, PDF, XLSX, DOCX.
- **Custom formulas**: Use Python expressions in `{...}`.

---

## Example

```python
from q2report.q2report import Q2Report

report = Q2Report()
report.add_page()
report.add_columns(widths=[5, 5, 5])
rows = report.add_rows(heights=[1, 1, 1])
rows.set_cell(0, 0, "Header 1", style={"font-weight": "bold"})
rows.set_cell(0, 1, "Header 2", style={"font-weight": "bold"})
rows.set_cell(1, 0, "{col1}")
rows.set_cell(1, 1, "{col2:F2}")
report.run(output_file="report.pdf", data={"data_source": [{"col1": "A", "col2": 123456}]})
```

---

## Advanced

- **Custom styles**: Use `Q2Report.make_style(...)` to generate style dicts.
- **Direct JSON**: You can load report definitions from JSON files or strings.
- **Accessing data**: Use `report.d.<dataset>` for advanced row access in formulas.

---

## See Also

- [test_data/](test_data/) for more examples.
- [q2report.py](q2report/q2report.py) for full API and docstrings.

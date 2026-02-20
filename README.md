# de-components

Reusable, generic components for data engineering and analytics workflows.

---

## Purpose

In nearly every data project, we rebuild the same building blocks:

- Plotting utilities
- Data quality checks
- Logging configurations
- Validation layers

`de-components` is a reusable component library designed to eliminate repetitive setup
and accelerate analytics and data engineering projects.

---

## Structure

### plots/
Generic plotting utilities that:
- Accept a pandas DataFrame
- Do not assume column names
- Provide safe defaults
- Allow optional customization

### eda/
Reusable exploratory data analysis helpers:
- Summary statistics
- Null analysis
- Column profiling

### validation/
Lightweight data quality components:
- Schema validation
- Duplicate detection
- Missing value checks
- Type validation

### utils/
Common utilities used across projects:
- Logging setup
- Config loaders
- Reusable helpers

---

## Design Principles

Every component is:

- Generic
- Reusable
- Minimal in assumptions
- Cleanly documented
- Production-aware

This is not a project repository.
It is a growing engineering toolkit.

---

## 🛠 Example

```python
from de_components.plots import create_line_plot

create_line_plot(
    df,
    x_col="date",
    y_col="revenue",
    title="Revenue Over Time"
)

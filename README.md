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

### core/
Foundational building blocks shared across the library.

### quality/
Lightweight, reusable data quality components.

### visualization/
Generic plotting utilities.- Schema validation

### transform//
Reusable transformation components.

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

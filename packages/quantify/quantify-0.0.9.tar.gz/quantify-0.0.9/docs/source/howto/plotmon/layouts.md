# Layouts

Plotmon layouts are defined using a simple nested array (list) structure in JSON. This structure determines how your plots are arranged on the dashboard.

---

## Layout Structure

- **Each inner array** (`[ ... ]`) represents a **row** of plots.
- **Each plot configuration** inside a row array is displayed side by side in that row.
- **The outer array** (`[ [...], [...] ]`) stacks these rows vertically, forming columns.

**In summary:**
- Plots in the same inner array appear in the same row (horizontally).
- Each inner array is a new row (stacked vertically).

---

## Example

```json
[
  [
    { /* plot config for plot 1 */ },
    { /* plot config for plot 2 */ }
  ],
  [
    { /* plot config for plot 3 */ }
  ]
]
```

- The first row contains two plots, side by side.
- The second row contains one plot, below the first row.

---

## How to Use

1. **Define each plot as a JSON object** (see the [graphs documentation](graphs) for details).
2. **Group plots into arrays** for each row.
3. **Combine all rows into an outer array** to form your layout.

---

## Visual Example

Given this layout:

```json
[
  [ { /* plot A */ }, { /* plot B */ } ],
  [ { /* plot C */ } ]
]
```

The dashboard will look like:

```
| Plot A | Plot B |
|      Plot C     |
```

---

## Notes

- **When a `GRAPH_CONFIG` command is sent, the previous layout will be completely overwritten.**   Any existing plots and their arrangement will be replaced by the new configuration you provide.
- The order of plots and rows in the arrays determines their position on the dashboard.
- You can have any number of rows and any number of plots per row.

- The order of plots and rows in the arrays determines their position on the dashboard.
- You can have any number of rows and any number of plots per row.

---

For more details on plot configuration, see [Customizing Graphs](graphs).

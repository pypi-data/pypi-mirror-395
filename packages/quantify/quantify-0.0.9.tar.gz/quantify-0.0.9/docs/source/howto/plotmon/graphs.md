# Customizing Graphs

Plotmon is designed to be a flexible, extensible plotting server for experiment monitoring. It allows users and data providers to define, add, and customize graphs dynamically, supporting a variety of plot types and layouts. This guide explains how to add new graphs and customize their appearance and behavior.

---

## 1. How Plotmon Handles Graphs

Plotmon uses a configuration-driven approach to define which graphs are displayed, their types, axes, and layout. Each graph is described by a configuration object, which among many other field specifies:

- **Plot name** (unique identifier)
- **Plot type** (e.g., line, heatmap)
- **X and Y axis keys**
- **Other plot-specific options** (e.g., color maps, tooltips)

The configuration is provided to Plotmon at initialization or via a command from the Data Provider.

---

## 2. Adding a New Graph

Each graph is described by a configuration object. Plotmon currently only supports line graphs and heatmap graphs. For example, to add a line plot plotmon has to ingests the following `json`:

```json
{
    "plot_name": "voltage_vs_time",
    "plot_type": "1d",
    "x_key": "time_ns",
    "y_key": "voltage_mV",
    // ...other options...
}
```

Similarly for a heatmap:

```json
{
    "plot_name": "spectrogram",
    "plot_type": "heatmap",
    "x_key": "frequency_GHz",
    "y_key": "time_ns",
    "image_key": "amplitude",
    "dw_key": "df",
    "dh_key": "dt",
    // ...other options...
}
```

## 3. Full Configuration Reference

This section documents the full configuration options for the two main plot types in Plotmon: line graphs and heatmap graphs. Each configuration can be provided as a JSON object when defining or customizing graphs.

---

### Heatmaps

Next is all configurable fields are presented for plotting heatmaps.

#### Example JSON

```json
{
  "plot_type": "heatmap",
  "image_key": "image",
  "x_key": "x",
  "y_key": "y",
  "dw_key": "dw",
  "dh_key": "dh",
  "plot_name": "generic_heatmap",
  "x_label": "X",
  "y_label": "Y",
  "z_label": "Z",
  "x_units": "",
  "y_units": "",
  "z_units": "",
  "title": "2D Heatmap",
  "width": 750,
  "height": 600,
  "palette": "Viridis256"
}
```

#### Field Reference

Here you can find out what each paramenter controls.

| Field         | Type    | Default        | Description                                                                                           |
|---------------|---------|----------------|-------------------------------------------------------------------------------------------------------|
| plot_type     | string  | "heatmap"      | Type of the plot (must be `"heatmap"`).                                                               |
| image_key     | string  | "image"        | Key for the image data in the source (e.g., `"image"` or `"img"`).                                    |
| x_key         | string  | "x"            | Key for the x-axis data in the source.                                                                |
| y_key         | string  | "y"            | Key for the y-axis data in the source.                                                                |
| dw_key        | string  | "dw"           | Key for the width of each image pixel.                                                                |
| dh_key        | string  | "dh"           | Key for the height of each image pixel.                                                               |
| plot_name     | string  | "generic_heatmap" | Name of the plot (must be unique).                                                                |
| x_label       | string  | "X"            | Label for the x-axis.                                                                                 |
| y_label       | string  | "Y"            | Label for the y-axis.                                                                                 |
| z_label       | string  | "Z"            | Label for the z-axis (colorbar).                                                                      |
| x_units       | string  | ""             | Units for the x-axis.                                                                                 |
| y_units       | string  | ""             | Units for the y-axis.                                                                                 |
| z_units       | string  | ""             | Units for the z-axis.                                                                                 |
| title         | string  | "2D Heatmap"   | Title of the heatmap figure.                                                                          |
| width         | int     | 750            | Width of the figure in pixels.                                                                        |
| height        | int     | 600            | Height of the figure in pixels.                                                                       |
| palette       | string  | "Viridis256"   | Color palette for the heatmap (e.g., `"Viridis256"`, `"Inferno256"`).                                 |

---

### Lines

Configuration fields for line graphs.

#### Example JSON

```json
{
  "plot_type": "1d",
  "x_label": "X-axis",
  "y_label": "Y-axis",
  "x_units": "units",
  "y_units": "units",
  "title": "1D Plot",
  "width": 300,
  "height": 300,
  "plot_name": "generic_plot",
  "inactive_alpha": 0.3,
  "active_alpha": 1.0,
  "color": "#1f77b4",
  "selection_color": "#1f77b4",
  "nonselection_color": "#ff7f0e",
  "nonselection_alpha": 0.08,
  "hover_color": "#ff7f0e",
  "hover_alpha": 1.0,
  "x_key": "x",
  "y_key": "y",
  "legend_title": "Experiments",
  "legend_location": "top_right",
  "legend_click_policy": "hide"
}
```

#### Field Reference

| Field               | Type    | Default        | Description                                                                                           |
|---------------------|---------|----------------|-------------------------------------------------------------------------------------------------------|
| plot_type           | string  | "1d"           | Type of the plot (must be `"1d"`).                                                                    |
| x_label             | string  | "X-axis"       | Label for the x-axis.                                                                                 |
| y_label             | string  | "Y-axis"       | Label for the y-axis.                                                                                 |
| x_units             | string  | "units"        | Units for the x-axis.                                                                                 |
| y_units             | string  | "units"        | Units for the y-axis.                                                                                 |
| title               | string  | "1D Plot"      | Title of the 1D figure.                                                                               |
| width               | int     | 300            | Width of the figure in pixels.                                                                        |
| height              | int     | 300            | Height of the figure in pixels.                                                                       |
| plot_name           | string  | "generic_plot" | Name of the plot (must be unique).                                                                    |
| inactive_alpha      | float   | 0.3            | Alpha value for inactive lines.                                                                       |
| active_alpha        | float   | 1.0            | Alpha value for the active line.                                                                      |
| color               | string  | "#1f77b4"      | Color for inactive lines (hex or named color).                                                        |
| selection_color     | string  | "#1f77b4"      | Color for the selected/active line.                                                                   |
| nonselection_color  | string  | "#ff7f0e"      | Color for non-selected lines.                                                                         |
| nonselection_alpha  | float   | 0.08           | Alpha value for non-selected lines.                                                                   |
| hover_color         | string  | "#ff7f0e"      | Color for lines on hover.                                                                             |
| hover_alpha         | float   | 1.0            | Alpha value for lines on hover.                                                                       |
| x_key               | string  | "x"            | Key for the x-axis data in the source.                                                                |
| y_key               | string  | "y"            | Key for the y-axis data in the source.                                                                |
| legend_title        | string  | "Experiments"  | Title for the legend.                                                                                 |
| legend_location     | string or [float, float] | "top_right" | Location of the legend (e.g., `"top_right"`, `"bottom_left"`, or `[x, y]`).                |
| legend_click_policy | string  | "hide"         | Legend click policy (`"hide"` or `"mute"`).                                                           |

---

### Notes

- All fields are optional except for those required by the plot type.
- For custom color values, use any valid [Bokeh color](https://docs.bokeh.org/en/latest/docs/reference/colors.html).
- The `plot_name` must be unique across all plots in a layout.

---

## 4. Advanced Customization

- **Shared Axes:**
  Plots with the same `x_key` or `y_key` will have their axes linked for zooming and panning.
- **Dynamic Updates:**
  Data can be streamed to any plot by referencing its `plot_name` and the experiment TUID. The keys inside the data object are corresponding to what key names were given in the configuration. Example if `x_key` is `t`, then Plotmon will look for the `t` key when updating data. See [commands](communication.md) section for more details.
- **Selection:**
  Users can select which experiment (TUID) to display using the DataTable.

---

## 5. Changing Graph Layout at Runtime

To change the graph layout (e.g., add/remove plots, rearrange), send a new configuration to Plotmon using the `GRAPH_CONFIG` command. Plotmon will reset its internal state and re-render the layout. See [layout](layouts) for more details.

---

## 6. Troubleshooting

- If a plot does not appear, check that its configuration is valid and that the data keys match.
- Missing data or axes? Ensure your data provider streams data with the correct keys.

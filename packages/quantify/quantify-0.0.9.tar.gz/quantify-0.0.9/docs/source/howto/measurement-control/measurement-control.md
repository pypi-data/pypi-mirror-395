# Measurement Control for Plotmon


The **MeasurementControl** class can be extended with live data visualization and monitoring by calling its `attach_plotmon` method. This enables live data extraction for visualization in [Plotmon](plotmon/intro.md) without changing your experimental workflow. Communication with Plotmon is abstracted, making it straightforward to upgrade or switch to different protocols in the future.

## Getting Started

The starting Plotmon is straightforward. You can initialize, set up parameters, and run experiments as usual. To enable live data communication for visualization, simply call `attach_plotmon()` before running your experiments.

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from qcodes import ManualParameter, Parameter

import quantify.data.handling as dh
from quantify.measurement.control import MeasurementControl

dh.set_datadir(Path.home() / "quantify-data")
meas_ctrl = MeasurementControl("meas_ctrl")
meas_ctrl.attach_plotmon()  # Enable live Plotmon visualization

par0 = ManualParameter(name="x0", label="X0", unit="s")
par1 = ManualParameter(name="x1", label="X1", unit="s")
par3 = ManualParameter(name="x3", label="X3", unit="s")
sig = Parameter(name="sig", label="Signal", unit="V", get_cmd=lambda: np.exp(par0()))

meas_ctrl.settables([par0, par1, par2])
meas_ctrl.setpoints_grid([
	np.linspace(0, 1, 4),
	np.linspace(1, 2, 5),
	np.linspace(2, 3, 6),
])
meas_ctrl.gettables(sig)
meas_ctrl.run("demo")

```


After starting your experiment, the console will display the address where [Plotmon](plotmon/intro) is serving the visualization. Open the provided link in your browser to view live data. Note that the port number may vary:

```bash
~/quantify$ Plotmon server started at http://localhost:5006
```

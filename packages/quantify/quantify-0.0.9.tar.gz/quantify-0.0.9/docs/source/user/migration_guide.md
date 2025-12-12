# Migration guide

This migration guide provides instructions for transitioning from quantify-scheduler and quantify-core to the new quantify package. In here, we explain the overlap between the three packages, the steps to migrate to quantify from quantify-scheduler and quantify-core.

Quantify package contains all functionalities in the existing quantify-core and quantify-scheduler packages. This package consolidates both quantify-core and quantify-scheduler under one package whilst ensuring all the functionalities are hardware independent. Quantify provides the way to write experiments in a hardware agnostic way which can then be used with a *quantify backend* to connect to the instruments. The following figure explains the overlap and modules that are present within quantify-scheduler and absent in quantify.

```{figure} /images/quantify_repos.svg
:align: center
:name: quantify-repos
:width: 300
```
Instruments specific modules excluded in quantify:

quantify_scheduler.backends.qblox,
quantify_scheduler.backends.zhinst,
quantify_scheduler.backends.types.qblox,
quantify_scheduler.backends.types.zhinst,
quantify_scheduler.backends.qblox_backend,
quantify_scheduler.backends.zhinst_backend,
quantify_scheduler.helpers.qblox_dummy_instrument,
quantify_scheduler.instrument_coordinator.components.qblox,
quantify_scheduler.instrument_coordinator.components.zhinst,
quantify_core.visualization.instrument_monitor,
quantify_core.visualization.pyqt_plotmon,
quantify_core.visualization.pyqt_plotmon_remote,
quantify_core.visualization.ins_mon_widget,

## Steps to migrate

To migrate, we need to do two steps:

1. Ensure that usages of pyqt `InstrumentMonitor` and `Plotmonitor` are replaced by the new implementations. (Or you can choose to use the PyQT versions, but do note that they will not be maintained any further). For information on how to use the Bokeh based implementation of `InstrumentMonitor`, refer {ref}`Instrument Monitor <instrument-monitor>`.
2. Replace imports to import the functionality from quantify instead of quantify-core or quantify-scheduler.

A user can manually replace all relevant imports or they can call a quantify-provided utility function to scour their environment and replace the imports with quantify. Below we demonstrate how to use the utility function provided by quantify.

NOTE: This utility function only looks at .py files. Other files such as .md or .ipynb files using quantify-scheduler and quantify-core imports will NOT be replaced.


```python
root_dir = "path/to/your/codebase" # Specify the root directory of your codebase

from quantify.utilities.general import replace_imports

replace_imports(root_dir)
# To store modified file names, provide a path to a text file
# file_names_store = "path/to/store"
# replace_imports(root_dir, file_names_store=file_names_store)
```

This would replace all imports of `quantify_scheduler` and `quantify_core` with `quantify`. The user is requested to do one final check by running their experiments that traditionally used quantify-scheduler or quantify-core.

N.B - Check if dependency requirements of your environment align with that of quantify.

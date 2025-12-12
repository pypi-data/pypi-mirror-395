# About Quantify

[`quantify`](https://pypi.org/project/quantify/) is a Python-based data acquisition framework focused on Quantum Computing and solid-state physics experiments. It is built on top of [QCoDeS](https://qcodes.github.io/Qcodes/)
and is a spiritual successor of [PycQED](https://github.com/DiCarloLab-Delft/PycQED_py3).

`quantify` is a Python module for writing quantum programs featuring a hybrid gate-pulse control model with explicit timing control. This control model allows quantum gate and pulse-level descriptions to be combined in a clearly defined and hardware-agnostic way. `quantify` is designed to allow experimentalists to easily define complex experiments. It produces synchronized pulse schedules
that are distributed to control hardware, after compiling these schedules into control-hardware specific executable programs. `quantify` contains all basic functionality to control experiments. This includes:

- A framework to control instruments.
- A data-acquisition loop.
- Data storage and analysis.
- Parameter monitoring and live visualization of experiments.
- A framework to design gate and/or pulse based experimental protocol

## Overview and Community

For a general overview of Quantify and connecting to its open-source community, see [quantify-os.org](https://quantify-os.org/).
Quantify is maintained by the Orange Quantum Systems.

&nbsp;
&nbsp;
&nbsp;
&nbsp;
[<img src="https://gitlab.com/quantify-os/quantify-scheduler/-/raw/main/docs/source/images/OQS_logo_with_text.svg" alt="Orange Quantum Systems logo" width=200px/>](https://orangeqs.com)

&nbsp;

The software is free to use under the conditions specified in the [license](https://gitlab.com/quantify-os/quantify/-/raw/main/LICENSE).

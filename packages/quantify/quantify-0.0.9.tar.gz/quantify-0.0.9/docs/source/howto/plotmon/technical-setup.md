# Technical setup

Plotmon is built on top of [Bokeh](https://bokeh.org/), a library for interactive web-based visualizations. Plotmon provides a live dashboard for monitoring experiments, updating plots in real time as new data arrives.

## How Plotmon fits into Quantify

Plotmon is the default plotting framework for Quantify's Measurement Control. When you start Measurement Control, Plotmon is automatically launched and connected, so you can immediately view and monitor your experiments in your web browser, no extra setup required.

## Data Providers and Integration

Plotmon is designed to work with any data provider that can send data using [ZeroMQ](https://zeromq.org/). This means you can use Plotmon with your own custom experiments, as long as your data provider implements the required messaging protocol. For most users, this is handled automatically by Quantify.

- **Custom Data Providers:** If you are developing your own data provider, you simply need to publish experiment data and commands (such as start, update, and finish) to a ZeroMQ topic. The only required information at startup is the topic name your provider will use.

- **Messaging Protocol:** Plotmon listens for messages that describe experiment state and data. These messages must follow the [Plotmon communication protocol](communication.md).

---

For more information on supported plot types and layouts, see [graphs](graphs) and [layout](layouts).

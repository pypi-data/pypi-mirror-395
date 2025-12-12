# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Tree component for the instrument monitor UI."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from bokeh.events import DocumentReady
from bokeh.layouts import column, row
from bokeh.models import Button, ColumnDataSource, CustomJS, Div

from quantify.visualization.instrument_monitor.components.theme import STYLES
from quantify.visualization.instrument_monitor.logging_setup import get_logger
from quantify.visualization.instrument_monitor.models import (
    Reading,
    TreeNode,
    _TreeEntry,
)

if TYPE_CHECKING:
    from bokeh.document import Document


logger = get_logger(__name__)


def _node_id(instrument: str, path: tuple[str, ...]) -> str:
    if not path:
        return instrument
    return "::".join((instrument, *path))


TREE_STYLESHEET = """
<style>
    .tree-container {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 13px;
        line-height: 1.6;
        color: #333;
    }
    .tree-item {
        display: flex;
        align-items: center;
        padding: 3px 0;
        user-select: none;
        border-left: 1px solid #eee;
    }
    .tree-item:hover {
        background: #f5f5f5;
    }
    .tree-toggle {
        display: inline-flex;
        width: 16px;
        margin-right: 4px;
        color: #999;
        font-size: 10px;
        cursor: pointer;
        flex-shrink: 0;
        transition: transform 0.15s ease;
    }
    .tree-toggle--expanded {
        transform: rotate(90deg);
    }
    .tree-label {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .tree-item--module .tree-label {
        color: #c41e3a;
        font-weight: 600;
    }
    .tree-item--instrument .tree-label {
        color: #0066cc;
        font-weight: 500;
    }
    .tree-item--param .tree-label {
        color: #333;
    }
    .tree-legend {
        position: absolute;
        right: 12px;
        top: 12px;
        display: flex;
        gap: 12px;
        font-size: 12px;
        color: #666;
        background: #fff;
        border: 1px solid #e5e5e5;
        border-radius: 6px;
        padding: 4px 6px;
        z-index: 2;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .legend-color {
        width: 12px;
        height: 12px;
        border-radius: 2px;
    }
    .tree-controls {
        display: flex;
        gap: 8px;
        margin-bottom: 8px;
    }
    .tree-control-btn {
        padding: 4px 8px;
        font-size: 11px;
        border: 1px solid #ddd;
        border-radius: 3px;
        background: #f8f9fa;
        cursor: pointer;
    }
    .tree-control-btn:hover {
        background: #e9ecef;
    }
    .tree-leaf-bullet {
        width: 16px;
        display: inline-block;
        text-align: center;
        color: #bbb;
        font-size: 10px;
        margin-right: 4px;
        flex-shrink: 0;
    }
</style>
"""


class SnapshotTree:
    """Interactive tree view showing instrument hierarchy."""

    def __init__(self) -> None:
        """Initialize the tree view component."""
        self.rows_container = Div(
            styles={
                "position": "relative",
            },
            css_classes=["tree-container"],
        )

        # Bridge for tree toggle events from JS to Python
        # JS will set node_id and bump tick to trigger on_change
        self.events = ColumnDataSource(
            data={
                "node_id": [""],
                "tick": [0],
            }
        )

        # Control buttons
        self.expand_all_btn = Button(
            label="Expand All",
            button_type="default",
            width=80,
            height=25,
            styles={"font-size": "11px"},
        )
        self.collapse_all_btn = Button(
            label="Collapse All",
            button_type="default",
            width=80,
            height=25,
            styles={"font-size": "11px"},
        )

        # Connect button callbacks
        self.expand_all_btn.on_click(self._expand_all)
        self.collapse_all_btn.on_click(self._collapse_all)

        controls = row(
            self.expand_all_btn, self.collapse_all_btn, styles={"margin-bottom": "8px"}
        )

        self.wrapper = column(
            self._create_legend(),
            controls,
            self.rows_container,
            sizing_mode="stretch_both",
            styles={
                "position": "relative",
                "padding": "12px",
                "overflow-y": "auto",
            },
        )

        self.empty_message = Div(
            text=(
                "⏳ No data available right now.\n"
                "Once instrument snapshots are ingested, the hierarchy will appear."
            ),
            styles={
                **STYLES["empty_state"],
                "position": "absolute",
                "left": "50%",
                "top": "50%",
                "transform": "translate(-50%, -50%)",
                "pointer-events": "none",
                "z-index": "1",
                "width": "80%",
                "background": "rgba(255,255,255,0.9)",
                "border-radius": "8px",
                "padding": "16px",
            },
            visible=True,
        )

        self._filter = ""
        self._expanded: set[str] = set()
        self._nodes: list[TreeNode] = []
        self._tree_roots: list[_TreeEntry] = []
        self._readings: Sequence[Reading] = []

    def bind_js(self, doc: Document) -> None:
        """Attach client-side delegated listener and global toggle function.

        This binds a DocumentReady CustomJS that:
        - Creates window.toggleTreeNode to write into ``self.events``.
        - Delegates clicks from ``self.rows_container`` to toggle nodes.
        """
        tree_toggle_js = CustomJS(
            args=dict(
                tree_events=self.events,
                tree_container=self.rows_container,
            ),
            code="""
            // Create global function for tree toggling
            window.toggleTreeNode = function(nodeId, event) {
              // Find the toggle element within the clicked row
              const toggleElement = document.getElementById('toggle-' + nodeId);

              if (toggleElement) {
                // Toggle the arrow rotation for immediate feedback
                toggleElement.classList.toggle('tree-toggle--expanded');
              }

              // Write nodeId and bump tick to trigger a change
              const d = Object.assign({}, tree_events.data);
              d.node_id = [String(nodeId || '')];
              const hasTick = Array.isArray(d.tick) && d.tick.length;
              const t = hasTick ? Number(d.tick[0]) : 0;
              d.tick = [t + 1];
              tree_events.data = d;
            };

            // Delegate click handling to the tree container
            // so inline onclick is not required
            try {
              const view = Bokeh.index[tree_container.id];
              if (view && view.el) {
                if (!view.el.__treeToggleBound) {
                  view.el.__treeToggleBound = true;
                  view.el.addEventListener('click', (ev) => {
                    // Prefer clicks on the arrow, but also allow row clicks
                    const toggleEl = ev.target.closest('.tree-toggle');
                    const rowEl = ev.target.closest('.tree-item');
                    if (!toggleEl && !rowEl) return;

                    // Determine node id from the closest toggle element
                    const t = toggleEl || (
                      rowEl && rowEl.querySelector('.tree-toggle')
                    );
                    if (!t || !t.id) return;
                    const id = t.id.startsWith('toggle-')
                      ? t.id.slice('toggle-'.length)
                      : t.id;
                    window.toggleTreeNode(id, ev);
                  });
                }
              }
            } catch (e) {
              // Swallow errors to avoid breaking the app
              // if the container is missing
            }

            // Fallback: also bind a document-level delegated listener once
            try {
              if (!document.__treeToggleBound) {
                document.__treeToggleBound = true;
                document.addEventListener('click', (ev) => {
                  const toggleEl = ev.target.closest('.tree-toggle');
                  const rowEl = ev.target.closest('.tree-item');
                  if (!toggleEl && !rowEl) return;
                  const t = toggleEl || (
                    rowEl && rowEl.querySelector('.tree-toggle')
                  );
                  if (!t || !t.id) return;
                  const id = t.id.startsWith('toggle-')
                    ? t.id.slice('toggle-'.length)
                    : t.id;
                  window.toggleTreeNode(id, ev);
                });
              }
            } catch (e) {}
            """,
        )
        # Bokeh's DocumentReady event binding
        try:
            doc.js_on_event(DocumentReady, tree_toggle_js)
        except Exception:
            logger.warning("Failed to bind tree toggle JS", exc_info=True)

    def bind_python_toggle_handler(self) -> None:
        """Attach Python-side handler for JS-originated toggle events."""
        try:
            self.events.on_change("data", self._on_events_change)
        except Exception:
            logger.warning("Failed to attach tree toggle handler", exc_info=True)

    def _on_events_change(self, _attr: str, _old: object, _new: object) -> None:
        """Handle changes to ``self.events`` from JS and toggle nodes."""
        try:
            data = self.events.data
            node_id_list = data.get("node_id", []) if isinstance(data, dict) else []
            node_id = ""
            if (
                isinstance(node_id_list, Sequence)
                and not isinstance(node_id_list, (str, bytes))
                and len(node_id_list) > 0
            ):
                node_id = str(node_id_list[0])
            if node_id:
                try:
                    expanded_before = node_id in self._expanded  # type: ignore[attr-defined]
                except Exception:
                    expanded_before = False
                logger.debug(
                    "Tree toggle requested",
                    extra={"node_id": node_id, "expanded_before": expanded_before},
                )
                self.toggle_node(node_id)
                try:
                    expanded_after = node_id in self._expanded  # type: ignore[attr-defined]
                except Exception:
                    expanded_after = False
                logger.debug(
                    "Tree toggle applied",
                    extra={"node_id": node_id, "expanded_after": expanded_after},
                )
        except Exception as e:
            logger.warning("Tree toggle handler failed: %s", str(e), exc_info=True)

    def update_readings(self, readings: Sequence[Reading]) -> None:
        """Update tree with new readings."""
        self._rebuild_view(readings)

    def focus_on_full_name(self, full_name: str) -> None:
        """Expand path to and highlight a specific parameter."""
        if not full_name:
            return

        instrument, _, tail = full_name.partition(".")
        segments = self._parameter_segments(tail) if tail else []
        self._ensure_expanded_path(instrument or "unknown", segments)
        # Rebuild so that expanded path's children are included
        self._rebuild_view(self._readings)

    def _rebuild_view(self, readings: Sequence[Reading]) -> None:
        self._readings = readings
        tree_roots = self._build_tree(readings)
        self._tree_roots = tree_roots

        if not tree_roots:
            self._nodes = []
            self._render_rows()
            self._show_empty_state(readings_present=bool(readings))
            return

        # Build flat list of nodes
        nodes: list[TreeNode] = []
        for root in sorted(tree_roots, key=lambda r: r.instrument.lower()):
            nodes.extend(self._flatten(root, 0))

        if not nodes:
            self._nodes = []
            self._render_rows()
            self._show_empty_state(readings_present=bool(readings), filter_active=False)
            return
        self._nodes = nodes
        self._render_rows()
        self.empty_message.visible = False

    def _render_rows(self) -> None:
        if not self._nodes:
            self.rows_container.text = ""
            return

        rows_html = [
            self._render_row(
                label=node.label,
                level=node.level,
                is_group=node.is_group,
                expanded=node.expanded,
                node_id=node.node_id,
            )
            for node in self._nodes
        ]

        # JS handlers are injected once in app.py via CustomJS
        self.rows_container.text = TREE_STYLESHEET + "".join(rows_html)

    def toggle_node(self, node_id: str) -> None:
        """Toggle expansion state of a specific node."""
        if node_id in self._expanded:
            self._expanded.remove(node_id)
        else:
            self._expanded.add(node_id)
        self._rebuild_view(self._readings)

    def _render_row(
        self,
        *,
        label: str,
        level: int,
        is_group: bool,
        expanded: bool,
        node_id: str,
    ) -> str:
        """Render a single tree row as HTML."""
        indent_px = level * 16
        item_class = "tree-item"

        if level == 0:
            item_class += " tree-item--module"
        elif is_group:
            item_class += " tree-item--instrument"
        else:
            item_class += " tree-item--param"

        toggle_html = ""
        row_onclick = ""
        cursor_style = ""
        if is_group:
            toggle_class = "tree-toggle"
            if expanded:
                toggle_class += " tree-toggle--expanded"
            toggle_html = (
                '<span class="'
                f"{toggle_class}"
                '" id="toggle-'
                f"{self._escape_html(node_id)}"
                '">▶</span>'
            )
            row_onclick = (
                " onclick=\"window.toggleTreeNode('"
                f"{self._escape_html(node_id)}"
                "', event)\""
            )
            cursor_style = "cursor: pointer;"
        else:
            toggle_html = '<span class="tree-leaf-bullet">•</span>'

        return (
            '<div class="'
            f"{item_class}"
            '" style="padding-left:'
            f"{indent_px}"
            "px; "
            f"{cursor_style}"
            '"'
            f"{row_onclick}"
            ">"
            f"{toggle_html}"
            '<span class="tree-label">'
            f"{self._escape_html(label)}"
            "</span>"
            "</div>"
        )

    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    def _create_legend(self) -> Div:
        """Create a Bokeh Div legend so it can be placed in layouts (LayoutDOM)."""
        return Div(
            text=(
                '<div class="legend-item">'
                '<div class="legend-color" style="display:inline-block; '
                "width:12px; height:12px; border-radius:2px; "
                'background: #c41e3a; margin-right: 4px;"></div>'
                "<span>Module</span>"
                "</div>"
                '<div class="legend-item">'
                '<div class="legend-color" style="display:inline-block; '
                "width:12px; height:12px; border-radius:2px; "
                'background: #0066cc; margin-right: 4px;"></div>'
                "<span>Instrument</span>"
                "</div>"
                '<div class="legend-item">'
                '<div class="legend-color" style="display:inline-block; '
                "width:12px; height:12px; border-radius:2px; "
                'background: #333; margin-right: 4px;"></div>'
                "<span>Parameter</span>"
                "</div>"
            ),
            css_classes=["tree-legend"],
            styles={
                "position": "absolute",
                "right": "12px",
                "top": "12px",
            },
        )

    def _show_empty_state(
        self, *, readings_present: bool, filter_active: bool = False
    ) -> None:
        if not readings_present:
            self.empty_message.text = (
                "⏳ No data available right now.\n"
                "Once instrument snapshots are ingested, the hierarchy will appear."
            )
        elif filter_active:
            self.empty_message.text = (
                "🔎 No results match your filter.\n"
                "Adjust the search to explore other parts of the hierarchy."
            )
        else:
            self.empty_message.text = (
                "✨ Instruments discovered, but no parameters are reporting values yet."
            )
        self.empty_message.visible = True

    def _build_tree(self, readings: Sequence[Reading]) -> list[_TreeEntry]:
        roots: dict[str, _TreeEntry] = {}
        for reading in readings:
            instrument = reading.instrument or "unknown"
            root = roots.get(instrument)
            if root is None:
                root = _TreeEntry(name=instrument, instrument=instrument, path=())
                roots[instrument] = root

            segments = self._parameter_segments(reading.parameter)
            if not segments:
                node = root.children.get(reading.parameter or reading.full_name)
                if node is None:
                    node = _TreeEntry(
                        name=reading.parameter or reading.full_name,
                        instrument=instrument,
                        path=(reading.parameter or reading.full_name,),
                    )
                    root.children[node.name] = node
                node.reading = reading
                continue

            # Walk the dotted path to create/find intermediate nodes and attach the leaf
            current = root
            path: list[str] = []
            for index, segment in enumerate(segments):
                path.append(segment)
                child = current.children.get(segment)
                if child is None:
                    child = _TreeEntry(
                        name=segment,
                        instrument=instrument,
                        path=tuple(path),
                    )
                    current.children[segment] = child
                if index == len(segments) - 1:
                    child.reading = reading
                current = child

        return list(roots.values())

    def _flatten(
        self,
        entry: _TreeEntry,
        level: int,
    ) -> list[TreeNode]:
        node_id = _node_id(entry.instrument, entry.path)
        is_group = bool(entry.children)
        expanded = node_id in self._expanded

        label = entry.name if level > 0 else entry.instrument

        node = TreeNode(
            node_id=node_id,
            label=label,
            level=level,
            is_group=is_group,
            expanded=expanded,
        )

        nodes = [node]
        if is_group and expanded:
            for child_name in sorted(entry.children.keys(), key=lambda n: n.lower()):
                child = entry.children[child_name]
                nodes.extend(self._flatten(child, level + 1))
        return nodes

    @staticmethod
    def _parameter_segments(parameter: str | None) -> list[str]:
        if not parameter:
            return []
        return [segment.strip() for segment in parameter.split(".") if segment.strip()]

    def _ensure_expanded_path(self, instrument: str, segments: Sequence[str]) -> None:
        self._expanded.add(instrument)
        prefix: list[str] = []
        for segment in segments:
            prefix.append(segment)
            self._expanded.add(_node_id(instrument, tuple(prefix)))

    def _expand_all(self) -> None:
        """Expand all nodes in the tree."""
        if not hasattr(self, "_tree_roots"):
            return

        def add_all_nodes(entry: _TreeEntry) -> None:
            node_id = _node_id(entry.instrument, entry.path)
            self._expanded.add(node_id)
            for child in entry.children.values():
                add_all_nodes(child)

        for root in self._tree_roots:
            add_all_nodes(root)
        # Rebuild to include all newly expanded nodes
        self._rebuild_view(self._readings)

    def _collapse_all(self) -> None:
        """Collapse all nodes in the tree."""
        self._expanded.clear()
        # Rebuild to reflect collapsed state
        self._rebuild_view(self._readings)

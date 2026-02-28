"""Protocol definitions for widget component interfaces."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QCheckBox, QLabel, QWidget

if TYPE_CHECKING:
    from napari.components import ViewerModel
    from napari.layers import Layer


class AxisComponent(Protocol):
    """Interface for a single axis-metadata editing component.

    Each implementation manages a set of per-axis widgets (one per
    dimension) and exposes them through ``get_entries_dict`` for layout
    by the parent widget.
    """

    _component_name: str
    _napari_viewer: ViewerModel
    _main_widget: QWidget
    _component_qlabel: QLabel

    _selected_layer: Layer | None
    _axis_name_labels_tuple: tuple[QLabel, ...]
    _inherit_checkbox_tuple: tuple[QCheckBox, ...]

    def __init__(
        self, napari_viewer: ViewerModel, main_widget: QWidget
    ) -> None: ...

    def load_entries(self, layer: Layer | None = None) -> None: ...

    def get_entries_dict(
        self,
    ) -> dict[
        int,
        dict[
            str,
            tuple[list[QWidget], int, int, str, Qt.AlignmentFlag | None],
        ],
    ]: ...

    def _reset_tuples(self) -> None: ...

    def _set_axis_name_labels(self) -> None: ...

    def inherit_layer_properties(self, template_layer: Layer) -> None: ...

    def _set_checkboxes_visibility(self, visible: bool) -> None: ...


class MetadataComponent(Protocol):
    """Interface for a file/general metadata display component.

    Unlike ``AxisComponent``, these show a single widget per entry
    (e.g. layer name, shape, dtype) rather than one per axis.
    """

    _component_name: str
    _napari_viewer: ViewerModel
    _component_qlabel: QLabel

    def __init__(
        self, napari_viewer: ViewerModel, main_widget: QWidget
    ) -> None: ...

    def load_entries(self, layer: Layer | None = None) -> None: ...

    def get_entries_dict(
        self, layout_mode: str
    ) -> (
        dict[
            str,
            tuple[QWidget, int, int, str, Qt.AlignmentFlag | None],
        ]
        | dict[
            int,
            dict[
                str,
                tuple[QWidget, int, int, str, Qt.AlignmentFlag | None],
            ],
        ]
    ): ...

    def get_under_label(self, layout_mode: str) -> bool: ...


class AxesMetadataComponentsInstanceAPI(Protocol):
    """Minimal interface exposed by ``AxisMetadata`` for cross-component updates."""

    def _update_axes_labels(self) -> None: ...


class MetadataWidgetAPI(Protocol):
    """Minimal interface expected by child widgets that need to call
    back into the top-level ``MetadataWidget``.
    """

    def apply_inheritance_to_current_layer(
        self, template_layer: Layer
    ) -> None: ...

    def load_axes_widgets(self) -> None: ...

    def get_axes_metadata_instance(
        self,
    ) -> AxesMetadataComponentsInstanceAPI: ...

    def _resolve_show_inheritance_checkboxes(
        self, orientation: str, checked: bool
    ) -> None: ...

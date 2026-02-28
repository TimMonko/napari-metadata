"""File / general metadata display components (name, shape, dtype, size, path).

Each component class is decorated with ``@_metadata_component`` to register
it in ``FILE_METADATA_COMPONENTS_DICT``.  The coordinator class
``FileGeneralMetadata`` instantiates all registered components.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QFontMetrics
from qtpy.QtWidgets import (
    QLabel,
    QLineEdit,
    QSizePolicy,
    QTextEdit,
    QWidget,
)

from napari_metadata.file_size import generate_display_size
from napari_metadata.layer_utils import (
    get_layer_data_dtype,
    get_layer_data_shape,
    get_layer_source_path,
    resolve_layer,
)
from napari_metadata.widgets._protocols import MetadataComponent

if TYPE_CHECKING:
    from napari.layers import Layer
    from napari.viewer import ViewerModel

FILE_METADATA_COMPONENTS_DICT: dict[str, type[MetadataComponent]] = {}


def _metadata_component(
    _setting_class: type[MetadataComponent],
) -> type[MetadataComponent]:
    """Decorator that registers a ``MetadataComponent`` implementation."""
    FILE_METADATA_COMPONENTS_DICT[_setting_class.__name__] = _setting_class
    return _setting_class


# ---------------------------------------------------------------------------
# Layer Name
# ---------------------------------------------------------------------------


@_metadata_component
class LayerNameComponent:
    _component_name: str
    _napari_viewer: ViewerModel
    _main_widget: QWidget
    _component_qlabel: QLabel
    _under_label: bool

    _layer_name_line_edit: QLineEdit

    def __init__(
        self, napari_viewer: ViewerModel, main_widget: QWidget
    ) -> None:
        self._napari_viewer = napari_viewer
        self._main_widget = main_widget

        component_qlabel: QLabel = QLabel('Layer Name:')
        component_qlabel.setStyleSheet('font-weight: bold;')
        component_qlabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._component_qlabel = component_qlabel

        layer_name_line_edit = QLineEdit()
        self._layer_name_line_edit = layer_name_line_edit
        layer_name_line_edit.setSizePolicy(
            QSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred,
            )
        )
        self._layer_name_line_edit.editingFinished.connect(
            self._on_name_line_changed
        )
        self._component_name = 'LayerName'

    def load_entries(self, layer: Layer | None = None) -> None:
        active_layer = resolve_layer(self._napari_viewer, layer)
        if active_layer is None:
            self._layer_name_line_edit.setText('None selected')
            return
        self._layer_name_line_edit.setText(active_layer.name)

    def get_entries_dict(
        self, layout_mode: str = 'vertical'
    ) -> dict[str, tuple[QWidget, int, int, str, Qt.AlignmentFlag | None]]:
        col_span = 2 if layout_mode == 'vertical' else 3
        return {
            'LayerName': (
                self._layer_name_line_edit,
                1,
                col_span,
                '_on_name_line_changed',
                Qt.AlignmentFlag.AlignTop,
            ),
        }

    def get_under_label(self, layout_mode: str = 'vertical') -> bool:
        return layout_mode == 'vertical'

    def _on_name_line_changed(self) -> None:
        text = self._layer_name_line_edit.text()
        active_layer = resolve_layer(self._napari_viewer)
        if active_layer is None:
            self._layer_name_line_edit.setText('No layer selected')
            return
        if text == active_layer.name:
            return
        active_layer.name = text


# ---------------------------------------------------------------------------
# Layer Shape
# ---------------------------------------------------------------------------


@_metadata_component
class LayerShapeComponent:
    _component_name: str
    _napari_viewer: ViewerModel
    _main_widget: QWidget
    _component_qlabel: QLabel
    _under_label: bool

    _layer_shape_label: QLabel

    def __init__(
        self, napari_viewer: ViewerModel, main_widget: QWidget
    ) -> None:
        self._napari_viewer = napari_viewer
        self._main_widget = main_widget

        component_qlabel: QLabel = QLabel('Layer Shape:')
        component_qlabel.setStyleSheet('font-weight: bold;')
        component_qlabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._component_qlabel = component_qlabel

        shape_label: QLabel = QLabel('None selected')
        shape_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._layer_shape_label = shape_label

        self._component_name = 'LayerShape'

    def load_entries(self, layer: Layer | None = None) -> None:
        active_layer = resolve_layer(self._napari_viewer, layer)
        if active_layer is None:
            self._layer_shape_label.setText('None selected')
            return
        self._layer_shape_label.setText(
            str(get_layer_data_shape(active_layer))
        )

    def get_entries_dict(
        self, layout_mode: str = 'vertical'
    ) -> dict[str, tuple[QWidget, int, int, str, Qt.AlignmentFlag | None]]:
        col_span = 1 if layout_mode == 'vertical' else 2
        return {
            'LayerShape': (
                self._layer_shape_label,
                1,
                col_span,
                '',
                Qt.AlignmentFlag.AlignLeft,
            ),
        }

    def get_under_label(self, layout_mode: str = 'vertical') -> bool:
        return False


# ---------------------------------------------------------------------------
# Layer DataType
# ---------------------------------------------------------------------------


@_metadata_component
class LayerDataTypeComponent:
    _component_name: str
    _napari_viewer: ViewerModel
    _main_widget: QWidget
    _component_qlabel: QLabel
    _under_label: bool

    def __init__(
        self, napari_viewer: ViewerModel, main_widget: QWidget
    ) -> None:
        self._napari_viewer = napari_viewer
        self._main_widget = main_widget

        component_qlabel: QLabel = QLabel('Layer DataType:')
        component_qlabel.setStyleSheet('font-weight: bold;')
        component_qlabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._component_qlabel = component_qlabel

        data_type_label: QLabel = QLabel('None selected')
        data_type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._layer_data_type_label = data_type_label

        self._component_name = 'LayerDataType'

    def load_entries(self, layer: Layer | None = None) -> None:
        active_layer = resolve_layer(self._napari_viewer, layer)
        if active_layer is None:
            self._layer_data_type_label.setText('None selected')
            return
        self._layer_data_type_label.setText(
            str(get_layer_data_dtype(active_layer))
        )

    def get_entries_dict(
        self, layout_mode: str = 'vertical'
    ) -> dict[str, tuple[QWidget, int, int, str, Qt.AlignmentFlag | None]]:
        col_span = 1 if layout_mode == 'vertical' else 2
        return {
            'LayerDataType': (
                self._layer_data_type_label,
                1,
                col_span,
                '',
                Qt.AlignmentFlag.AlignLeft,
            ),
        }

    def get_under_label(self, layout_mode: str = 'vertical') -> bool:
        return False


# ---------------------------------------------------------------------------
# Layer File Size
# ---------------------------------------------------------------------------


@_metadata_component
class LayerFileSizeComponent:
    _component_name: str
    _napari_viewer: ViewerModel
    _main_widget: QWidget
    _component_qlabel: QLabel
    _under_label: bool

    def __init__(
        self, napari_viewer: ViewerModel, main_widget: QWidget
    ) -> None:
        self._napari_viewer = napari_viewer
        self._main_widget = main_widget

        component_qlabel: QLabel = QLabel('File Size:')
        component_qlabel.setStyleSheet('font-weight: bold;')
        component_qlabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._component_qlabel = component_qlabel

        file_size_label: QLabel = QLabel('None selected')
        file_size_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._layer_file_size_label = file_size_label

        self._component_name = 'LayerFileSize'

    def load_entries(self, layer: Layer | None = None) -> None:
        active_layer = resolve_layer(self._napari_viewer, layer)
        if active_layer is None:
            self._layer_file_size_label.setText('None selected')
            return
        self._layer_file_size_label.setText(
            str(generate_display_size(active_layer))
        )

    def get_entries_dict(
        self, layout_mode: str = 'vertical'
    ) -> dict[str, tuple[QWidget, int, int, str, Qt.AlignmentFlag | None]]:
        col_span = 1 if layout_mode == 'vertical' else 2
        return {
            'LayerFileSize': (
                self._layer_file_size_label,
                1,
                col_span,
                '',
                Qt.AlignmentFlag.AlignLeft,
            ),
        }

    def get_under_label(self, layout_mode: str = 'vertical') -> bool:
        return False


# ---------------------------------------------------------------------------
# Source Path
# ---------------------------------------------------------------------------


@_metadata_component
class SourcePathComponent:
    _component_name: str
    _napari_viewer: ViewerModel
    _main_widget: QWidget
    _component_qlabel: QLabel
    _under_label: bool

    def __init__(
        self, napari_viewer: ViewerModel, main_widget: QWidget
    ) -> None:
        self._component_name = 'SourcePath'
        self._napari_viewer = napari_viewer
        self._main_widget = main_widget

        component_qlabel: QLabel = QLabel('Source Path:')
        component_qlabel.setStyleSheet('font-weight: bold;')
        component_qlabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._component_qlabel = component_qlabel

        source_path_text_edit: SingleLineTextEdit = SingleLineTextEdit()
        source_path_text_edit.setPlainText('None selected')
        source_path_text_edit.setReadOnly(True)
        source_path_text_edit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        source_path_text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self._source_path_text_edit = source_path_text_edit

    def load_entries(self, layer: Layer | None = None) -> None:
        active_layer = resolve_layer(self._napari_viewer, layer)
        if active_layer is None:
            self._source_path_text_edit.setPlainText('None selected')
            font_metrics = QFontMetrics(self._source_path_text_edit.font())
            self._source_path_text_edit.setMaximumHeight(
                font_metrics.height() + 30
            )
            return
        self._source_path_text_edit.setPlainText(
            str(get_layer_source_path(active_layer))
        )
        font_metrics = QFontMetrics(self._source_path_text_edit.font())
        self._source_path_text_edit.setMaximumHeight(
            font_metrics.height() + 30
        )

    def get_entries_dict(
        self, layout_mode: str = 'vertical'
    ) -> dict[str, tuple[QWidget, int, int, str, Qt.AlignmentFlag | None]]:
        if layout_mode == 'vertical':
            return {
                'SourcePath': (
                    self._source_path_text_edit,
                    1,
                    2,
                    '',
                    Qt.AlignmentFlag.AlignVCenter,
                ),
            }
        return {
            'SourcePath': (
                self._source_path_text_edit,
                1,
                3,
                '',
                Qt.AlignmentFlag.AlignTop,
            ),
        }

    def get_under_label(self, layout_mode: str = 'vertical') -> bool:
        return layout_mode == 'vertical'


# ---------------------------------------------------------------------------
# Coordinator
# ---------------------------------------------------------------------------


class FileGeneralMetadata:
    """Coordinator that instantiates and manages all registered
    ``MetadataComponent`` implementations for file/general metadata.
    """

    _napari_viewer: ViewerModel
    _main_widget: QWidget
    _file_metadata_components_dict: dict[str, MetadataComponent]

    def __init__(
        self, napari_viewer: ViewerModel, main_widget: QWidget
    ) -> None:
        self._napari_viewer = napari_viewer
        self._main_widget = main_widget
        self._file_metadata_components_dict: dict[str, MetadataComponent] = {}

        for (
            name,
            cls,
        ) in FILE_METADATA_COMPONENTS_DICT.items():
            self._file_metadata_components_dict[name] = cls(
                napari_viewer, main_widget
            )


# ---------------------------------------------------------------------------
# Utility widgets
# ---------------------------------------------------------------------------


class SingleLineTextEdit(QTextEdit):
    """A QTextEdit sized to display a single line of text."""

    def sizeHint(self):
        font_metrics = QFontMetrics(self.font())
        return QSize(50, font_metrics.height())

    def maximumHeight(self) -> int:
        font_metrics = QFontMetrics(self.font())
        return font_metrics.height() + 6

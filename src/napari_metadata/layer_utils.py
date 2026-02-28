"""Helpers for reading and writing napari layer properties.

All functions operate on ``napari.components.ViewerModel`` and
``napari.layers.Layer``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from contextlib import suppress
from typing import TYPE_CHECKING, cast

import numpy as np
import pint

if TYPE_CHECKING:
    from napari.components import ViewerModel
    from napari.layers import Layer


# ---------------------------------------------------------------------------
# Layer resolution
# ---------------------------------------------------------------------------


def resolve_layer(
    viewer: ViewerModel, layer: Layer | None = None
) -> Layer | None:
    """Return *layer* if given, otherwise the viewer's active layer."""
    if layer is not None:
        return layer
    return viewer.layers.selection.active


def get_layers_list(viewer: ViewerModel) -> list[Layer]:
    """Return a list of all layers in the viewer."""
    return list(viewer.layers)


# ---------------------------------------------------------------------------
# Axes labels
# ---------------------------------------------------------------------------


def get_axes_labels(
    viewer: ViewerModel, layer: Layer | None = None
) -> tuple[str, ...]:
    """Get axis labels from *layer* (or the active layer)."""
    resolved = resolve_layer(viewer, layer)
    return resolved.axis_labels if resolved is not None else ()


def set_axes_labels(
    viewer: ViewerModel,
    axes_labels: tuple[str, ...],
    layer: Layer | None = None,
) -> None:
    """Set axis labels on *layer* (or the active layer)."""
    resolved = resolve_layer(viewer, layer)
    if resolved is not None:
        resolved.axis_labels = axes_labels


# ---------------------------------------------------------------------------
# Axes units
# ---------------------------------------------------------------------------


def get_axes_units(
    viewer: ViewerModel, layer: Layer | None = None
) -> tuple[pint.Unit | None, ...]:
    """Get axis units from *layer* (or the active layer)."""
    resolved = resolve_layer(viewer, layer)
    return resolved.units if resolved is not None else ()


def set_axes_units(
    viewer: ViewerModel,
    axes_units: tuple[str, ...],
    layer: Layer | None = None,
) -> None:
    """Set axis units on *layer* (or the active layer)."""
    resolved = resolve_layer(viewer, layer)
    if resolved is not None:
        resolved.units = axes_units


# ---------------------------------------------------------------------------
# Axes scales
# ---------------------------------------------------------------------------


def get_axes_scales(
    viewer: ViewerModel, layer: Layer | None = None
) -> tuple[float, ...]:
    """Get axis scales from *layer* (or the active layer)."""
    resolved = resolve_layer(viewer, layer)
    return (
        cast(tuple[float, ...], resolved.scale) if resolved is not None else ()
    )


def set_axes_scales(
    viewer: ViewerModel,
    axes_scales: tuple[float, ...],
    layer: Layer | None = None,
) -> None:
    """Set axis scales on *layer* (or the active layer).

    Non-float values cause an early return.  Values <= 0 are clamped to
    0.001.
    """
    resolved = resolve_layer(viewer, layer)
    if resolved is None:
        return

    for scale in axes_scales:
        if not isinstance(scale, float):
            return

    clamped = tuple(max(s, 0.001) for s in axes_scales)
    resolved.scale = np.array(clamped)


# ---------------------------------------------------------------------------
# Axes translations
# ---------------------------------------------------------------------------


def get_axes_translations(
    viewer: ViewerModel, layer: Layer | None = None
) -> tuple[float, ...]:
    """Get axis translations from *layer* (or the active layer)."""
    resolved = resolve_layer(viewer, layer)
    return (
        cast(tuple[float, ...], resolved.translate)
        if resolved is not None
        else ()
    )


def set_axes_translations(
    viewer: ViewerModel,
    axes_translations: tuple[float, ...],
    layer: Layer | None = None,
) -> None:
    """Set axis translations on *layer* (or the active layer)."""
    resolved = resolve_layer(viewer, layer)
    if resolved is not None:
        resolved.translate = axes_translations


# ---------------------------------------------------------------------------
# Layer introspection
# ---------------------------------------------------------------------------


def get_layer_data_shape(layer: Layer | None) -> tuple[int, ...]:
    """Return the shape of the layer's data."""
    if layer is None:
        return ()
    if hasattr(layer.data, 'shape'):
        return layer.data.shape
    if isinstance(layer.data, Sequence):
        return (len(layer.data),)
    return ()


def get_layer_data_dtype(layer: Layer | None) -> str:
    """Return the dtype of the layer's data as a string."""
    if layer is None:
        return ''
    data = layer.data
    if hasattr(data, 'dtype'):
        return str(data.dtype)
    if (
        isinstance(data, Sequence)
        and len(data) > 0
        and hasattr(data[0], 'dtype')
    ):
        return str(data[0].dtype)
    return 'Unknown'


def get_layer_source_path(layer: Layer | None) -> str:
    """Return the source path of the layer, or ``''``."""
    if layer is None or layer.source.path is None:
        return ''
    return layer.source.path


def get_layer_dimensions(layer: Layer | None) -> int:
    """Return the number of dimensions in the layer."""
    return layer.ndim if layer is not None else 0


# ---------------------------------------------------------------------------
# Event callback wiring
# ---------------------------------------------------------------------------


def connect_callback_to_layer_selection_events(
    viewer: ViewerModel, cb_function: Callable
) -> None:
    """Connect *cb_function* to layer selection change events."""
    viewer.layers.selection.events.active.connect(cb_function)


def disconnect_callback_to_layer_selection_events(
    viewer: ViewerModel, cb_function: Callable
) -> None:
    """Disconnect *cb_function* from layer selection change events."""
    with suppress(TypeError, ValueError):
        viewer.layers.selection.events.active.disconnect(cb_function)


def connect_callback_to_list_events(
    viewer: ViewerModel, cb_function: Callable
) -> None:
    """Connect *cb_function* to layer list events (insert, remove, change)."""
    viewer.layers.events.inserted.connect(cb_function)
    viewer.layers.events.removed.connect(cb_function)
    viewer.layers.events.changed.connect(cb_function)


def disconnect_callback_to_list_events(
    viewer: ViewerModel, cb_function: Callable
) -> None:
    """Disconnect *cb_function* from layer list events."""
    with suppress(TypeError, ValueError):
        viewer.layers.events.inserted.disconnect(cb_function)
    with suppress(TypeError, ValueError):
        viewer.layers.events.removed.disconnect(cb_function)
    with suppress(TypeError, ValueError):
        viewer.layers.events.changed.disconnect(cb_function)


def connect_callback_to_layer_name_changed(
    viewer: ViewerModel,
    cb_function: Callable,
    layer: Layer | None = None,
) -> None:
    """Connect *cb_function* to the name-changed event of *layer*."""
    resolved = resolve_layer(viewer, layer)
    if resolved is None:
        return
    resolved.events.name.connect(cb_function)


def disconnect_callback_to_layer_name_changed(
    viewer: ViewerModel,
    cb_function: Callable,
    layer: Layer | None,
) -> None:
    """Disconnect *cb_function* from the name-changed event of *layer*."""
    if layer is None:
        return
    with suppress(TypeError, ValueError):
        layer.events.name.disconnect(cb_function)

"""File and in-memory size formatting for layer data."""

from __future__ import annotations

import logging
import math
import urllib
from pathlib import Path
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from napari.layers import Layer

logger = logging.getLogger(__name__)

__all__ = ['generate_display_size']


def _generate_text_for_size(size: Union[int, float], suffix: str = '') -> str:
    """Format *size* (in bytes) as a human-readable string.

    Examples
    --------
    >>> _generate_text_for_size(13)
    '13.00 bytes'
    >>> _generate_text_for_size(1303131, suffix=' (in memory)')
    '1.30 MB (in memory)'
    """
    order = 0 if size == 0 else int(math.log10(size))

    logger.debug('order: %s', order)
    if order <= 2:
        text = f'{size:.2f} bytes'
    elif order < 6:
        text = f'{size / 1e3:.2f} KB'
    elif order < 9:
        text = f'{size / 1e6:.2f} MB'
    else:
        text = f'{size / 1e9:.2f} GB'
    return f'{text}{suffix}'


def generate_display_size(layer: Layer) -> str:
    """Return a formatted file-size string for *layer*.

    If the layer has a source path on disk the on-disk size is used;
    otherwise the in-memory size of the data array is reported.
    """
    is_url = urllib.parse.urlparse(layer.source.path).scheme in (
        'http',
        'https',
    )
    # data exists in file on disk
    if layer.source.path and not is_url:
        p = Path(layer.source.path)
        if p.is_dir():
            size = sum(
                file.stat().st_size for file in p.rglob('*') if file.is_file()
            )
        else:
            size = p.stat().st_size
        suffix = ''
    # data exists only in memory
    else:
        layer_type = type(layer).__name__
        if layer_type in ('Shapes', 'Surface') or layer.multiscale is True:
            size = sum(d.nbytes for d in layer.data)
        else:
            size = layer.data.nbytes
        suffix = ' (in memory)'

    return _generate_text_for_size(size, suffix=suffix)

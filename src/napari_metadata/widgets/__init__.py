"""Widget subpackage for napari-metadata.

All Qt-dependent code lives here.  The top-level package modules
(``units``, ``layer_utils``, ``file_size``) are pure Python and must
**not** be imported from this subpackage.
"""

from napari_metadata.widgets._main import MetadataWidget

__all__ = ['MetadataWidget']

import numpy as np
import pytest

napari = pytest.importorskip("napari")

from morphodeep import morphodeep_widget
from magicgui.widgets import Container


@pytest.fixture
def make_napari_viewer():
    """Simple local replacement for napari's make_napari_viewer fixture.

    This version does NOT depend on pytest-qt or the 'qtbot' fixture.
    It just creates a Viewer instance directly.
    """
    def _make():
        viewer = napari.Viewer()
        return viewer

    return _make


def test_morphodeep_widget_builds_with_viewer(make_napari_viewer, monkeypatch):
    """The main widget factory should return a magicgui Container
    and be callable in a napari-like context without running the real model.
    """

    # Create a napari viewer and add a simple image
    viewer = make_napari_viewer()
    viewer.add_image(np.random.random((16, 16)))

    # Patch current_viewer() used inside morphodeep._widget
    monkeypatch.setattr("morphodeep._widget.current_viewer", lambda: viewer)

    # Patch run_instance_segmentation so the test does not load a real model
    def _fake_run_instance_segmentation(*args, **kwargs):
        # Retrieve the image from kwargs (as called in _widget)
        if "image" in kwargs:
            image = kwargs["image"]
        elif args:
            image = args[0]
        else:
            raise ValueError("No image provided to fake run_instance_segmentation")

        # Return a labels array with the same shape as the input image
        return np.zeros_like(image, dtype=np.int32)

    monkeypatch.setattr(
        "morphodeep._widget.run_instance_segmentation",
        _fake_run_instance_segmentation,
    )

    # Call the public widget factory
    widget = morphodeep_widget()

    # Basic sanity check: the factory returns a magicgui Container
    assert isinstance(widget, Container)

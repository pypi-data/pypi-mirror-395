from magicgui.widgets import (
    Container,
    ComboBox,
    CheckBox,
    PushButton,
    Label,
    LineEdit,
)
from napari.layers import Image as ImageLayer, Labels
from napari import current_viewer
from PyQt5.QtCore import Qt

from .model import run_instance_segmentation


def morphodeep_widget() -> Container:
    """Create and return the main MorphoDeep napari widget.

        The widget lets the user:

        - select an image layer,
        - configure network parameters (patch size, 2D/3D mode),
        - specify voxel size and Z axis,
        - enable/disable isotropic rescaling and patches mode,
        - run the instance segmentation and add a Labels layer to the viewer.

        Returns
        -------
        magicgui.widgets.Container
            A container that can be added as a dock widget in napari.
    """
    viewer = current_viewer()

    # ---------- TITLE : IMAGE ----------
    title_image = Label(value="<h2><b>MorphoDeep</b></h2></br><b>Select your image</b>")
    title_image.native.setAlignment(Qt.AlignCenter)

    image_combo = ComboBox(
        label="raw image",
        choices=lambda w: [
            layer for layer in viewer.layers if isinstance(layer, ImageLayer)
        ],
    )

    def _on_image_changed(event=None):
        """Update widget state when the selected image layer changes.
            This callback refreshes:

            - the displayed image shape,
            - the 2D/3D mode guess based on the number of dimensions,
            - the voxel size fields using the layer scale, when available.
        """
        layer = image_combo.value
        if layer is None:
            image_shape.value = ""
        else:
            image_shape.value = str(layer.data.shape)

            if len(layer.data.shape) >= 3: mode.value = "3D"
            else: mode.value = "2D"

            scale = layer.scale
            if len(scale) == 1:
                vx, vy, vz = 1.0, 1.0, float(scale[0])
            elif len(scale) == 2:  # (X, Y)
                vx, vy, vz = float(scale[0]), float(scale[1]), 1.0
            else:
                vx, vy, vz = float(scale[0]), float(scale[1]), float(scale[2])
            voxel_x.value=vx
            voxel_y.value = vy
            voxel_z.value = vz

    image_combo.changed.connect(_on_image_changed)

    row_image = Container(layout="horizontal", widgets=[image_combo])
    row_image.native.layout().setSpacing(10)

    # ---------- NETWORK PARAMETERS  ----------
    title_net = Label(value="<b>Network parameters</b>")
    title_net.native.setAlignment(Qt.AlignCenter)

    net_size = ComboBox(label="Size", choices=["128", "256"], value="256")
    net_size.max_width = 80
    mode = ComboBox(label="Dimension", choices=["2D", "3D"], value="2D")
    mode.max_width = 80
    patches_mode = CheckBox(label="Patches Mode", value=True)

    # centered horizontal line
    row_net = Container(layout="horizontal")
    row_net.native.layout().addStretch(1)
    row_net.extend([net_size, mode])
    row_net.native.layout().addStretch(1)
    row_net.native.layout().setSpacing(20)

    # ---------- 3D PRED ----------
    title_3d = Label(value="<b>3D prediction</b>")
    image_shape = Label(value="[1219,1512,5112]")
    image_shape.max_width = 110
    image_z = ComboBox(label="Z axis", choices=[0, 1, 2], value=0)
    image_z.max_width = 60
    row_z = Container(layout="horizontal")
    row_z.extend([image_z, image_shape])



    # ---------- VOXEL SIZE ----------
    voxel_title = Label(value="Voxel size                  ")
    voxel_x = LineEdit(label="X",value="1.0")
    voxel_y = LineEdit(label="Y",value="1.0")
    voxel_z = LineEdit(label="Z",value="1.0")
    for v in (voxel_x, voxel_y, voxel_z):
        v.min_width = 50
        v.max_width = 50

    row_voxel = Container(layout="horizontal")
    row_voxel.extend([voxel_x, voxel_y, voxel_z])

    isotrope = CheckBox(label="Isotropic rescaling", value=True)

    # ---------- RUN ----------
    run_button = PushButton(text="Predict instance segmentation")
    run_button.max_width = 280


    def _on_run_clicked(event=None):
        """Run the segmentation pipeline on the currently selected image.

            This callback collects all widget parameters and calls
            :func:`morphodeep.model.run_instance_segmentation`, then adds the
            resulting labels as a new napari Labels layer.
        """
        layer = image_combo.value
        if layer is None:
            print("No image selected")
            return

        data = layer.data

        labels_arr = run_instance_segmentation(
            image=data,
            net_size=int(net_size.value),
            mode=str(mode.value),
            patches=bool(patches_mode.value),
            voxel_size=(
                float(voxel_x.value),
                float(voxel_y.value),
                float(voxel_z.value),
            ),
            isotrope=bool(isotrope.value),
            z_axis=int(image_z.value),
        )

        labels_layer = Labels(labels_arr, name=f"{layer.name}_instances")
        viewer.add_layer(labels_layer)

    run_button.clicked.connect(_on_run_clicked)

    # ---------- MAIN ----------
    main = Container(
        layout="vertical",
        widgets=[
            title_image,
            row_image,
            Label(value=""),
            title_net,
            row_net,
            patches_mode,
            Label(value=""),
            title_3d,
            row_z,
            voxel_title,
            row_voxel,
            isotrope,
            Label(value=""),
            run_button
        ],
    )
    main.native.layout().setAlignment(row_voxel.native, Qt.AlignRight)
    main.native.layout().setAlignment(voxel_title.native, Qt.AlignCenter)
    main.native.layout().setAlignment(run_button.native, Qt.AlignCenter)
    main.native.layout().setAlignment(row_net.native, Qt.AlignRight)
    main.native.layout().setAlignment(patches_mode.native, Qt.AlignCenter)
    main.native.layout().setAlignment(isotrope.native, Qt.AlignCenter)



    current = viewer.layers.selection.active
    if not isinstance(current, ImageLayer):
        current = next((ly for ly in viewer.layers if isinstance(ly, ImageLayer)), None)
    if current is not None:
        image_combo.value = current
        _on_image_changed()

    return main
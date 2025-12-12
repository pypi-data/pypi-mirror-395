from PySide6.QtWidgets import (QVBoxLayout, QLabel, QGroupBox, QGridLayout, QDialog, QDialogButtonBox, QCheckBox,
                               QComboBox, QDoubleSpinBox, QPushButton)


class DomainCreateDialog(QDialog):
    def __init__(self, managers, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create GBT Domain")
        self.setModal(True)
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = setup_domain_parameters(layout)
        prepare_domain_parameters(self.form, managers)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_data(self):
        return get_domain_parameters(self.form)


class DomainEdit(QGroupBox):
    def __init__(self, callback_fn, parent=None):
        super().__init__(parent)

        self.setWindowTitle("GBT Domain")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = setup_domain_parameters(layout)

        # Button
        apply_btn = QPushButton("Apply modifications")
        apply_btn.clicked.connect(callback_fn)
        layout.addWidget(apply_btn)

    def fill(self, data, managers):
        prepare_domain_parameters(self.form, managers)
        max_reflections, max_refractions = data['num_bounces']
        included_meshes = data.get('meshes', [])
        current_source_id = data['source']

        self.form['max_reflections'].setValue(max_reflections)
        self.form['max_refractions'].setValue(max_refractions)
        self.form['power_threshold'].setValue(data['power_threshold'])

        sources = get_gbt_compatible_sources(managers)
        i = 1
        for item_id, item in sources:
            if item_id == current_source_id:
                self.form['source'].setCurrentIndex(i)
            i += 1

        checkboxes = self.form['mesh_group'].findChildren(QCheckBox)
        for checkbox in checkboxes:
            checkbox.setChecked(checkbox.property('uuid') in included_meshes)

    def get_parameters(self):
        return get_domain_parameters(self.form)


def get_domain_parameters(form):
    """Retrieve all checked checkboxes from the group box"""
    checked_items = []

    # Method 1: Using findChildren to get all QCheckBox widgets
    checkboxes = form['mesh_group'].findChildren(QCheckBox)
    for checkbox in checkboxes:
        if checkbox.isChecked():
            checked_items.append(checkbox.property('uuid'))

    return {
        'num_bounces': (form['max_reflections'].value(), form['max_refractions'].value()),
        'power_threshold': form['power_threshold'].value(),
        'meshes': checked_items,
        'source': form['source'].currentData()
    }


def setup_domain_parameters(layout) -> dict:
    form = {
        'max_reflections': QDoubleSpinBox(decimals=0, value=2),
        'max_refractions': QDoubleSpinBox(decimals=0, value=4),
        'power_threshold': QDoubleSpinBox(decimals=8, value=1e-5),
        'source': QComboBox(),
        'mesh_group': QGroupBox("Included mesh(es)")
    }

    # File selection
    beam_tracing_group = QGroupBox("Gaussian Beam Tracing")
    beam_tracing_layout = QGridLayout()
    beam_tracing_group.setLayout(beam_tracing_layout)
    layout.addWidget(beam_tracing_group)

    beam_tracing_layout.addWidget(QLabel('Max. reflections'), 0, 0)
    beam_tracing_layout.addWidget(QLabel('Max. refractions'), 1, 0)
    beam_tracing_layout.addWidget(QLabel('Min power threshold'), 2, 0)

    beam_tracing_layout.addWidget(form['max_reflections'], 0, 1)
    beam_tracing_layout.addWidget(form['max_refractions'], 1, 1)
    beam_tracing_layout.addWidget(form['power_threshold'], 2, 1)

    # Connected source
    source_group = QGroupBox("Source")
    source_layout = QGridLayout()
    form['source'].addItem('None', None)
    source_layout.addWidget(form['source'])
    source_group.setLayout(source_layout)
    layout.addWidget(source_group)

    # Connected Mesh
    form['mesh_group'].setLayout(QVBoxLayout())
    layout.addWidget(form['mesh_group'])

    return form


def get_gbt_compatible_sources(managers) -> list:
    list_sources = managers[0].get_objects_by_type()['GBE']
    list_sources += managers[1].get_sources(only_type='NearFieldSource')
    list_sources += managers[1].get_sources(only_type='GaussianBeam')
    return list_sources


def prepare_domain_parameters(form, managers):
    # Connected source
    form['source'].clear()
    form['source'].addItem('None', None)
    sources = get_gbt_compatible_sources(managers)
    for item_id, item in sources:
        form['source'].addItem(item['name'], item_id)  # Display name, store ID

    # Enclosed meshes
    meshes_layout = form['mesh_group'].layout()
    while meshes_layout.count():
        child = meshes_layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

    objects = managers[0].get_objects_by_type()['StepMesh']
    objects += managers[0].get_objects_by_type()['ShapeMesh']
    objects += managers[0].get_objects_by_type()['LensMesh']
    for object_uuid, obj in objects:
        checkbox = QCheckBox(obj['name'])
        checkbox.setProperty('uuid', object_uuid)  # Store UUID as property
        meshes_layout.addWidget(checkbox)

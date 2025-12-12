from PySide6.QtWidgets import (QVBoxLayout, QLabel, QLineEdit, QGroupBox, QGridLayout, QDialog, QDialogButtonBox,
                               QComboBox, QPushButton, QDoubleSpinBox)


class NFGridCreateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Near Field Grid")
        self.setModal(True)
        self.resize(350, 360)

        # link objects
        object_manager = parent.object_manager if hasattr(parent, "object_manager") else None

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set fields and combobox
        self.form = setup_nf_parameters(layout)
        prepare_nf_parameters(self.form, object_manager)

        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_parameters(self):
        try:
            return get_nf_parameters(self.form)

        except ValueError as e:
            print(e)
            return None


class NFGridEdit(QDialog):
    def __init__(self, callback_fn, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Near Field Grid")
        self.setModal(True)
        self.resize(350, 360)

        # link objects

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set fields and combobox
        self.form = setup_nf_parameters(layout)

        # Bouton
        nf_request_update = QPushButton("Update")
        nf_request_update.clicked.connect(callback_fn)
        layout.addWidget(nf_request_update)

    def fill(self, data, managers):
        prepare_nf_parameters(self.form, managers[0], linked_domain_uuid=data.get('domain', None))

        self.form['u_start'].setValue(data['u_range'][0] * 1e3)
        self.form['u_stop'].setValue(data['u_range'][1] * 1e3)
        self.form['u_step'].setValue(data['u_range'][2] * 1e3)
        self.form['v_start'].setValue(data['v_range'][0] * 1e3)
        self.form['v_stop'].setValue(data['v_range'][1] * 1e3)
        self.form['v_step'].setValue(data['v_range'][2] * 1e3)
        self.form['n_value'] .setValue(data['n'] * 1e3)

        plane_map = {'XY': 0, 'ZX': 1, 'ZY': 2}
        self.form['plane'].setCurrentIndex(plane_map[data['plane']])

        field_map = {'E': 0, 'H': 1}
        self.form['field'].setCurrentIndex(field_map[data['field']])

    def get_parameters(self):
        try:
            return get_nf_parameters(self.form)

        except ValueError as e:
            print(e)
            return None


def get_nf_parameters(form):
    return {
        'u_range': (form['u_start'].value() * 1e-3, form['u_stop'].value() * 1e-3, form['u_step'].value() * 1e-3),
        'v_range': (form['v_start'].value() * 1e-3, form['v_stop'].value() * 1e-3, form['v_step'].value() * 1e-3),
        'n': form['n_value'].value() * 1e-3,
        'plane': form['plane'].currentData(),
        'field': form['field'].currentData(),
        'domain': form['domain'].currentData(),
    }


def setup_nf_parameters(layout) -> dict:
    # Initialization
    form = {
        'field': QComboBox(),
        'plane': QComboBox(),
        'domain': QComboBox(),
        'u_start': QDoubleSpinBox(decimals=3, value=-40, minimum=-1e6, maximum=1e6),
        'u_stop': QDoubleSpinBox(decimals=3, value=-40, minimum=-1e6, maximum=1e6),
        'u_step': QDoubleSpinBox(decimals=3, value=1),
        'v_start': QDoubleSpinBox(decimals=3, value=-40, minimum=-1e6, maximum=1e6),
        'v_stop': QDoubleSpinBox(decimals=3, value=-40, minimum=-1e6, maximum=1e6),
        'v_step': QDoubleSpinBox(decimals=3, value=1, minimum=-1e6, maximum=1e6),
        'n_value': QDoubleSpinBox(decimals=3, value=0, minimum=-1e6, maximum=1e6),
    }

    group1 = QLabel("")
    group_layout1 = QGridLayout()
    group1.setLayout(group_layout1)
    group1.setMinimumHeight(105)

    form['field'].addItem("E Field", 'E')
    form['field'].addItem("H Field", 'H')
    form['field'].addItem("E and H Fields", 'EH')

    form['plane'].addItem("XY", 'XY')
    form['plane'].addItem("ZX", 'ZX')
    form['plane'].addItem("ZY", "ZY")

    group_layout1.addWidget(QLabel("Field"), 0, 0)
    group_layout1.addWidget(form['field'], 0, 1, 1, 2)

    group_layout1.addWidget(QLabel("Domain"), 1, 0)
    group_layout1.addWidget(form['domain'], 1, 1, 1, 2)

    group_layout1.addWidget(QLabel("Plane"), 2, 0)
    group_layout1.addWidget(form['plane'], 2, 1, 1, 2)

    # Section for grid bounds
    group2 = QGroupBox("Bounds (mm)")
    group_layout2 = QGridLayout()
    group2.setLayout(group_layout2)
    min_label = QLabel("Min")
    max_label = QLabel("Max")
    step_label = QLabel("Step")
    min_label.setFixedHeight(10)
    max_label.setFixedHeight(10)
    step_label.setFixedHeight(10)
    group_layout2.addWidget(min_label, 0, 1)
    group_layout2.addWidget(max_label, 0, 2)
    group_layout2.addWidget(step_label, 0, 3)

    # U axis sampling
    group_layout2.addWidget(QLabel("U:"), 1, 0)
    form['u_start'].setMaximumWidth(80)
    group_layout2.addWidget(form['u_start'], 1, 1)
    form['u_stop'].setMaximumWidth(80)
    group_layout2.addWidget(form['u_stop'], 1, 2)
    form['u_step'].setMaximumWidth(80)
    group_layout2.addWidget(form['u_step'], 1, 3)

    # V axis sampling
    group_layout2.addWidget(QLabel("V:"), 2, 0)
    form['v_start'].setMaximumWidth(80)
    group_layout2.addWidget(form['v_start'], 2, 1)
    form['v_stop'].setMaximumWidth(80)
    group_layout2.addWidget(form['v_stop'], 2, 2)
    form['v_step'].setMaximumWidth(80)
    group_layout2.addWidget(form['v_step'], 2, 3)

    # N position
    group_layout2.addWidget(QLabel("N:"), 3, 0)
    form['n_value'].setMaximumWidth(80)
    group_layout2.addWidget(form['n_value'], 3, 1)

    layout.addWidget(group1)
    layout.addWidget(group2)

    return form

def prepare_nf_parameters(form, object_manager, linked_domain_uuid = None):
    list_domains = object_manager.get_objects_by_type()['Domain']
    form['domain'].clear()
    form['domain'].addItem('None', None)

    selected_id = 0
    i = 1
    for item_id, item in list_domains:
        form['domain'].addItem(item['name'], item_id)  # Display name, store ID"""
        if item_id == linked_domain_uuid:
            selected_id = i
        i += 1
    if selected_id is not None:
        form['domain'].setCurrentIndex(selected_id)


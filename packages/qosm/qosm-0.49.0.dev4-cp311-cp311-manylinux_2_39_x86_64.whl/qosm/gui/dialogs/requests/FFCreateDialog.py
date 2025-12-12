from PySide6.QtWidgets import (QVBoxLayout, QLabel, QLineEdit, QGroupBox, QGridLayout, QDialog, QDialogButtonBox,
                               QComboBox, QPushButton, QDoubleSpinBox)


class FFRequestCreateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Far Field Request")
        self.setModal(True)
        self.resize(350, 230)

        # link objects
        source_manager = parent.source_manager if hasattr(parent, "source_manager") else None

        # Initialization
        self.ff_horn_combo = None
        self.ff_phi_value = None
        self.ff_theta_start = None
        self.ff_theta_stop = None
        self.ff_theta_step = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set fields and combobox
        self.form = setup_ff_parameters(layout)
        prepare_ff_parameters(self.form, source_manager)

        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_parameters(self):
        try:
            return get_ff_parameters(self.form)

        except ValueError as e:
            print(e)
            return None


class FFRequestEdit(QDialog):
    def __init__(self, callback_fn, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Far Field Request")
        self.resize(350, 360)

        # link objects

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Set fields and combobox
        self.form = setup_ff_parameters(layout)

        # Bouton
        ff_request_update = QPushButton("Update")
        ff_request_update.clicked.connect(callback_fn)
        layout.addWidget(ff_request_update)

    def fill(self, data, managers):
        prepare_ff_parameters(self.form, managers[1], linked_horn_uuid=data.get('horn', None))

        self.form['phi_value'].setValue(data['phi'])
        self.form['theta_start'].setValue(data['theta_range'][0])
        self.form['theta_stop'].setValue(data['theta_range'][1])
        self.form['theta_step'].setValue(data['theta_range'][2])

    def get_parameters(self):
        try:
            return get_ff_parameters(self.form)

        except ValueError as e:
            print(e)
            return None


def get_ff_parameters(form):
    return {
        'horn': form['horn'].currentData(),
        'phi': form['phi_value'].value(),
        'theta_range': (form['theta_start'].value(), form['theta_stop'].value(), form['theta_step'].value()),
    }


def setup_ff_parameters(layout) -> dict:
    # Initialization
    form = {
        'horn': QComboBox(),
        'phi_value': QDoubleSpinBox(decimals=1, value=0, minimum=-360, maximum=360, suffix=' °'),
        'theta_start': QDoubleSpinBox(decimals=1, minimum=-90, maximum=90, value=-90, suffix=' °'),
        'theta_stop': QDoubleSpinBox(decimals=1, minimum=-90, maximum=90, value=90, suffix=' °'),
        'theta_step': QDoubleSpinBox(decimals=1, value=1, minimum=0.1, maximum=180, suffix=' °'),
    }

    group1 = QLabel("")
    group_layout1 = QGridLayout()
    group1.setLayout(group_layout1)
    group1.setMinimumHeight(90)

    group_layout1.addWidget(QLabel("Horn"), 0, 0)
    group_layout1.addWidget(form['horn'], 0, 1, 1, 2)

    group_layout1.addWidget(QLabel("Cut-plane φ"), 1, 0)
    group_layout1.addWidget(form['phi_value'], 1, 1)

    # Section for angle range
    group2 = QGroupBox("Theta Range")
    group_layout2 = QGridLayout()
    group2.setLayout(group_layout2)

    start_label = QLabel("Start")
    stop_label = QLabel("Stop")
    step_label = QLabel("Step")
    group_layout2.addWidget(start_label, 0, 1)
    group_layout2.addWidget(stop_label, 0, 2)
    group_layout2.addWidget(step_label, 0, 3)

    # Theta axis sampling
    group_layout2.addWidget(QLabel("θ:"), 1, 0)
    form['theta_start'].setMaximumWidth(80)
    group_layout2.addWidget(form['theta_start'], 1, 1)
    form['theta_stop'].setMaximumWidth(80)
    group_layout2.addWidget(form['theta_stop'], 1, 2)
    form['theta_step'].setMaximumWidth(80)
    group_layout2.addWidget(form['theta_step'], 1, 3)

    layout.addWidget(group1)
    layout.addWidget(group2)

    return form


def prepare_ff_parameters(form, source_manager, linked_horn_uuid=None):
    list_horns = source_manager.get_sources(only_type='Horn')
    form['horn'].clear()
    form['horn'].addItem('None', None)
    form['horn'].addItem('Current selected horn (if any)', 'current_selected_source')

    selected_id = 0
    if linked_horn_uuid == 'current_selected_source':
        selected_id = 1

    i = 2
    for item_id, item in list_horns:
        form['horn'].addItem(item['name'], item_id)  # Display name, store ID
        if item_id == linked_horn_uuid:
            selected_id = i
        i += 1

    form['horn'].setCurrentIndex(selected_id)
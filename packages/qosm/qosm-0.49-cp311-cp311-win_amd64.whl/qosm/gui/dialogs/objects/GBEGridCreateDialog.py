from PySide6.QtWidgets import (QVBoxLayout, QWidget, QLabel, QLineEdit, QGroupBox, QGridLayout, QDialog,
                               QDialogButtonBox, QRadioButton, QButtonGroup, QComboBox, QHBoxLayout, QDoubleSpinBox,
                               QPushButton, QAbstractSpinBox)
from qosm import PlaneType


class GBEGridCreateDialog(QDialog):
    def __init__(self, managers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create GBE Grid")
        self.setModal(True)
        self.resize(290, 400)

        self.form = {
            'source': QComboBox(),
            'gbe_plane': QComboBox(),
            'sampling_step': QDoubleSpinBox(),
            'sampling_unit': QComboBox(),
            'kappa': QDoubleSpinBox(),
            'u_min': QDoubleSpinBox(),
            'u_max': QDoubleSpinBox(),
            'v_min': QDoubleSpinBox(),
            'v_max': QDoubleSpinBox(),
            'n': QDoubleSpinBox(),
        }

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Connected source
        source_group = QGroupBox("Source to expand")
        source_layout = QGridLayout()
        self.form['source'] = QComboBox()
        self.form['source'].addItem('None', None)
        self.form['source'].addItem('Current active source', 'active_src_uuid')
        sources = get_gbe_compatible_sources(managers[0])
        for item_id, item in sources:
            self.form['source'].addItem(item['name'], item_id)  # Display name, store ID
        source_layout.addWidget(self.form['source'])
        source_group.setLayout(source_layout)
        layout.addWidget(source_group)

        # Plane
        self.setup_plane_section(layout)

        # Bounds
        self.setup_bounds_section(layout)

        # Resolution
        self.setup_sampling_section(layout)

        layout.addStretch()

        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def setup_plane_section(self, layout):
        """Section for plane selection"""
        group = QGroupBox("Plane")
        group_layout = QVBoxLayout()
        group.setLayout(group_layout)

        self.form['gbe_plane'] = QComboBox()
        self.form['gbe_plane'].addItem("XY", "XY")
        self.form['gbe_plane'].addItem("ZX", "ZX")
        self.form['gbe_plane'].addItem("ZY", "ZY")
        group_layout.addWidget(self.form['gbe_plane'])

        layout.addWidget(group)

    def setup_bounds_section(self, layout):
        """Section for grid bounds"""
        group = QGroupBox("Bounds")
        grid = QGridLayout()
        group.setLayout(grid)

        # set ranges
        to1 = QLabel("to")
        to2 = QLabel("to")
        to1.setFixedWidth(11)
        to2.setFixedWidth(11)
        grid.addWidget(QLabel("U:"), 0, 0)
        grid.addWidget(QLabel("V:"), 1, 0)
        grid.addWidget(to1, 0, 2)
        grid.addWidget(to2, 1, 2)
        items = ('u_min', 'u_max', 'v_min', 'v_max')
        values = (-40., 40., -40., 40.)
        for i, item in enumerate(items):
            self.form[item].setRange(-10000, 10000)
            self.form[item].setValue(values[i])
            self.form[item].setDecimals(4)
            self.form[item].setSuffix(' mm')
            grid.addWidget(self.form[item], i // 2, 2 * (i % 2) + 1)

        # N position
        grid.addWidget(QLabel("N:"), 2, 0)
        self.form['n'].setRange(-10000, 10000)
        self.form['n'].setValue(0.)
        self.form['n'].setDecimals(4)
        self.form['n'].setSuffix(' mm')
        self.form['n'].setMaximumWidth(120)
        grid.addWidget(self.form['n'], 2, 1)

        layout.addWidget(group)

    def setup_sampling_section(self, layout):

        """Section for grid resolution"""
        group = QGroupBox("Sampling")
        group_layout = QGridLayout()
        group.setLayout(group_layout)

        self.form['sampling_unit'] = QComboBox()
        self.form['sampling_unit'].addItem('λ', 'lambda')
        self.form['sampling_unit'].addItem('mm', 'mm')

        self.form['sampling_step'].setValue(1.)
        self.form['sampling_step'].setDecimals(4)
        self.form['sampling_step'].setSuffix(' λ')

        def handle_unit_changed():
            unit_txt = self.form['sampling_unit'].currentText()
            unit = self.form['sampling_unit'].currentData()
            self.form['sampling_step'].setSuffix(f" {unit_txt}")
            if unit == 'lambda':
                self.form['sampling_step'].setRange(0.8, 2.0)
            else:
                self.form['sampling_step'].setRange(0, 1000.)

        self.form['sampling_unit'].currentTextChanged.connect(handle_unit_changed)

        self.form['kappa'].setValue(1.)
        self.form['kappa'].setDecimals(2)
        self.form['kappa'].setRange(0.8, 1.5)

        self.kappa = QLineEdit("1")
        self.kappa.setMaximumWidth(80)

        group_layout.addWidget(QLabel('Unit'), 0, 0)
        group_layout.addWidget(self.form['sampling_unit'], 0, 1)
        group_layout.addWidget(QLabel('Step'), 1, 0)
        group_layout.addWidget(self.form['sampling_step'], 1, 1)
        group_layout.addWidget(QLabel('Overlapping factor'), 2, 0)
        group_layout.addWidget(self.form['kappa'], 2, 1)

        layout.addWidget(group)

    def get_parameters(self):
        f = self.form
        return {
            'u_range': [f['u_min'].value() * 1e-3, f['u_max'].value() * 1e-3],
            'v_range': [f['v_min'].value() * 1e-3, f['v_max'].value() * 1e-3],
            'sampling_step': f['sampling_step'].value(),
            'sampling_unit': f['sampling_unit'].currentData(),
            'kappa': f['kappa'].value(),
            'n': f['n'].value() * 1e-3,
            'plane': f['gbe_plane'].currentData(),
            'source': f['source'].currentData()
        }


class GBEGridEdit(QGroupBox):
    def __init__(self, callback_fn):
        super().__init__("Grid Parameters")

        self.grid_layout = QVBoxLayout()
        self.setLayout(self.grid_layout)

        self.form = {
            'size_u': QDoubleSpinBox(),
            'size_v': QDoubleSpinBox(),
            'sampling_step': QDoubleSpinBox(),
            'sampling_unit': QComboBox(),
            'kappa': QDoubleSpinBox(),
            'position_x': QDoubleSpinBox(),
            'position_y': QDoubleSpinBox(),
            'position_z': QDoubleSpinBox(),
            'reference':  QComboBox(),
            'source': QComboBox(),
        }

        self.setup_ui(callback_fn)

    def setup_ui(self, callback_fn):
        # set units and suffix and prefix
        self.form['size_u'].setSuffix(' mm')
        self.form['size_v'].setSuffix(' mm')
        self.form['position_x'].setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.form['position_y'].setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.form['position_z'].setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.form['position_x'].setPrefix('x: ')
        self.form['position_y'].setPrefix('y: ')
        self.form['position_z'].setPrefix('z: ')
        self.form['position_x'].setRange(-1e4, 1e4)
        self.form['position_y'].setRange(-1e4, 1e4)
        self.form['position_z'].setRange(-1e4, 1e4)
        self.form['position_x'].setDecimals(4)
        self.form['position_y'].setDecimals(4)
        self.form['position_z'].setDecimals(4)
        self.form['size_u'].setPrefix('u: ')
        self.form['size_v'].setPrefix('v: ')
        self.form['size_u'].setRange(0, 1e4)
        self.form['size_v'].setRange(0, 1e4)

        # Connected source
        source_group = QGroupBox("Source to expand")
        source_layout = QGridLayout()
        source_layout.addWidget(self.form['source'])
        source_group.setLayout(source_layout)
        self.grid_layout.addWidget(source_group)

        # Grid dimensions and sampling
        grid_sampling_group = QGroupBox("Sampling")
        grid_sampling_layout = QGridLayout()
        grid_sampling_group.setLayout(grid_sampling_layout)
        self.grid_layout.addWidget(grid_sampling_group)

        grid_sampling_layout.addWidget(QLabel("Size"), 0, 0)
        grid_sampling_layout.addWidget(self.form['size_u'], 0, 1)
        grid_sampling_layout.addWidget(self.form['size_v'], 0, 2)

        grid_sampling_group.setLayout(grid_sampling_layout)
        grid_sampling_layout.addWidget(QLabel("Step"), 2, 0)
        grid_sampling_layout.addWidget(self.form['sampling_step'], 2, 1)
        grid_sampling_layout.addWidget(self.form['sampling_unit'], 2, 2)
        grid_sampling_layout.addWidget(QLabel("kappa"), 3, 0)
        grid_sampling_layout.addWidget(self.form['kappa'], 3, 1)
        self.grid_layout.addWidget(grid_sampling_group)

        # Grid center position
        grid_position_group = QGroupBox("Center position (mm)")
        grid_position_layout = QGridLayout()
        grid_position_group.setLayout(grid_position_layout)

        grid_position_layout.addWidget(self.form['position_x'], 0, 0)
        grid_position_layout.addWidget(self.form['position_y'], 0, 1)
        grid_position_layout.addWidget(self.form['position_z'], 0, 2)

        grid_position_layout.addWidget(QLabel("Relative to:"), 1, 0)

        # Center on object selector
        reference_layout = QHBoxLayout()
        self.form['reference'].addItem("Absolute", None)
        reference_layout.addWidget(self.form['reference'])
        center_widget = QWidget()
        center_widget.setLayout(reference_layout)
        grid_position_layout.addWidget(center_widget, 1, 1, 1, 2)

        self.grid_layout.addWidget(grid_position_group)

        # Apply Grid button
        apply_grid_btn = QPushButton("Apply Grid Changes")
        self.grid_layout.addWidget(apply_grid_btn)
        apply_grid_btn.clicked.connect(callback_fn)

    def fill(self, data, managers):
        list_sources = get_gbe_compatible_sources(managers[0])
        list_objects = managers[0].get_objects_by_type()['StepMesh']
        list_objects += managers[0].get_objects_by_type()['ShapeMesh']
        list_objects += managers[0].get_objects_by_type()['LensMesh']
        grid_uuid = managers[0].active_object_uuid

        # Fill data
        self.form['sampling_unit'].clear()
        self.form['sampling_unit'].addItem('λ', 'lambda')
        self.form['sampling_unit'].addItem('mm', 'mm')
        self.form['sampling_unit'].addItem('m', 'm')
        unit_idx = {'lambda': 0, 'mm': 1}
        if data.get('sampling_unit', None) is None:
            data['sampling_unit'] = 'mm'
            data['sampling_step'] *= 1e3
        self.form['sampling_unit'].setCurrentIndex(unit_idx[data['sampling_unit']])
        self.form['size_u'].setValue(data['size_u'] * 1e3)
        self.form['size_v'].setValue(data['size_v'] * 1e3)
        self.form['kappa'].setValue(data['kappa'])
        self.form['sampling_step'].setValue(data['sampling_step'])
        self.form['position_x'].setValue(data['position'][0] * 1e3)
        self.form['position_y'].setValue(data['position'][1] * 1e3)
        self.form['position_z'].setValue(data['position'][2] * 1e3)

        self.form['source'].clear()
        self.form['source'].addItem('None', None)
        self.form['source'].addItem('Current active source', 'active_src_uuid')
        if data['source'] == 'active_src_uuid':
            self.form['source'].setCurrentIndex(1)
        i = 2
        for item_id, item in list_sources:
            if item_id == grid_uuid:
                continue
            self.form['source'].addItem(item['name'], item_id)  # Display name, store ID
            if item_id == data['source']:
                self.form['source'].setCurrentIndex(i)
            i += 1

        self.form['reference'].clear()
        self.form['reference'].addItem("Absolute", None)
        i = 1
        selected_uuid = 0
        for item_uuid, item in list_objects:
            self.form['reference'].addItem(item['name'], item_uuid)
            if item_uuid == data['reference']:
                selected_uuid = i
            i += 1
        self.form['reference'].setCurrentIndex(selected_uuid)

    def update_parameters(self, obj):
        obj['parameters']['size_u'] = self.form['size_u'].value() * 1e-3
        obj['parameters']['size_v'] = self.form['size_v'].value() * 1e-3
        obj['parameters']['sampling_step'] = self.form['sampling_step'].value()
        obj['parameters']['sampling_unit'] = self.form['sampling_unit'].currentData()
        obj['parameters']['kappa'] = self.form['kappa'].value()
        obj['parameters']['position'] = (self.form['position_x'].value() * 1e-3,
                                         self.form['position_y'].value() * 1e-3,
                                         self.form['position_z'].value() * 1e-3)
        obj['parameters']['source'] = self.form['source'].currentData()
        obj['parameters']['reference'] = self.form['reference'].currentData()



def get_gbe_compatible_sources(object_manager) -> list:
    list_sources = object_manager.get_objects_by_type()['Domain']
    list_sources += object_manager.get_objects_by_type()['GBE']
    return list_sources
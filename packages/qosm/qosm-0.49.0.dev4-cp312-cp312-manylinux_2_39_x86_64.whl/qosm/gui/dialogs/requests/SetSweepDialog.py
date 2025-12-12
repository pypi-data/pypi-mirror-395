from PySide6.QtWidgets import (QLabel, QLineEdit, QGroupBox, QGridLayout, QDialog, QDialogButtonBox, QComboBox,
                               QHBoxLayout)


class SetSweepDialog(QDialog):
    def __init__(self, parent=None, current_configuration=None):
        super().__init__(parent)
        self.setWindowTitle("Set Sweep")
        self.setModal(True)
        self.setFixedWidth(450)

        if not current_configuration:
            current_configuration = {
                'target': ('None', None),
                'attribute': 'None',
                'sweep': (0, 0, 1)
            }

        # link objects
        self.object_manager = parent.object_manager if hasattr(parent, "object_manager") else None
        self.source_manager = parent.source_manager if hasattr(parent, "source_manager") else None

        gbtc_objects = self.object_manager.get_objects_by_type()
        freq_sweep_enabled = len(gbtc_objects['GBTCPort']) == 0 and len(gbtc_objects['GBTCSample']) == 0

        layout = QGridLayout()
        self.setLayout(layout)

        step_list = self.object_manager.get_objects_by_type()['StepMesh']
        gbe_list = self.object_manager.get_objects_by_type()['GBE']
        gbtc_port_list = self.object_manager.get_objects_by_type()['GBTCPort']
        gbtc_sample_list = self.object_manager.get_objects_by_type()['GBTCSample']
        nfs_list = self.source_manager.get_sources(only_type='NearFieldSource')
        horn_list = self.source_manager.get_sources(only_type='Horn')

        layout.addWidget(QLabel('Applied on'), 0, 0)
        self.menu_target = QComboBox()
        self.menu_target.addItem('None', ('None', None))
        selected_idx = 0
        i = 1
        if freq_sweep_enabled:
            self.menu_target.addItem('Frequency [GHz]', ("freq_GHz", None))
            i += 1
            if current_configuration['target'][0] == 'freq_GHz':
                selected_idx = 1
        elif current_configuration['target'][0] == 'freq_GHz':
            current_configuration['target'] = (None, None)

        for step_uuid, step in step_list:
            self.menu_target.addItem(step['name'], ('step', step_uuid))
            if current_configuration['target'][1] == step_uuid:
                selected_idx = i
            i += 1
        for gbe_uuid, gbe in gbe_list:
            self.menu_target.addItem(gbe['name'], ('gbe',gbe_uuid))
            if current_configuration['target'][1] == gbe_uuid:
                selected_idx = i
            i += 1
        for src_uuid, src in nfs_list:
            self.menu_target.addItem(src['name'], ('nf_src', src_uuid))
            if current_configuration['target'][1] == src_uuid:
                selected_idx = i
            i += 1
        for src_uuid, src in horn_list:
            self.menu_target.addItem(src['name'], ('horn', src_uuid))
            if current_configuration['target'][1] == src_uuid:
                selected_idx = i
            i += 1
        for port_uuid, port in gbtc_port_list:
            self.menu_target.addItem(port['name'], ('gbtc_port', port_uuid))
            if current_configuration['target'][1] == port_uuid:
                selected_idx = i
            i += 1
        for sample_uuid, sample in gbtc_sample_list:
            self.menu_target.addItem(sample['name'], ('gbtc_sample', sample_uuid))
            if current_configuration['target'][1] == sample_uuid:
                selected_idx = i
            i += 1

        self.menu_target.setCurrentIndex(selected_idx)
        layout.addWidget(self.menu_target, 0, 1)

        self.menu_attr = QComboBox()
        self.menu_attr.setDisabled(True)
        layout.addWidget(self.menu_attr, 0, 2)

        self.num_points = QLineEdit(f"{int(current_configuration['sweep'][2]):.0f}")
        self.sweep_start = QLineEdit(f"{float(current_configuration['sweep'][0]):.5f}")
        self.sweep_stop = QLineEdit(f"{float(current_configuration['sweep'][1]):.5f}")
        self.group_sweep = QGroupBox('Sweep range')
        layout_sweep = QHBoxLayout()
        self.group_sweep.setLayout(layout_sweep)
        layout_sweep.addWidget(QLabel('From '))
        layout_sweep.addWidget(self.sweep_start)
        layout_sweep.addWidget(QLabel(' to '))
        layout_sweep.addWidget(self.sweep_stop)
        layout_sweep.addWidget(QLabel(' with '))
        layout_sweep.addWidget(self.num_points)
        layout_sweep.addWidget(QLabel(' pts '))
        layout.addWidget(self.group_sweep, 1, 0, 1, 3)

        def menu_changed(_):
            data = self.menu_target.currentData()

            self.menu_attr.setVisible(data[1] is not None)
            self.group_sweep.setVisible(data[0] != 'None')
            if data[1] is None:
                return

            self.menu_attr.clear()
            self.menu_attr.setDisabled(data[0] in ['freq_GHz', 'None'])

            if 'step' in data[0]:
                self.menu_attr.addItem('Position x', "pose.x")
                self.menu_attr.addItem('Position y', "pose.y")
                self.menu_attr.addItem('Position z', "pose.z")
                self.menu_attr.addItem('Rotation x', "pose.rx")
                self.menu_attr.addItem('Rotation y', "pose.ry")
                self.menu_attr.addItem('Rotation z', "pose.rz")
                pose_idx = {
                    "pose.x": 0, "pose.y": 1, "pose.z": 2,
                    "pose.rx": 3, "pose.ry": 4, "pose.rz": 5,
                }
                if current_configuration['attribute'] != 'None':
                    self.menu_attr.setCurrentIndex(pose_idx[current_configuration['attribute']])
            elif 'nf_src' in data[0]:
                self.menu_attr.addItem('Sampling step', "sampling_step_lambda")
                self.menu_attr.addItem('kappa', "kappa")
            elif 'horn' in data[0]:
                self.menu_attr.addItem('Aperture Lx', "a")
                self.menu_attr.addItem('Aperture Ly', "b")
                self.menu_attr.addItem('Aperture Lx and Ly (square)', "a_b")
            elif 'gbe' in data[0]:
                self.menu_attr.addItem('Sampling step', "sampling_step")
                self.menu_attr.addItem('kappa', "kappa")
            elif 'gbtc_port' in data[0] or 'gbtc_port' in data[0]:
                self.menu_attr.addItem('Offset x', "delta.x")
                self.menu_attr.addItem('Offset y', "delta.y")
                self.menu_attr.addItem('Offset z', "delta.z")
                if current_configuration['attribute'] != 'None':
                    delta_idx = {
                        "delta.x": 0, "delta.y": 1, "delta.z": 2
                    }
                    self.menu_attr.setCurrentIndex(delta_idx[current_configuration['attribute']])
            elif 'gbtc_sample' in data[0]:
                self.menu_attr.addItem('Rotation x', "pose.rx")
                self.menu_attr.addItem('Rotation y', "pose.ry")
                self.menu_attr.addItem('Rotation z', "pose.rz")
                if current_configuration['attribute'] != 'None':
                    pose_idx = {
                        "pose.rx": 0, "pose.ry": 1, "pose.rz": 2
                    }
                    self.menu_attr.setCurrentIndex(pose_idx[current_configuration['attribute']])

        self.menu_target.currentIndexChanged.connect(menu_changed)

        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box, 2, 0, 1, 3)

        menu_changed(None)

    def get_parameters(self):
        try:
            return {
                'target': self.menu_target.currentData(),
                'attribute': self.menu_attr.currentData(),
                'sweep': (float(self.sweep_start.text()), float(self.sweep_stop.text()), int(self.num_points.text()))
            }
        except ValueError:
            return None
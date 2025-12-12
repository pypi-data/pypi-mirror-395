from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QGridLayout,
                               QFileDialog, QDialog, QDialogButtonBox, QComboBox, QDoubleSpinBox, QAbstractSpinBox,
                               QCheckBox)
import os


class StepLoadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import STEP File")
        self.setModal(True)
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.form = setup_step_parameters(self, layout)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_parameters(self):
        return get_step_parameters(self.form)


class StepMeshEdit(QGroupBox):
    def __init__(self, callback_fn):
        super().__init__("Step Mesh")
        self.setWindowTitle('Step Mesh')

        step_mesh_layout = QVBoxLayout()
        self.setLayout(step_mesh_layout)

        self.form = setup_step_parameters(self, step_mesh_layout)

        # Apply Pose button
        apply_btn = QPushButton("Apply modifications")
        apply_btn.clicked.connect(callback_fn)
        step_mesh_layout.addWidget(apply_btn)

    def fill(self, data):
        """
        Fill the form with existing data

        Args:
            data: Dictionary containing STEP data with keys:
                - 'filepath': str
                - 'element_size': float
                - 'position': tuple (x, y, z)
                - 'rotation': tuple (rx, ry, rz)
                - 'medium': dict with 'type' and 'value' keys
                - 'scale': float (optional, defaults to 1e-3)
        """
        if data is None:
            return

        form = self.form

        if 'parameters' in data:
            data = data['parameters']

        try:
            # Set filepath
            filepath = data.get('filepath', '')
            if filepath:
                form['file']['filepath'].setText(filepath)
                # Set relative path checkbox based on whether path is relative
                form['file']['relative_checkbox'].setChecked(not os.path.isabs(filepath))

            # Set element size
            element_size = data.get('element_size', 4.0)
            form['file']['element_size'].setValue(element_size)

            # Set position
            position = data.get('position', (0.0, 0.0, 0.0))
            if len(position) >= 3:
                form['pose']['x'].setValue(position[0] * 1e3)
                form['pose']['y'].setValue(position[1] * 1e3)
                form['pose']['z'].setValue(position[2] * 1e3)

            # Set rotation
            rotation = data.get('rotation', (0.0, 0.0, 0.0))
            if len(rotation) >= 3:
                form['pose']['rx'].setValue(rotation[0])
                form['pose']['ry'].setValue(rotation[1])
                form['pose']['rz'].setValue(rotation[2])

            # Set medium
            medium = data.get('medium', {})
            if 'type' in medium:
                medium_type = medium['type']
                if 0 <= medium_type < form['medium']['type_combo_box'].count():
                    form['medium']['type_combo_box'].setCurrentIndex(medium_type)

            if 'value' in medium:
                medium_value = medium['value']
                if isinstance(medium_value, complex):
                    form['medium']['real_part'].setValue(medium_value.real)
                    form['medium']['imag_part'].setValue(medium_value.imag)
                else:
                    # Handle case where value is real number
                    form['medium']['real_part'].setValue(medium_value)
                    form['medium']['imag_part'].setValue(0.0)

        except (ValueError, KeyError, IndexError) as e:
            print(f"Error filling form: {e}")

    def get_parameters(self):
        return get_step_parameters(self.form)


def setup_step_parameters(self, layout) -> dict:
    form = {
        'medium': {
            'type_combo_box': QComboBox(),
            'real_part': QDoubleSpinBox(),
            'imag_part': QDoubleSpinBox(),
        },
        'file': {
            'filepath': QLineEdit(),
            'button': QPushButton("\U0001F4C1"),
            'element_size': QDoubleSpinBox(),
            'relative_checkbox': QCheckBox("Use relative path")
        },
        'pose': {
            'x': QDoubleSpinBox(),
            'y': QDoubleSpinBox(),
            'z': QDoubleSpinBox(),
            'rx': QDoubleSpinBox(),
            'ry': QDoubleSpinBox(),
            'rz': QDoubleSpinBox()
        }
    }

    form['medium']['real_part'].setDecimals(3)
    form['medium']['imag_part'].setRange(1e-6, 1e31)

    form['file']['button'].setFixedWidth(40)
    form['file']['button'].setStyleSheet('padding: 4px')
    form['file']['element_size'].setDecimals(2)
    form['file']['element_size'].setSuffix(' mm')
    form['pose']['x'].setPrefix('x: ')
    form['pose']['y'].setPrefix('y: ')
    form['pose']['z'].setPrefix('z: ')
    form['pose']['rx'].setPrefix('rx: ')
    form['pose']['ry'].setPrefix('ry: ')
    form['pose']['rz'].setPrefix('rz: ')

    for _, item in form['pose'].items():
        item.setValue(0.)
        item.setDecimals(4)
        item.setRange(-1e4, 1e4)
        item.setButtonSymbols(QAbstractSpinBox.NoButtons)

    def browse_file():
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a STEP file",
            "",
            "STEP Files (*.step *.stp);;All Files (*)"
        )
        if file_path:
            # Convert to relative path if checkbox is checked
            if form['file']['relative_checkbox'].isChecked():
                try:
                    file_path = os.path.relpath(file_path)
                except ValueError:
                    # If relative path conversion fails (different drives on Windows), keep absolute
                    pass
            form['file']['filepath'].setText(file_path)

    def on_relative_checkbox_changed(checked):
        current_path = form['file']['filepath'].text().strip()
        if not current_path:
            return

        try:
            if checked:
                # Convert to relative path
                if os.path.isabs(current_path):
                    relative_path = os.path.relpath(current_path)
                    form['file']['filepath'].setText(relative_path)
            else:
                # Convert to absolute path
                if not os.path.isabs(current_path):
                    absolute_path = os.path.abspath(current_path)
                    form['file']['filepath'].setText(absolute_path)
        except (ValueError, OSError):
            # If conversion fails, keep current path
            pass

    # Medium
    medium_group = QGroupBox("Medium")
    medium_layout = QGridLayout()
    medium_group.setLayout(medium_layout)
    layout.addWidget(medium_group)

    type_combo_box = form['medium']['type_combo_box']
    type_combo_box.addItem("Complex permittivity", 0)
    type_combo_box.addItem("Complex IOR", 1)
    type_combo_box.addItem("PEC", 2)
    medium_layout.addWidget(type_combo_box, 0, 0, 1, 4)

    # Set placeholders for medium
    form['medium']['real_part'].setValue(1.0)
    form['medium']['imag_part'].setValue(0.0)
    label1 = QLabel(" - ")
    label2 = QLabel("j")
    label1.setFixedWidth(16)
    label2.setFixedWidth(11)
    medium_layout.addWidget(form['medium']['real_part'], 1, 0)
    medium_layout.addWidget(label1, 1, 1)
    medium_layout.addWidget(form['medium']['imag_part'], 1, 2)
    medium_layout.addWidget(label2, 1, 3)

    def update_medium_parameters():
        hidden = form['medium']['type_combo_box'].currentIndex() == 2
        form['medium']['real_part'].setHidden(hidden)
        form['medium']['imag_part'].setHidden(hidden)
        label1.setHidden(hidden)
        label2.setHidden(hidden)

    type_combo_box.currentTextChanged.connect(update_medium_parameters)

    # File selection
    file_group = QGroupBox("STEP File")
    file_layout = QGridLayout()
    file_group.setLayout(file_layout)

    file_select_layout = QHBoxLayout()
    file_path = form['file']['filepath']
    file_path.setPlaceholderText("Select a STEP file...")
    browse_btn = QPushButton("\U0001F4C1")
    browse_btn.setStyleSheet('padding: 4px')
    browse_btn.clicked.connect(browse_file)
    browse_btn.setFixedWidth(40)

    file_select_layout.addWidget(file_path)
    file_select_layout.addWidget(browse_btn)
    file_layout.addLayout(file_select_layout, 0, 0, 1, 2)

    # Add relative path checkbox
    relative_checkbox = form['file']['relative_checkbox']
    relative_checkbox.setChecked(True)  # Default to relative paths
    relative_checkbox.toggled.connect(on_relative_checkbox_changed)
    file_layout.addWidget(relative_checkbox, 1, 0, 1, 2)

    file_layout.addWidget(QLabel('Mesh element size'), 2, 0)
    form['file']['element_size'].setValue(4.0)
    file_layout.addWidget(form['file']['element_size'], 2, 1)

    layout.addWidget(file_group)

    # Initial pose setup
    pose_group = QGroupBox("Pose")
    pose_layout = QGridLayout()
    pose_group.setLayout(pose_layout)
    layout.addWidget(pose_group)

    # Position
    pose_layout.addWidget(QLabel("Position (mm):"), 0, 0, 1, 3)
    pose_layout.addWidget(form['pose']['x'], 1, 0)
    pose_layout.addWidget(form['pose']['y'], 1, 1)
    pose_layout.addWidget(form['pose']['z'], 1, 2)

    # Rotation (in degrees)
    pose_layout.addWidget(QLabel("Rotation (°):"), 2, 0, 1, 3)
    pose_layout.addWidget(form['pose']['rx'], 3, 0)
    pose_layout.addWidget(form['pose']['ry'], 3, 1)
    pose_layout.addWidget(form['pose']['rz'], 3, 2)

    return form


def get_step_parameters(form):
    try:
        s = 1e-3
        filepath = form['file']['filepath'].text().strip()

        # Ensure we have a valid file path
        if not filepath:
            print("Error: No file path specified")
            return None

        # Convert relative path to absolute for internal use if needed
        # but keep the original path format as entered by user
        return {
            'position': (form['pose']['x'].value() * s, form['pose']['y'].value() * s, form['pose']['z'].value() * s),
            'rotation': (form['pose']['rx'].value(), form['pose']['ry'].value(), form['pose']['rz'].value()),
            'filepath': filepath,
            'medium': {
                'type': form['medium']['type_combo_box'].currentIndex(),
                'value': form['medium']['real_part'].value() - 1j * form['medium']['imag_part'].value()
            },
            'scale': 1e-3,
            'element_size': form['file']['element_size'].value()
        }
    except ValueError as e:
        print(f"Error parsing parameters: {e}")
        return None


# Example usage
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dialog = StepLoadDialog()

    if dialog.exec() == QDialog.Accepted:
        params = dialog.get_parameters()
        if params:
            print("STEP parameters:", params)
        else:
            print("Invalid parameters")

    sys.exit()
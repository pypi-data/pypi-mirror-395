import os
import sys

from PySide6.QtWidgets import (QVBoxLayout, QLabel, QLineEdit, QGroupBox, QDialog, QHBoxLayout, QDialogButtonBox,
                               QPushButton, QFileDialog, QTextEdit, QMessageBox, QProgressBar, QApplication, QMainWindow, QDoubleSpinBox, QComboBox, QGridLayout)

from numpy import linspace

from qosm.gui.objects import TicraFileLoader, FekoFileLoader

class NFSourceCreateDialog(QDialog):
    """
    Dialog for creating grids from NF files.

    This dialog allows users to select and load near-field files
    and displays information about the loaded data.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Grid from Near Field Files")
        self.setModal(True)
        self.resize(450, 750)

        self.forms = {
            'ticra': {},
            'feko': {},
            'hfss': {},
        }

        self.resampling_form = {}
        self.resampling_group = QGroupBox()

        self.groups = {
            'ticra': QGroupBox(),
            'feko': QGroupBox(),
            'hfss': QGroupBox(),
        }

        self.data = {
            'ticra': None,
            'feko': None,
            'hfss': None,
        }
        self.size_limits = (0, 0)

        self.loader_thread = None
        self.source_combo_box = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Source selection
        self.setup_file_source_section(layout)

        # Files selection
        self.setup_feko_section(layout)
        self.setup_ticra_section(layout)
        self.setup_hfss_section(layout)

        # Load button
        self.setup_load_section(layout)

        # Information on loaded file
        self.setup_info_section(layout)

        # Grid resampling
        self.setup_resampling_section(layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)
        layout.addWidget(button_box)

        self.handle_source_change()

    def setup_ticra_section(self, layout):

        group = QGroupBox("TICRA Files")
        group_layout = QVBoxLayout()
        group.setLayout(group_layout)

        form = {
            'e_grd_path': QLineEdit(),
            'e_grd_button': QPushButton("\U0001F4C1"),
            'h_grd_path': QLineEdit(),
            'h_grd_button': QPushButton("\U0001F4C1"),
            'z_position_spinbox': QDoubleSpinBox(),
            'units_combo_box': QComboBox()
        }

        def browse_e_grd_file():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select E-field GRD File", "", "GRD Files (*.grd);;All Files (*)"
            )
            if file_path:
                form['e_grd_path'].setText(file_path)

        def browse_h_grd_file():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select H-field GRD File", "", "GRD Files (*.grd);;All Files (*)"
            )
            if file_path:
                form['h_grd_path'].setText(file_path)

        e_grd_layout = QHBoxLayout()
        e_grd_layout.addWidget(QLabel("E-field GRD:"))
        form['e_grd_path'].setPlaceholderText("Select E-field GRD file...")
        e_grd_layout.addWidget(form['e_grd_path'])

        form['e_grd_button'].setFixedWidth(40)
        form['e_grd_button'].setStyleSheet('padding: 4px')
        form['e_grd_button'].clicked.connect(browse_e_grd_file)
        e_grd_layout.addWidget(form['e_grd_button'])
        group_layout.addLayout(e_grd_layout)

        h_grd_layout = QHBoxLayout()
        h_grd_layout.addWidget(QLabel("H-field GRD:"))
        form['h_grd_path'] = QLineEdit()
        form['h_grd_path'].setPlaceholderText("Select H-field GRD file...")
        h_grd_layout.addWidget(form['h_grd_path'])

        form['h_grd_button'].setFixedWidth(40)
        form['h_grd_button'].setStyleSheet('padding: 4px')
        form['h_grd_button'].clicked.connect(browse_h_grd_file)
        h_grd_layout.addWidget(form['h_grd_button'])
        group_layout.addLayout(h_grd_layout)

        z_layout = QHBoxLayout()
        z_layout.addWidget(QLabel("Z Position (units):"))
        form['z_position_spinbox'].setRange(-1000.0, 1000.0)
        form['z_position_spinbox'].setValue(50.0)
        form['z_position_spinbox'].setDecimals(5)
        z_layout.addWidget(form['z_position_spinbox'])
        z_layout.addStretch()
        group_layout.addLayout(z_layout)

        units_layout = QHBoxLayout()
        units_layout.addWidget(QLabel("File units:"))
        form['units_combo_box'].addItem('mm', 1e-3)
        form['units_combo_box'].addItem('cm', 1e-2)
        form['units_combo_box'].addItem('m', 1.)
        units_layout.addWidget(form['units_combo_box'])
        units_layout.addStretch()
        group_layout.addLayout(units_layout)

        layout.addWidget(group)

        form['e_grd_path'].textChanged.connect(self.check_file_paths)
        form['h_grd_path'].textChanged.connect(self.check_file_paths)

        self.forms['ticra'] = form
        self.groups['ticra'] = group

    def setup_feko_section(self, layout):

        group = QGroupBox("FEKO Files")
        group_layout = QVBoxLayout()
        group.setLayout(group_layout)

        form = {
            'efe_path': QLineEdit(),
            'efe_button': QPushButton("\U0001F4C1")
        }

        def browse_efe_file():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select EFE File", "", "EFE Files (*.efe);;All Files (*)"
            )
            if file_path:
                form['efe_path'].setText(file_path)

        e_grd_layout = QHBoxLayout()
        e_grd_layout.addWidget(QLabel("E-field :"))
        form['efe_path'].setPlaceholderText("Select EFE file...")
        e_grd_layout.addWidget(form['efe_path'])

        form['efe_button'].setFixedWidth(40)
        form['efe_button'].setStyleSheet('padding: 4px')
        form['efe_button'].clicked.connect(browse_efe_file)
        e_grd_layout.addWidget(form['efe_button'])
        group_layout.addLayout(e_grd_layout)

        layout.addWidget(group)

        form['efe_path'].textChanged.connect(self.check_file_paths)

        self.forms['feko'] = form
        self.groups['feko'] = group

    def setup_hfss_section(self, layout):

        group = QGroupBox("HFSS Files")
        group_layout = QVBoxLayout()
        group.setLayout(group_layout)

        form = {
            'e_csv_path': QLineEdit(),
            'e_csv_button': QPushButton("\U0001F4C1"),
            'h_csv_path': QLineEdit(),
            'h_csv_button': QPushButton("\U0001F4C1"),
            'z_position_spinbox': QDoubleSpinBox(),
            'units_combo_box': QComboBox()
        }

        def browse_e_csv_file():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select E-field CSV File", "", "CSV Files (*.csv);;All Files (*)"
            )
            if file_path:
                form['e_csv_path'].setText(file_path)

        def browse_h_csv_file():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select H-field CSV File", "", "CSV Files (*.csv);;All Files (*)"
            )
            if file_path:
                form['h_csv_path'].setText(file_path)

        e_grd_layout = QHBoxLayout()
        e_grd_layout.addWidget(QLabel("E-field CSV:"))
        form['e_csv_path'].setPlaceholderText("Select E-field CSV file...")
        e_grd_layout.addWidget(form['e_csv_path'])

        form['e_csv_button'].setFixedWidth(40)
        form['e_csv_button'].setStyleSheet('padding: 4px')
        form['e_csv_button'].clicked.connect(browse_e_csv_file)
        e_grd_layout.addWidget(form['e_csv_button'])
        group_layout.addLayout(e_grd_layout)

        h_grd_layout = QHBoxLayout()
        h_grd_layout.addWidget(QLabel("H-field CSV:"))
        form['h_csv_path'] = QLineEdit()
        form['h_csv_path'].setPlaceholderText("Select H-field CSV file...")
        h_grd_layout.addWidget(form['h_csv_path'])

        form['h_csv_button'].setFixedWidth(40)
        form['h_csv_button'].setStyleSheet('padding: 4px')
        form['h_csv_button'].clicked.connect(browse_h_csv_file)
        h_grd_layout.addWidget(form['h_csv_button'])
        group_layout.addLayout(h_grd_layout)

        z_layout = QHBoxLayout()
        z_layout.addWidget(QLabel("Z Position (mm):"))
        form['z_position_spinbox'].setRange(-1000.0, 1000.0)
        form['z_position_spinbox'].setValue(50.0)
        form['z_position_spinbox'].setDecimals(5)
        form['z_position_spinbox'].setSuffix(" mm")
        z_layout.addWidget(form['z_position_spinbox'])
        z_layout.addStretch()
        group_layout.addLayout(z_layout)

        units_layout = QHBoxLayout()
        units_layout.addWidget(QLabel("File units:"))
        form['units_combo_box'].addItem('mm', 1e-3)
        form['units_combo_box'].addItem('cm', 1e-2)
        form['units_combo_box'].addItem('m', 1.)
        units_layout.addWidget(form['units_combo_box'])
        units_layout.addStretch()
        group_layout.addLayout(units_layout)

        layout.addWidget(group)

        form['e_csv_path'].textChanged.connect(self.check_file_paths)
        form['h_csv_path'].textChanged.connect(self.check_file_paths)

        self.forms['hfss'] = form
        self.groups['hfss'] = group

    def check_file_paths(self):
        sw_src = self.source_combo_box.currentData()
        form = self.forms[sw_src]
        if sw_src == 'feko':
            hfe_path = form['efe_path'].text().replace('.efe', '.hfe')
            efe_valid = os.path.exists(form['efe_path'].text())
            hfe_valid = os.path.exists(hfe_path)
            self.load_button.setEnabled(efe_valid and hfe_valid)
        elif sw_src == 'ticra':
            e_grd_valid = os.path.exists(form['e_grd_path'].text())
            h_grd_valid = os.path.exists(form['h_grd_path'].text())
            self.load_button.setEnabled(e_grd_valid and h_grd_valid)

    def setup_file_source_section(self, layout):
        group_layout = QGridLayout()
        self.source_combo_box = QComboBox()
        self.source_combo_box.addItem('Feko', 'feko')
        self.source_combo_box.addItem('Ticra', 'ticra')
        self.source_combo_box.addItem('HFSS', 'hfss')
        self.source_combo_box.currentTextChanged.connect(self.handle_source_change)

        group_layout.addWidget(QLabel('Software'), 0, 0)
        group_layout.addWidget(self.source_combo_box, 0, 1, 1, 2)

        layout.addLayout(group_layout)

    def handle_source_change(self):
        sw_src = self.source_combo_box.currentData()
        for _, item in self.groups.items():
            item.setHidden(True)

        self.groups[sw_src].setHidden(False)
        self.check_file_paths()
        self.reset_file_info()

    def setup_load_section(self, layout):
        self.load_button = QPushButton("Load Files")
        self.load_button.clicked.connect(self.load_files)
        self.load_button.setEnabled(False)
        layout.addWidget(self.load_button)

    def setup_info_section(self, layout):
        """Section d'informations sur les fichiers chargés"""
        group = QGroupBox("File Information")
        group_layout = QVBoxLayout()
        group.setLayout(group_layout)

        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setPlaceholderText("Load files to see information...")
        group_layout.addWidget(self.info_text)

        layout.addWidget(group)

    def setup_resampling_section(self, layout):
        self.resampling_group = QGroupBox("Input Grid Resampling (for GBE)")
        group_layout = QGridLayout()
        self.resampling_group.setLayout(group_layout)

        self.resampling_form = {
            'sampling_step_lambda': QDoubleSpinBox(),
            'kappa': QDoubleSpinBox(),
            'max_width_lambda': QDoubleSpinBox(),
            'max_height_lambda': QDoubleSpinBox(),
        }

        self.resampling_form['sampling_step_lambda'].setRange(0.001, 10.0)
        self.resampling_form['sampling_step_lambda'].setValue(1.0)
        self.resampling_form['sampling_step_lambda'].setDecimals(8)
        self.resampling_form['sampling_step_lambda'].setSuffix(" λ")

        self.resampling_form['kappa'].setRange(0.5, 2.0)
        self.resampling_form['kappa'].setValue(1.0)
        self.resampling_form['kappa'].setDecimals(2)

        self.resampling_form['max_width_lambda'].setRange(0, 100.0)
        self.resampling_form['max_width_lambda'].setDecimals(8)
        self.resampling_form['max_width_lambda'].setSuffix(" λ")

        self.resampling_form['max_height_lambda'].setRange(0, 100.0)
        self.resampling_form['max_height_lambda'].setDecimals(8)
        self.resampling_form['max_height_lambda'].setSuffix(" λ")

        def check_values():
            step_lambda = self.resampling_form['sampling_step_lambda'].value()
            if step_lambda > 2. or step_lambda < 0.9:
                self.resampling_form['sampling_step_lambda'].setStyleSheet('QDoubleSpinBox {color: #dd8888}')
                self.ok_button.setEnabled(False)
            else:
                self.resampling_form['sampling_step_lambda'].setStyleSheet(None)
                self.ok_button.setEnabled(True)

            kappa = self.resampling_form['kappa'].value()
            if kappa > 1.5 or kappa < 0.8:
                self.resampling_form['kappa'].setStyleSheet('QDoubleSpinBox {color: #dd8888}')
                self.ok_button.setEnabled(False)
            else:
                self.resampling_form['kappa'].setStyleSheet(None)
                self.ok_button.setEnabled(True)

            width_lambda = self.resampling_form['max_width_lambda'].value()
            height_lambda = self.resampling_form['max_height_lambda'].value()

            self.ok_button.setEnabled(True)
            self.resampling_form['max_width_lambda'].setStyleSheet(None)
            self.resampling_form['max_height_lambda'].setStyleSheet(None)

            if width_lambda > self.size_limits[0] + step_lambda:
                self.resampling_form['max_width_lambda'].setStyleSheet('QDoubleSpinBox {color: #dd8888}')
                self.ok_button.setEnabled(False)

            if height_lambda > self.size_limits[1] + step_lambda:
                self.resampling_form['max_height_lambda'].setStyleSheet('QDoubleSpinBox {color: #dd8888}')
                self.ok_button.setEnabled(False)

        self.resampling_form['sampling_step_lambda'].valueChanged.connect(check_values)
        self.resampling_form['max_width_lambda'].valueChanged.connect(check_values)
        self.resampling_form['max_height_lambda'].valueChanged.connect(check_values)
        self.resampling_form['kappa'].valueChanged.connect(check_values)

        group_layout.addWidget(QLabel('Sampling'), 0, 0)
        group_layout.addWidget(QLabel('kappa'), 1, 0)
        group_layout.addWidget(QLabel('Max. Width'), 2, 0)
        group_layout.addWidget(QLabel('Max. Height'), 3, 0)

        i = 0
        for _, item in self.resampling_form.items():
            group_layout.addWidget(item, i, 1)
            i += 1

        self.resampling_group.setDisabled(True)
        layout.addWidget(self.resampling_group)

    def load_files(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.load_button.setEnabled(False)

        sw_src = self.source_combo_box.currentData()
        form = self.forms[sw_src]

        if sw_src == 'ticra':
            self.loader_thread = TicraFileLoader(
                form['e_grd_path'].text(),
                form['h_grd_path'].text(),
                z_plane=form['z_position_spinbox'].value()
            )
        elif sw_src == 'feko':
            efe_path = form['efe_path'].text()
            hfe_path = efe_path.replace('.efe', '.hfe')
            self.loader_thread = FekoFileLoader(efe_path, hfe_path)
        else:
            return

        self.loader_thread.progress.connect(self.progress_bar.setValue)
        self.loader_thread.finished_loading.connect(self.on_files_loaded)
        self.loader_thread.error_occurred.connect(self.on_loading_error)
        self.loader_thread.start()

    def on_files_loaded(self, data):
        """Callback when files are loaded"""
        sw_src = self.source_combo_box.currentData()
        self.data[sw_src] = data
        self.progress_bar.setVisible(False)
        self.load_button.setEnabled(True)

        self.ok_button.setEnabled(True)
        self.update_file_info()

    def on_loading_error(self, error_msg):
        """Callback in case of error during file loading"""
        self.progress_bar.setVisible(False)
        self.load_button.setEnabled(True)
        self.resampling_group.setEnabled(False)
        QMessageBox.critical(self, "Loading Error", f"Error loading files:\n{error_msg}")

    def reset_file_info(self):
        info_lines = []
        self.info_text.setPlainText("\n".join(info_lines))
        self.resampling_group.setEnabled(False)
        self.ok_button.setEnabled(False)
        for _, data in self.data.items():
            data = None

    def update_file_info(self):
        """Update file information"""
        sw_src = self.source_combo_box.currentData()
        if not self.data[sw_src]:
            return

        data = self.data[sw_src]
        metadata = data['metadata']
        grid_info = data['grid_info']

        info_lines = [f"Source: {metadata.get('source_name', 'Unknown')}"]

        unit = 1.

        if sw_src == 'ticra':
            unit = self.forms[sw_src]['units_combo_box'].currentData()
            unit_name = self.forms[sw_src]['units_combo_box'].currentText()

            # General Information
            info_lines.append(f"File Format: TICRA {metadata.get('version', 'Unknown')}")
            info_lines.append(f"Source: {metadata.get('source_name', 'Unknown')}")
            info_lines.append(f"Frequency: {data['frequency_GHz']:.3f} GHz")
            info_lines.append(f"File Units: {unit_name} ({unit} m)")

            # Specific TICRA information
            if 'nset' in metadata:
                info_lines.append(f"NSET (field sets): {metadata['nset']}")
            if 'icomp' in metadata:
                info_lines.append(f"ICOMP (field components): {metadata['icomp']}")
            if 'ncomp' in metadata:
                info_lines.append(f"NCOMP (components): {metadata['ncomp']}")
            if 'igrid' in metadata:
                info_lines.append(f"IGRID (grid type): {metadata['igrid']}")

        elif sw_src == 'feko':
            info_lines.append(f"Frequency: {data['frequency_GHz']:.3f} GHz")

        # Grid information
        if 'nx' in metadata and 'ny' in metadata:
            info_lines.append(f"Grid Dimensions: {metadata['nx']} × {metadata['ny']}")

        info_lines.append(f"Total Points: {data['e_field'].shape[0]}")

        x_min, x_max, x_samples = grid_info['x_range']
        y_min, y_max, y_samples = grid_info['y_range']
        z_min, z_max, z_samples = grid_info['z_range']

        x_min *= unit
        x_max *= unit
        y_min *= unit
        y_max *= unit
        z_min *= unit
        z_max *= unit

        data['points'] *= unit
        grid_info['x_range'][0] = x_min
        grid_info['x_range'][1] = x_max
        grid_info['y_range'][0] = y_min
        grid_info['y_range'][1] = y_max
        grid_info['z_range'][0] = z_min
        grid_info['z_range'][1] = z_max

        info_lines.append(
            f"X range: {x_min * 1000:.2f} to {x_max * 1000:.2f} mm ({x_samples:.0f} pt(s))")
        info_lines.append(
            f"Y range: {y_min * 1000:.2f} to {y_max * 1000:.2f} mm ({y_samples:.0f} pt(s))")
        info_lines.append(f"Z position: {z_min * 1000:.2f} mm")

        self.info_text.setPlainText("\n".join(info_lines))

        lambda_0 = 299792458. / (data['frequency_GHz'] * 1e9)

        u = linspace(x_min, x_max, x_samples, endpoint=True)
        step_lambda = round((u[1] - u[0]) / lambda_0, 8)
        width_lambda = (x_samples - 1) * step_lambda
        height_lambda = (y_samples - 1) * step_lambda
        self.size_limits = (width_lambda, height_lambda)

        self.resampling_form['sampling_step_lambda'].setValue(step_lambda)
        self.resampling_form['max_width_lambda'].setValue(width_lambda)
        self.resampling_form['max_height_lambda'].setValue(height_lambda)

        self.resampling_group.setEnabled(True)

    def get_data(self):
        sw_src = self.source_combo_box.currentData()
        if not self.data[sw_src]:
            return None

        resampling_data = {
            'sampling_step_lambda': self.resampling_form['sampling_step_lambda'].value(),
            'kappa': self.resampling_form['kappa'].value(),
            'max_width_lambda': self.resampling_form['max_width_lambda'].value(),
            'max_height_lambda': self.resampling_form['max_height_lambda'].value(),
        }
        data = self.data[sw_src] | resampling_data

        return data


class NFSourceEditDialog(QDialog):
    """
    Dialog for editing grids from NF files.

    This dialog allows users to edit a loaded near-field files
    """

    def __init__(self, parent=None, data=None, name=None):
        super().__init__(parent)
        if name:
            self.setWindowTitle(f"{name}: Near Field Input Resampling")
        else:
            self.setWindowTitle("Near Field Input Resampling")
        self.setModal(True)
        self.resize(300, 150)

        self.resampling_form = {}
        self.size_limits = (0, 0)

        self.frequency_GHz = 0

        layout = QGridLayout()
        self.setLayout(layout)

        # Grid resampling
        self.setup_resampling_section(layout)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)
        layout.addWidget(button_box, 10, 0, 1, 2)

        if data is not None:
            self.update_form(data)

    def setup_resampling_section(self, layout):
        self.resampling_form = {
            'sampling_step_lambda': QDoubleSpinBox(),
            'kappa': QDoubleSpinBox(),
            'max_width_lambda': QDoubleSpinBox(),
            'max_height_lambda': QDoubleSpinBox(),
        }

        self.resampling_form['sampling_step_lambda'].setRange(0.001, 10.0)
        self.resampling_form['sampling_step_lambda'].setValue(1.0)
        self.resampling_form['sampling_step_lambda'].setDecimals(12)
        self.resampling_form['sampling_step_lambda'].setSuffix(" λ")

        self.resampling_form['kappa'].setRange(0.5, 2.0)
        self.resampling_form['kappa'].setValue(1.0)
        self.resampling_form['kappa'].setDecimals(2)

        self.resampling_form['max_width_lambda'].setRange(0, 100.0)
        self.resampling_form['max_width_lambda'].setDecimals(12)
        self.resampling_form['max_width_lambda'].setSuffix(" λ")

        self.resampling_form['max_height_lambda'].setRange(0, 100.0)
        self.resampling_form['max_height_lambda'].setDecimals(12)
        self.resampling_form['max_height_lambda'].setSuffix(" λ")

        def check_values():
            step_lambda = self.resampling_form['sampling_step_lambda'].value()
            if step_lambda > 2. or step_lambda < 0.9:
                self.resampling_form['sampling_step_lambda'].setStyleSheet('QDoubleSpinBox {color: #dd8888}')
                self.ok_button.setEnabled(False)
            else:
                self.resampling_form['sampling_step_lambda'].setStyleSheet(None)
                self.ok_button.setEnabled(True)

            kappa = self.resampling_form['kappa'].value()
            if kappa > 1.5 or kappa < 0.8:
                self.resampling_form['kappa'].setStyleSheet('QDoubleSpinBox {color: #dd8888}')
                self.ok_button.setEnabled(False)
            else:
                self.resampling_form['kappa'].setStyleSheet(None)
                self.ok_button.setEnabled(True)

            width_lambda = self.resampling_form['max_width_lambda'].value()
            height_lambda = self.resampling_form['max_height_lambda'].value()

            self.ok_button.setEnabled(True)
            self.resampling_form['max_width_lambda'].setStyleSheet(None)
            self.resampling_form['max_height_lambda'].setStyleSheet(None)

            if width_lambda > self.size_limits[0] + step_lambda:
                self.resampling_form['max_width_lambda'].setStyleSheet('QDoubleSpinBox {color: #dd8888}')
                self.ok_button.setEnabled(False)

            if height_lambda > self.size_limits[1] + step_lambda:
                self.resampling_form['max_height_lambda'].setStyleSheet('QDoubleSpinBox {color: #dd8888}')
                self.ok_button.setEnabled(False)

        self.resampling_form['sampling_step_lambda'].valueChanged.connect(check_values)
        self.resampling_form['kappa'].valueChanged.connect(check_values)
        self.resampling_form['max_width_lambda'].valueChanged.connect(check_values)
        self.resampling_form['max_height_lambda'].valueChanged.connect(check_values)

        layout.addWidget(QLabel('Sampling'), 0, 0)
        layout.addWidget(QLabel('kappa'), 1, 0)
        layout.addWidget(QLabel('Max. Width'), 2, 0)
        layout.addWidget(QLabel('Max. Height'), 3, 0)

        i = 0
        for _, item in self.resampling_form.items():
            layout.addWidget(item, i, 1)
            i += 1

    def update_form(self, data):
        self.frequency_GHz = data['frequency_GHz']
        lambda_0 = 299792458. / (data['frequency_GHz'] * 1e9)

        grid_info = data['grid_info']
        x_min, x_max, x_samples = grid_info['x_range']
        y_min, y_max, y_samples = grid_info['y_range']

        u = linspace(x_min, x_max, x_samples, endpoint=True)
        step_lambda = round((u[1] - u[0]) / lambda_0, 8)
        width_lambda = (x_samples - 1) * step_lambda
        height_lambda = (y_samples - 1) * step_lambda
        self.size_limits = (width_lambda, height_lambda)

        width_lambda = data.get('max_width_lambda', width_lambda)
        height_lambda = data.get('max_height_lambda', height_lambda)
        step_lambda = data.get('sampling_step_lambda', lambda_0)
        kappa = data.get('kappa', 1)

        self.resampling_form['kappa'].setValue(kappa)
        self.resampling_form['sampling_step_lambda'].setValue(step_lambda)
        self.resampling_form['max_width_lambda'].setValue(width_lambda)
        self.resampling_form['max_height_lambda'].setValue(height_lambda)

    def update_data(self, data):
        data['sampling_step_lambda'] = self.resampling_form['sampling_step_lambda'].value()
        data['kappa'] = self.resampling_form['kappa'].value()
        data['max_width_lambda'] = self.resampling_form['max_width_lambda'].value()
        data['max_height_lambda'] = self.resampling_form['max_height_lambda'].value()

        return data


class MainWindow(QMainWindow):

    def __init__(self):
        from qosm.gui.view.sources.NFSourceViewer import NFSourceViewDialog
        super().__init__()
        self.setWindowTitle("Test load NF Dialog")
        self.setGeometry(100, 100, 300, 200)

        dialog = NFSourceCreateDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if data:
                print(f"Fréquence: {data['frequency_GHz']} GHz")
                print(f"Points E-field: {data['e_field'].shape}")
                print(f"Points H-field: {data['h_field'].shape}")
                print(f"Grid info: {data['grid_info']}")
                print(f"sampling: {data['sampling_step_lambda']} λ")

                dialog2 = NFSourceViewDialog(data)

                dialog2.exec()
            else:
                print("Aucune donnée chargée")
        else:
            print("Dialog annulé")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

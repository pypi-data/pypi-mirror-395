from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDoubleSpinBox, QSpinBox,
                               QCheckBox, QPushButton)


class GifExportDialog(QDialog):
    """Dialog for configuring GIF export settings"""

    def __init__(self, default_use_db=False, default_db_min=-50.0, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GIF Export Settings")
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Display mode
        layout.addWidget(QLabel("Display Mode:"))
        self.display_combo = QComboBox()
        self.display_combo.addItem('Magnitude', 'magnitude_all')
        self.display_combo.addItem('Mag X', 'magnitude_x')
        self.display_combo.addItem('Mag Y', 'magnitude_y')
        self.display_combo.addItem('Mag Z', 'magnitude_z')
        self.display_combo.addItem('Phase X', 'phase_x')
        self.display_combo.addItem('Phase Y', 'phase_y')
        self.display_combo.addItem('Phase Z', 'phase_z')
        layout.addWidget(self.display_combo)

        # Animation settings
        layout.addWidget(QLabel("Frame Duration (seconds):"))
        self.duration_spinbox = QDoubleSpinBox()
        self.duration_spinbox.setRange(0.1, 10.0)
        self.duration_spinbox.setValue(0.5)
        self.duration_spinbox.setSingleStep(0.1)
        layout.addWidget(self.duration_spinbox)

        # DPI setting
        layout.addWidget(QLabel("Resolution (DPI):"))
        self.dpi_spinbox = QSpinBox()
        self.dpi_spinbox.setRange(50, 300)
        self.dpi_spinbox.setValue(100)
        layout.addWidget(self.dpi_spinbox)

        # dB settings
        self.db_checkbox = QCheckBox("Use dB scale")
        self.db_checkbox.setChecked(default_use_db)
        layout.addWidget(self.db_checkbox)

        self.db_min_spinbox = QDoubleSpinBox()
        self.db_min_spinbox.setRange(-200, 0)
        self.db_min_spinbox.setValue(default_db_min)
        self.db_min_spinbox.setSuffix(" dB")
        self.db_min_spinbox.setEnabled(default_use_db)
        layout.addWidget(QLabel("dB Minimum:"))
        layout.addWidget(self.db_min_spinbox)

        # Annotations checkbox
        self.annotations_checkbox = QCheckBox("Include HPBW annotations and contours")
        self.annotations_checkbox.setChecked(False)
        self.annotations_checkbox.setToolTip("Show half-power lines, HPBW calculations, and contour lines")
        layout.addWidget(self.annotations_checkbox)

        # Connect signals
        self.db_checkbox.toggled.connect(self.db_min_spinbox.setEnabled)

        # Buttons
        button_layout = QHBoxLayout()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def get_settings(self):
        """Return dialog settings as dictionary"""
        return {
            'display_mode': self.display_combo.currentData(),
            'duration_per_frame': self.duration_spinbox.value(),
            'dpi': self.dpi_spinbox.value(),
            'use_db': self.db_checkbox.isChecked(),
            'db_min': self.db_min_spinbox.value(),
            'show_annotations': self.annotations_checkbox.isChecked()
        }

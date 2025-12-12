from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QPushButton, QScrollArea,
                               QWidget, QFrame, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class PipelineBranchSelector(QDialog):
    def __init__(self, pipeline, parent=None):
        """
        Initialize the Pipeline Branch Selector dialog.

        Args:
            pipeline (SimulationPipeline): The pipeline instance
            parent (QWidget, optional): Parent widget
        """
        super().__init__(parent)
        self.pipeline = pipeline
        self.branch_checkboxes = []
        self.selected_branches = []

        self.setWindowTitle("Select Pipeline Branches")
        self.setMinimumSize(800, 400)

        self.setup_ui()
        self._load_branches()

    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)

        # Title
        title_label = QLabel("Select valid pipeline branches to retain:")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Scroll area for branches
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(scroll_area)

        # Selection buttons
        button_layout = QHBoxLayout()

        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self._select_all)
        button_layout.addWidget(select_all_btn)

        select_none_btn = QPushButton("Select None")
        select_none_btn.clicked.connect(self._select_none)
        button_layout.addWidget(select_none_btn)

        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Dialog buttons
        dialog_buttons = QHBoxLayout()

        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        ok_btn.setDefault(True)
        dialog_buttons.addWidget(ok_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        dialog_buttons.addWidget(cancel_btn)

        layout.addLayout(dialog_buttons)

    def _load_branches(self):
        """Load and display the valid branches."""
        try:
            # Get valid branches with names
            valid_branches = self.pipeline.get_valid_branches(show_id=False)
            valid_branches_id = self.pipeline.get_valid_branches(show_id=True)

            if not valid_branches:
                # No valid branches found
                no_branches_label = QLabel("No valid branches found.")
                no_branches_label.setStyleSheet("color: red; font-style: italic;")
                self.scroll_layout.addWidget(no_branches_label)
                return

            # Create checkboxes for each branch
            for i, branch in enumerate(valid_branches, 1):
                branch_frame = QFrame()
                branch_frame.setLineWidth(1)
                frame_layout = QVBoxLayout(branch_frame)

                # Branch header
                branch_header = QLabel(f"Branch {i}:")
                frame_layout.addWidget(branch_header)

                # Branch path
                branch_path = " → ".join(branch)
                checkbox = QCheckBox(branch_path)
                checkbox.setChecked(True)  # Default to selected

                # Store reference to the branch data
                checkbox.branch_data = valid_branches_id[i-1]

                frame_layout.addWidget(checkbox)
                self.branch_checkboxes.append(checkbox)

                self.scroll_layout.addWidget(branch_frame)

        except Exception as e:
            error_label = QLabel(f"Error loading branches: {str(e)}")
            error_label.setStyleSheet("color: red;")
            self.scroll_layout.addWidget(error_label)

    def _select_all(self):
        """Select all branch checkboxes."""
        for checkbox in self.branch_checkboxes:
            checkbox.setChecked(True)

    def _select_none(self):
        """Deselect all branch checkboxes."""
        for checkbox in self.branch_checkboxes:
            checkbox.setChecked(False)

    def get_selected_branches(self):
        """
        Get the list of selected branches.

        Returns:
            list: List of selected branch paths (list of names)
        """
        selected = []
        for checkbox in self.branch_checkboxes:
            if checkbox.isChecked():
                selected.append(checkbox.branch_data)
        return selected

    def accept(self):
        """Handle OK button click."""
        selected_branches = self.get_selected_branches()

        if not selected_branches:
            # Show warning if no branches are selected
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("No Selection")
            msg.setText("No branches are selected. Are you sure you want to continue?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)

            if msg.exec() == QMessageBox.No:
                return

        self.selected_branches = selected_branches
        super().accept()


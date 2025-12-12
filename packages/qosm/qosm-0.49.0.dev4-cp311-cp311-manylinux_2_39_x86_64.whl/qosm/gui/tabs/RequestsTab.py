import copy

from PySide6.QtCore import Qt, QThread, QTimer
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QVBoxLayout, QWidget, QMessageBox, QPushButton, QDialog, QGroupBox, QListWidget, \
    QApplication, QListWidgetItem, QMenu, QInputDialog, QProgressBar

from qosm.gui.dialogs import NFGridCreateDialog, SetSweepDialog, PipelineBranchSelector, FFRequestCreateDialog, \
    GBTCRequestCreateDialog
from qosm.gui.managers import RequestType, SimulationAborted
from qosm.gui.objects.pipeline import InvalidPipeline

from qosm.gui.workers import SimulationWorker
from qosm.gui.view.RequestViewer import launch_gui_request_viewer
import traceback

from qosm.gui.objects import HDF5Exporter


class RequestsTab(QWidget):
    """Requests tab widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.selection_callback = None
        self.result_viewer = None
        self.results = None
        self.sweep = {
            'target': ('None', None),
            'attribute': 'None',
            'sweep': (0., 0., 1)
        }

        # Link objects
        self.object_manager = parent.object_manager if hasattr(parent, "object_manager") else None
        self.source_manager = parent.source_manager if hasattr(parent, "source_manager") else None
        self.request_manager = parent.request_manager if hasattr(parent, "request_manager") else None
        self.viewer = parent.viewer if hasattr(parent, "viewer") else None
        self.log_message = parent.log_message if hasattr(parent, "log_message") else None

        # Lists
        self.request_group = None
        self.request_list = None

        # Parameters
        self.parameters = None

        # Threading
        self.simulation_thread = None
        self.simulation_worker = None

        # UI Elements for progress
        self.progress_bar = None
        self.cancel_button = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        btn_group = QGroupBox('')
        btn_group.setStyleSheet("QGroupBox { border: none; }")
        btn_group_layout = QVBoxLayout()
        btn_group.setLayout(btn_group_layout)
        layout.addWidget(btn_group)

        sweep_btn = QPushButton("Set sweep")
        sweep_btn.clicked.connect(self.set_sweep)
        sweep_btn.setObjectName("sweep_btn")
        btn_group_layout.addWidget(sweep_btn)

        self.build_btn = QPushButton("Build pipeline and simulate")
        self.build_btn.clicked.connect(self.build)
        self.build_btn.setObjectName("build_btn")
        btn_group_layout.addWidget(self.build_btn)

        # Progress bar (hidden by default) - Modified to show 0-100%
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)  # Progress from 0 to 100%
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        self.cancel_button = QPushButton("Cancel Simulation")
        self.cancel_button.clicked.connect(self.cancel_simulation)
        self.cancel_button.setObjectName("cancel_btn")
        self.cancel_button.hide()
        layout.addWidget(self.cancel_button)

        # Objects list group
        self.create_request_list_group()
        self.request_group.setMinimumHeight(220)

        layout.addWidget(self.request_group)

        self.export_all_btn = QPushButton("Export All Results (HDF5)")
        self.export_all_btn.clicked.connect(self.export_all_results_hdf5)
        self.export_all_btn.setObjectName("export_btn")
        self.export_all_btn.setEnabled(False)  # Disabled until results are available
        layout.addWidget(self.export_all_btn)

        layout.addStretch()

        # Initialize HDF5 exporter
        self.hdf5_exporter = HDF5Exporter(self)

    def connect_parameters(self, parameter_tab):
        self.parameters = parameter_tab
        self.update_lists()

    def set_sweep(self):
        dialog = SetSweepDialog(self, current_configuration=self.sweep)
        if dialog.exec() == QDialog.Accepted:
            res = dialog.get_parameters()
            if res is not None:
                self.sweep = res
                self.log_message('Sweep configuration updated', type='success')
            else:
                self.log_message('Sweep configuration update failed', type='error')

    def build(self):
        self.parent_window.tabs.setCurrentIndex(1)

        num_domains = len(self.object_manager.get_objects_by_type()['Domain'])
        if num_domains == 0:
            self.log_message('At least one GBT domain is required for beam tracing to be activated.', type='warning')

        try:
            if self.result_viewer is not None:
                self.result_viewer.close()

            self.start_simulation_thread()

        except InvalidPipeline as e:
            self.log_message(str(e), type='error')
        except SimulationAborted as e:
            self.log_message(str(e), type='error')

    def start_simulation_thread(self):
        if self.simulation_thread is not None and self.simulation_thread.isRunning():
            self.cancel_simulation()

        self.show_progress_ui()

        # CREATE COPIES of data (not objects)
        source_data = {
            'uuid': copy.deepcopy(self.source_manager.active_source_uuid),
            'source': copy.deepcopy(self.source_manager.get_active_source())
        }

        request_data = copy.deepcopy(self.request_manager.requests)
        object_data = copy.deepcopy(self.object_manager.objects)
        sweep_data = copy.deepcopy(self.sweep)

        # Create workers with COPIES
        self.simulation_thread = QThread()
        self.simulation_worker = SimulationWorker(source_data, request_data, object_data, sweep_data,
                                                  current_file=self.request_manager.current_file)

        self.simulation_worker.moveToThread(self.simulation_thread)

        # Connect signals
        self.simulation_worker.user_confirm.connect(self.select_pipelines)
        self.simulation_thread.started.connect(self.simulation_worker.run)
        self.simulation_worker.finished.connect(self.simulation_thread.quit)
        self.simulation_worker.finished.connect(self.simulation_worker.deleteLater)
        self.simulation_thread.finished.connect(self.simulation_thread.deleteLater)
        self.simulation_thread.finished.connect(self.hide_progress_ui)

        self.simulation_worker.success.connect(self.on_simulation_success)
        self.simulation_worker.error.connect(self.on_simulation_error)
        self.simulation_worker.warning.connect(self.on_simulation_warning)
        self.simulation_worker.results_ready.connect(self.store_results)
        self.simulation_worker.results_ready.connect(self.display_results)
        self.simulation_worker.progress.connect(self.on_simulation_progress)
        self.simulation_worker.progress_bar.connect(self.on_simulation_progress_update)

        self.keep_alive_timer = QTimer()
        self.keep_alive_timer.timeout.connect(lambda: QApplication.processEvents())
        self.keep_alive_timer.start(100)  # Every 100ms
        self.simulation_thread.start()

    def select_pipelines(self, pipeline):
        dialog = PipelineBranchSelector(pipeline, parent=self)
        result = dialog.exec()

        if result == QDialog.Accepted:
            self.simulation_worker.run_branches = dialog.get_selected_branches()
        else:
            self.simulation_worker.run_branches = []

    def show_progress_ui(self):
        """Show progress interface"""
        self.build_btn.setEnabled(False)
        self.progress_bar.setValue(0)  # Reset to 0
        self.progress_bar.show()
        self.cancel_button.show()

    def hide_progress_ui(self):
        """Hide progress interface"""
        self.build_btn.setEnabled(True)
        self.progress_bar.hide()
        self.cancel_button.hide()
        self.simulation_thread = None

    def cancel_simulation(self):
        """Cancel running simulation"""
        if self.simulation_worker:
            self.simulation_worker.stop()
        if self.simulation_thread and self.simulation_thread.isRunning():
            self.simulation_thread.quit()
            self.simulation_thread.wait(3000)  # Wait max 3 seconds
            self.simulation_thread = None
        self.log_message('Simulation cancelled', type='warning')

    def on_simulation_success(self, message):
        """Called when simulation completes successfully"""
        self.log_message(message, type='success')

    def on_simulation_warning(self, message):
        """Called when simulation encounters a warning"""
        self.log_message(message, type='warning')

    def on_simulation_error(self, error_msg, error_type):
        """Called when simulation encounters an error"""
        if error_type == 'SimulationAborted':
            self.log_message(error_msg, type='error')
        else:
            self.log_message(error_msg, type='error')

    def on_simulation_progress_update(self, progress_value):
        """Called to update progress bar (0-100)"""
        self.progress_bar.setValue(progress_value)

    def on_simulation_progress(self, message):
        """Called for progress messages"""
        self.log_message(message, type='log')

    def store_results(self, results):
        self.results = results

        # Enable export all button when results are available
        if hasattr(self, 'export_all_btn'):
            self.export_all_btn.setEnabled(results is not None and len(results) > 0)

    def export_request_hdf5(self, req_uuid):
        """Export a specific request's data to HDF5"""
        if self.results is None or req_uuid not in self.results:
            QMessageBox.warning(self, "Export Error", "No simulation results available for this request.")
            return

        # Get request data
        data_dict = self.results[req_uuid]

        # Generate suggested filename
        req_name = str(data_dict.get('req_name', f'request_{req_uuid}'))
        clean_name = "".join(c for c in req_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        suggested_filename = f"{clean_name}_results.h5"

        # Export the data
        success = self.hdf5_exporter.export_single_request(data_dict, suggested_filename)

        if success:
            self.log_message(f'Request "{req_name}" exported to HDF5 successfully', type='success')
        else:
            self.log_message(f'Failed to export request "{req_name}" to HDF5', type='error')

    def export_all_results_hdf5(self):
        """Export all simulation results to a single HDF5 file"""
        if self.results is None or len(self.results) == 0:
            QMessageBox.warning(self, "Export Error", "No simulation results available to export.")
            return

        # Generate suggested filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        suggested_filename = f"all_simulation_results_{timestamp}.h5"

        # Export all results
        success = self.hdf5_exporter.export_all_results(self.results, suggested_filename)

        if success:
            self.log_message(f'All simulation results exported to HDF5 successfully', type='success')
        else:
            self.log_message('Failed to export simulation results to HDF5', type='error')

    def display_results(self, results = None):
        """Display results (called in main thread)"""
        if results is None:
            results = self.results
        try:
            if self.result_viewer is not None:
                self.result_viewer.close()
            if results is not None and len(results) > 0:
                # Execute launch_gui_request_viewer in main thread
                self.result_viewer = launch_gui_request_viewer(results)
            else:
                self.log_message('No result to show', type='warning')
        except Exception as e:
            traceback.print_exception(e)
            self.log_message(f'Error displaying results: {str(e)}', type='error')

    # ... [Rest of the code unchanged] ...

    def create_request_list_group(self):
        """Create requests list group"""
        self.request_group = QGroupBox("")
        request_layout = QVBoxLayout()
        request_layout.setAlignment(Qt.AlignTop)
        self.request_group.setLayout(request_layout)

        # Create objects list widget
        self.request_list = QListWidget()
        self.request_list.setSpacing(4)
        self.request_list.itemClicked.connect(self.on_request_list_item_clicked)
        self.request_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.request_list.customContextMenuRequested.connect(self.show_object_context_menu)

        request_layout.addWidget(self.request_list)

    def update_request_list(self):
        """Update the request list display"""
        if not self.request_list:
            return

        # Get system palette
        palette = QApplication.palette()
        selection_bg = palette.color(QPalette.Highlight)
        disabled_text_color = palette.color(QPalette.Disabled, QPalette.Text)

        self.request_list.clear()
        requests_by_type = self.request_manager.get_requests_by_type()

        num_objects = 0
        for type_name, requests in requests_by_type.items():
            if requests:
                type_name_value = getattr(RequestType, type_name).value + ('s' if len(requests) > 1 else '')
                num_objects += 1
                header_item = QListWidgetItem(f"◺ {type_name_value} ({len(requests)})")
                header_item.setFlags(header_item.flags() & ~Qt.ItemIsSelectable)
                header_item.setBackground(QColor(80, 80, 80))
                header_item.setForeground(QColor(200, 200, 200))
                header_item.setData(Qt.UserRole, None)
                self.request_list.addItem(header_item)

                for req_uuid, obj in requests:
                    display_name = self.request_manager.get_request_display_name(req_uuid)
                    item_text = f"     {display_name}"
                    item = QListWidgetItem(item_text)
                    if not obj['enabled']:
                        item.setForeground(disabled_text_color)
                    item.setData(Qt.UserRole, req_uuid)

                    self.request_list.addItem(item)
                    if req_uuid == self.request_manager.active_request_uuid:
                        item.setBackground(selection_bg)

        if num_objects == 0:
            item = QListWidgetItem("No request created")
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            item.setForeground(QColor(128, 128, 128))
            self.request_list.addItem(item)

    def on_request_list_item_clicked(self, item):
        """Handle click on object list item"""
        req_uuid = item.data(Qt.UserRole)
        if req_uuid is None:
            return

        self.request_manager.set_active_request(req_uuid)
        self.selection_callback(req_uuid)

        self.log_message(f"Request selected: {self.request_manager.get_request_display_name(req_uuid)}")

    def show_object_context_menu(self, position):
        item = self.request_list.itemAt(position)
        if item is None:
            return
        req_uuid = item.data(Qt.UserRole)
        if req_uuid is None:
            return

        context_menu = QMenu(self)
        rename_action = context_menu.addAction("Enable / Disable")
        rename_action.triggered.connect(lambda: self.toogle_request_enable_disable(req_uuid))
        context_menu.addSeparator()
        rename_action = context_menu.addAction("Rename")
        rename_action.triggered.connect(lambda: self.rename_request(req_uuid))
        delete_action = context_menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_request(req_uuid))

        context_menu.addSeparator()
        export_hdf5_action = context_menu.addAction("Export to HDF5")
        export_hdf5_action.triggered.connect(lambda: self.export_request_hdf5(req_uuid))

        # Enable export only if results are available
        export_hdf5_action.setEnabled(self.results is not None and req_uuid in self.results)

        context_menu.exec(self.request_list.mapToGlobal(position))

    def toogle_request_enable_disable(self, req_uuid):
        if self.request_manager.toggle_enable_disable(req_uuid):
            self.update_lists()
            self.viewer.update()

    def rename_request(self, req_uuid=None):
        """Rename an object"""
        if not req_uuid:
            req_uuid = self.request_manager.active_request_uuid

        current_name = self.request_manager.get_request_display_name(req_uuid)
        new_name, ok = QInputDialog.getText(self, "Rename request", "New name:", text=current_name)
        if ok:
            if self.request_manager.set_request_name(new_name, req_uuid):
                self.log_message(f"Request renamed: '{current_name}' → '{new_name}'", type='success')
                self.update_request_list()
            else:
                self.log_message(f"Unable to rename the request: '{current_name}' to '{new_name}'", type='error')

    def delete_request(self, req_uuid=None):
        if not req_uuid:
            req_uuid = self.request_manager.active_request_uuid

        if not self.request_manager.exists(req_uuid):
            return

        display_name = self.request_manager.get_request_display_name(req_uuid)

        reply = QMessageBox.question(
            self, "Delete Object",
            f"Are you sure you want to delete this object?\n\nName: {display_name}\n",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Clean up reference tracking
            if self.request_manager.remove_request(req_uuid):
                # Remove reference in linked objects
                self.selection_callback(self.request_manager.active_request_uuid)
                # Log removal
                self.log_message(f"Request removed: {display_name}", type='success')
            else:
                self.log_message(f"Failed to delete: {display_name}")

    def create_near_field_request(self):
        dialog = NFGridCreateDialog(self)
        if dialog.exec() == QDialog.Accepted:
            if self.request_manager.add_request(RequestType.NEAR_FIELD, dialog.get_parameters()):
                self.selection_callback(self.request_manager.active_request_uuid)
                self.log_message('Near Field request added', type='success')
            else:
                self.log_message('Near Field request could not be added', type='error')

    def create_far_field_request(self):
        dialog = FFRequestCreateDialog(self)
        if dialog.exec() == QDialog.Accepted:
            if self.request_manager.add_request(RequestType.FAR_FIELD, dialog.get_parameters()):
                self.selection_callback(self.request_manager.active_request_uuid)
                self.log_message('Far Field request added', type='success')
            else:
                self.log_message('Far Field request could not be added', type='error')

    def create_gbtc_request(self):
        dialog = GBTCRequestCreateDialog(self)
        if dialog.exec() == QDialog.Accepted:
            if self.request_manager.add_request(RequestType.GBTC, dialog.get_parameters()):
                self.selection_callback(self.request_manager.active_request_uuid)
                self.log_message('GBTC request added', type='success')
            else:
                self.log_message('GBTC request could not be added', type='error')

    def update_lists(self, update_params = True):
        self.update_request_list()
        if update_params:
            self.parameters.display_parameters(tab='requests')

    def apply_request_update(self):
        req = self.request_manager.get_active_request()
        req_name = req['name']
        params = self.parameters.sections[req['type']].get_parameters()

        if self.request_manager.update_active_request(params):
            self.selection_callback(self.request_manager.active_request_uuid)
            self.log_message(f"Request '{req_name}' updated", type='success')
        else:
            self.log_message(f"Unable to update the request '{req_name}'", type='error')


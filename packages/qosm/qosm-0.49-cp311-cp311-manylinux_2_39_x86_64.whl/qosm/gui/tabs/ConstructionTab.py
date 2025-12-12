import os

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QGroupBox, QListWidget, QDialog, QMessageBox, QListWidgetItem,
                               QApplication, QMenu, QInputDialog, QSplitter)
from PySide6.QtCore import Qt

from qosm.gui.dialogs import (GBEGridCreateDialog, StepLoadDialog, ShapeCreateDialog,
                              NFSourceCreateDialog, NFSourceEditDialog, DomainCreateDialog, GaussianBeamCreateDialog,
                              HornCreateDialog, GBTCPortCreateDialog, MultiLayerSampleCreateDialog, BiconvexLensCreateDialog)
from qosm.gui.view import NFSourceViewDialog


class ConstructionTab(QWidget):
    """Construction tab widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.selection_callback = None

        # link objects
        self.object_manager = parent.object_manager if hasattr(parent, "object_manager") else None
        self.source_manager = parent.source_manager if hasattr(parent, "source_manager") else None
        self.viewer  = parent.viewer if hasattr(parent, "viewer") else None
        self.log_message = parent.log_message if hasattr(parent, "log_message") else None

        # Object and source lists
        self.object_list = None
        self.sources_list = None

        # Sections
        self.parameters = None
        self.objects_section = None
        self.sources_section = None

        # Modifications controls
        self.step_form = None
        self.shape_form = None

        # Grid modification controls
        self.grid_form = {}
        self.grid_u = None
        self.grid_v = None
        self.grid_sampling_step = None
        self.grid_kappa = None
        self.grid_center_x = None
        self.grid_center_y = None
        self.grid_center_z = None
        self.reference_combo = None
        self.grid_source_combo_box = None

        # Domain modification controls
        self.max_reflections = None
        self.max_refractions = None
        self.power_threshold = None
        self.domain_source_combo_box = None
        self.meshes_layout = None

        self.setup_ui()

    def connect_parameters(self, parameter_tab):
        self.parameters = parameter_tab

        # Hide both groups initially
        self.update_display_for_selection()

    def setup_ui(self):
        """Setup construction tab UI"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        # objects list group
        self.create_object_list_group()

        # Sources group
        self.create_source_list_group()

        # Add to splitter
        splitter = QSplitter(Qt.Vertical)
        splitter.setStyleSheet("font-size: 0.9em;")
        splitter.addWidget(self.sources_section)
        splitter.addWidget(self.objects_section)
        splitter.setSizes([200, 800])
        layout.addWidget(splitter)

    def create_object_list_group(self):
        """Create objects list group"""
        self.objects_section = QGroupBox("Objects")
        objects_layout = QVBoxLayout()
        objects_layout.setAlignment(Qt.AlignTop)
        self.objects_section.setLayout(objects_layout)

        # Create objects list widget
        self.object_list = QListWidget()
        self.object_list.setSpacing(4)
        self.object_list.itemClicked.connect(self.on_object_list_item_clicked)
        self.object_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.object_list.customContextMenuRequested.connect(self.show_object_context_menu)

        objects_layout.addWidget(self.object_list)

    def create_source_list_group(self):
        """Create sources list group"""
        self.sources_section = QGroupBox("Main sources")
        sources_layout = QVBoxLayout()
        sources_layout.setAlignment(Qt.AlignTop)
        self.sources_section.setLayout(sources_layout)

        # Create sources list widget
        self.sources_list = QListWidget()
        self.sources_list.setSpacing(4)
        self.sources_list.itemClicked.connect(self.on_source_list_item_clicked)
        self.sources_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sources_list.customContextMenuRequested.connect(self.show_source_context_menu)

        sources_layout.addWidget(self.sources_list)

    def get_object_display_name(self, object_uuid):
        """Return display name for an object by UUID (override for custom names)"""
        return self.object_manager.get_object_display_name(object_uuid)

    def on_object_list_item_clicked(self, item):
        """Handle click on object list item"""
        object_uuid = item.data(Qt.UserRole)
        if object_uuid is None:
            return

        self.object_manager.set_active_object(object_uuid)
        self.selection_callback(object_uuid)

        self.log_message(f"Object selected: {self.object_manager.get_object_display_name()}")

    def on_source_list_item_clicked(self, item):
        """Handle click on source list item"""
        src_uuid = item.data(Qt.UserRole)
        if src_uuid is not None:
            self.source_manager.set_active_source(src_uuid)
            self.update_lists()
            source_name = self.source_manager.sources[src_uuid]['name']
            self.log_message(f"Active source: {source_name}")
            if self.viewer:
                self.viewer.update()

    def show_object_context_menu(self, position):
        """Show context menu for object list"""
        item = self.object_list.itemAt(position)
        if item is None:
            return
        object_uuid = item.data(Qt.UserRole)
        if object_uuid is None:
            return

        context_menu = QMenu(self)
        rename_action = context_menu.addAction("Rename")
        rename_action.triggered.connect(lambda: self.rename_object(object_uuid))
        context_menu.addSeparator()
        delete_action = context_menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_object(object_uuid))

        context_menu.exec(self.object_list.mapToGlobal(position))

    def show_source_context_menu(self, position):
        """Show context menu for source list"""
        item = self.sources_list.itemAt(position)
        if item is None:
            return
        source_index = item.data(Qt.UserRole)
        if source_index is None:
            return

        context_menu = QMenu(self)

        set_active_action = context_menu.addAction("Clic on list to set as Active")
        set_active_action.setDisabled(True)

        context_menu.addSeparator()

        rename_action = context_menu.addAction("Rename")
        rename_action.triggered.connect(lambda: self.rename_source(source_index))

        delete_action = context_menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_source(source_index))

        source = self.source_manager.sources[source_index]
        if source and source['type'] in ('GaussianBeam', 'NearFieldSource', 'Horn'):
            edit_action = context_menu.addAction("Edit")
            edit_action.triggered.connect(lambda: self.edit_source(source, source_index))
        if source and source['type'] == 'NearFieldSource':
            view_action = context_menu.addAction("View fields")
            view_action.triggered.connect(lambda: self.view_source(source))

        context_menu.exec(self.sources_list.mapToGlobal(position))

    def rename_object(self, object_uuid=None):
        """Rename an object"""
        if not self.object_manager.exists(object_uuid):
            return

        current_name = self.object_manager.get_object_display_name(object_uuid)
        new_name, ok = QInputDialog.getText(self, "Rename object", "New name :", text=current_name)
        if ok:
            self.object_manager.set_object_name(new_name, object_uuid)
            new_name = self.object_manager.get_object_display_name(object_uuid)
            self.log_message(f"Object renamed: '{current_name}' → '{new_name}'", type='success')
            self.update_objects_list()
            self.update_display_for_selection()

    def rename_source(self, src_uuid):
        """Rename a source"""
        if not self.source_manager.exists(src_uuid):
            return

        try:
            current_name = self.source_manager.sources[src_uuid].name
        except AttributeError:
            try:
                current_name = self.source_manager.sources[src_uuid]['name']
            except KeyError:
                self.log_message("Unable to retrieve the source name", type='error')

        new_name, ok = QInputDialog.getText(self, "Rename Source", "New name:", text=current_name)
        if ok and new_name.strip():
            self.source_manager.sources[src_uuid]['name'] = new_name.strip()
            self.update_sources_list()
            self.log_message(f"Source renamed: '{current_name}' → '{new_name.strip()}'", type='success')

    def delete_object(self, object_uuid=None):
        """Delete an object with confirmation"""
        if not self.object_manager.exists(object_uuid):
            return

        display_name = self.object_manager.get_object_display_name(object_uuid)

        reply = QMessageBox.question(
            self, "Delete Object",
            f"Are you sure you want to delete this object?\n\nName: {display_name}\n",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Clean up reference tracking
            if self.object_manager.remove_object(object_uuid):
                # remove reference in linked objects
                for _, _obj in self.object_manager.objects.items():
                    src_uuid = _obj.get('parameters', {}).get('source', None)
                    if src_uuid is not None and src_uuid == object_uuid:
                        _obj['parameters']['source'] = None
                self.selection_callback(self.object_manager.active_object_uuid)
                # Log removal
                self.log_message(f"Object removed: {display_name}", type='success')
            else:
                self.log_message(f"Failed to delete: {display_name}")
                QMessageBox.critical(self, "Error", f"Failed to delete: {display_name}", type='error')

    def edit_source(self, src, src_uuid):
        """Edit a source"""
        if src:
            source_name = src['name']
            data = src['parameters']
            data['source_name'] = source_name
            if src['type'] == 'GaussianBeam':
                dialog = GaussianBeamCreateDialog(self, data)
            elif src['type'] == 'NearFieldSource':
                dialog = NFSourceEditDialog(self, data, name=src['name'])
            elif src['type'] == 'Horn':
                dialog = HornCreateDialog(self, data, name=src['name'])
            else:
                return

            if dialog.exec() == QDialog.Accepted:
                if src['type'] in ('GaussianBeam', 'Horn'):
                    data = dialog.get_data()
                else:
                    data = dialog.update_data(data)
                self.source_manager.edit_source(src_uuid, data)
                self.update_lists()

    @staticmethod
    def view_source(src):
        """Edit a source"""
        if src:
            source_name = src['name']
            data = src['parameters']
            if src['type'] == 'NearFieldSource':
                dialog = NFSourceViewDialog(data)
            else:
                return

            dialog.exec()

    def delete_source(self, src_uuid):
        """Delete a source with confirmation"""
        if not self.source_manager.exists(src_uuid):
            return

        source_name = self.source_manager.sources[src_uuid]['name']
        reply = QMessageBox.question(
            self, "Delete Source",
            f"Are you sure you want to delete the source '{source_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.source_manager.remove_source(src_uuid):
                # remove reference in linked objects
                for _, _obj in self.object_manager.objects.items():
                    obj_src_uuid = _obj.get('parameters', {}).get('source', None)
                    if src_uuid is not None and obj_src_uuid == src_uuid:
                        _obj['parameters']['source'] = None
                self.update_lists()
                self.log_message(f"Source deleted: {source_name}", type='success')
            else:
                self.log_message(f"Source deletion failed ({source_name})", type='error')
                QMessageBox.critical(self, "Error", f"Failed to delete source: {source_name}")

    def update_lists(self, update_params = True):
        """Update all lists"""
        self.update_objects_list()
        self.update_sources_list()
        if update_params:
            self.update_display_for_selection()

    def update_objects_list(self):
        """Update the objects list display"""
        if not self.object_list:
            return

        # Get system palette
        palette = QApplication.palette()
        selection_bg = palette.color(QPalette.Highlight)

        self.object_list.clear()
        objects_by_type = self.object_manager.get_objects_by_type()

        num_objects = 0
        for type_name, objects in objects_by_type.items():
            if objects:
                num_objects += 1
                header_item = QListWidgetItem(f"◺ {type_name} ({len(objects)})")
                header_item.setFlags(header_item.flags() & ~Qt.ItemIsSelectable)
                header_item.setBackground(QColor(80, 80, 80))
                header_item.setForeground(QColor(200, 200, 200))
                header_item.setData(Qt.UserRole, None)
                self.object_list.addItem(header_item)

                for object_uuid, obj in objects:
                    display_name = self.object_manager.get_object_display_name(object_uuid)
                    item_text = f"     {display_name}"
                    item = QListWidgetItem(item_text)
                    item.setData(Qt.UserRole, object_uuid)

                    self.object_list.addItem(item)
                    if object_uuid == self.object_manager.active_object_uuid:
                        item.setBackground(selection_bg)

        if num_objects == 0:
            item = QListWidgetItem("No object loaded")
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            item.setForeground(QColor(128, 128, 128))
            self.object_list.addItem(item)

    def update_sources_list(self):
        """Update the sources list in the interface"""
        if not self.sources_list:
            return

        self.sources_list.clear()

        if not self.source_manager.sources:
            item = QListWidgetItem("No sources loaded")
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            item.setForeground(QColor(128, 128, 128))
            self.sources_list.addItem(item)
            return

        for src_uuid, source in self.source_manager.get_sources():
            item_text = f"{source['name']}"
            if src_uuid == self.source_manager.active_source_uuid:
                item_text += " (Active)"

            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, src_uuid)

            if src_uuid == self.source_manager.active_source_uuid:
                item.setBackground(QColor(34, 100, 34))
                item.setForeground(QColor(255, 255, 255))
            else:
                item.setBackground(QColor(0, 0, 0, 0))
                item.setForeground(QColor(255, 255, 255))

            self.sources_list.addItem(item)

    def update_display_for_selection(self):
        self.parameters.display_parameters(tab='construction')

    def import_step_file(self):
        """Open STEP file loading dialog"""
        dialog = StepLoadDialog(self)
        if dialog.exec() == QDialog.Accepted:
            step_params = dialog.get_parameters()
            if step_params is not None:
                file_path = step_params['filepath']
                mesh_uuid = self.object_manager.create_step(step_params)

                if mesh_uuid is not None:
                    self.object_manager.set_active_object(mesh_uuid)
                    self.selection_callback(mesh_uuid)
                    filename_only = os.path.basename(file_path)
                    self.log_message(f"File loaded: {filename_only}", type='success')
                else:
                    self.log_message(f"Loading failed: {file_path}", type='error')
            else:
                self.log_message(f"Unable to import a step with the selected parameters", type='error')

    def create_shape(self):
        """Create a shape"""
        dialog = ShapeCreateDialog(self)
        if dialog.exec() == QDialog.Accepted:
            shape_params = dialog.get_parameters()
            if shape_params is not None:
                mesh_uuid = self.object_manager.create_shape(shape_params)

                if mesh_uuid is not None:
                    self.object_manager.set_active_object(mesh_uuid)
                    self.selection_callback(mesh_uuid)
                    self.log_message(f"Shape created", type='success')
                else:
                    self.log_message(f"Failed to create the Shape", type='error')
            else:
                self.log_message(f"Unable to create a shape with the selected parameters", type='error')

    def create_lens(self):
        """Create a shape"""
        dialog = BiconvexLensCreateDialog(self)
        if dialog.exec() == QDialog.Accepted:
            shape_params = dialog.get_data()
            if shape_params is not None:
                mesh_uuid = self.object_manager.create_lens(shape_params)

                if mesh_uuid is not None:
                    self.object_manager.set_active_object(mesh_uuid)
                    self.selection_callback(mesh_uuid)
                    self.log_message(f"Lens created", type='success')
                else:
                    self.log_message(f"Failed to create the Lens", type='error')
            else:
                self.log_message(f"Unable to create a Lens with the selected parameters", type='error')

    def create_gbe_grid(self):
        """Open grid creation dialog"""
        dialog = GBEGridCreateDialog(managers=(self.object_manager, self.source_manager), parent=self)
        if dialog.exec() == QDialog.Accepted:
            grid_params = dialog.get_parameters()
            if grid_params:
                grid_uuid = self.object_manager.create_gbe_grid(grid_params)
                if grid_uuid is not None:
                    self.object_manager.set_active_object(grid_uuid)
                    self.selection_callback(grid_uuid)
                    self.log_message("GBE grid created successfully", type='success')
                else:
                    self.log_message("GBE grid creation failed", type='error')
                    QMessageBox.critical(self, "Error", "Unable to create GBE grid")
            else:
                QMessageBox.critical(self, "Error", "Invalid GBE grid parameters")

    def create_gaussian_beam_source(self):
        """Create a Gaussian Beam"""
        dialog = GaussianBeamCreateDialog(self)
        if dialog.exec() == QDialog.Accepted:
            gb_data = dialog.get_data()
            source_name = gb_data['source_name']
            success = self.source_manager.add_source('GaussianBeam', source_name, gb_data)
            if success:
                self.log_message(f"Gaussian Beam source '{source_name}' added successfully", type='success')
                self.update_lists()
                self.update()
            else:
                QMessageBox.critical(self, "Error", "Failed to add the Gaussian Beam source to manager")

    def create_horn_source(self):
        dialog = HornCreateDialog(self)
        if dialog.exec() == QDialog.Accepted:
            horn_data = dialog.get_data()
            source_name = horn_data['source_name']
            success = self.source_manager.add_source('Horn', source_name, horn_data)
            if success:
                self.log_message(f"Horn source '{source_name}' added successfully", type='success')
                self.update_lists()
                self.update()
            else:
                QMessageBox.critical(self, "Error", "Failed to add the Horn source to manager")

    def create_nf_source(self):
        """Create a near field source"""
        dialog = NFSourceCreateDialog(self)

        if dialog.exec() == QDialog.Accepted:
            src_data = dialog.get_data()
            source_name = src_data['metadata']['source_name']

            success = self.source_manager.add_source('NearFieldSource', source_name, src_data)
            if success:
                self.log_message(f"Near Field source '{source_name}' added successfully", type='success')
                self.update_lists()
                self.update()
                self.viewer.update()

                # Show source information
                frequency = src_data['frequency_GHz']
                bounds = src_data['grid_info']
                self.log_message(f"  frequency: {frequency} GHz")
                self.log_message(f"  Grid bounds: X[{bounds['x_range'][0]:.3f}, {bounds['x_range'][1]:.3f}]")
                self.log_message(f"               Y[{bounds['y_range'][0]:.3f}, {bounds['y_range'][1]:.3f}]")
                self.log_message(f"               Z[{bounds['z_range'][0]:.3f}, {bounds['z_range'][1]:.3f}]")
            else:
                QMessageBox.critical(self, "Error", "Failed to add Near Field source to manager")

    def create_domain(self):
        dialog = DomainCreateDialog(managers=(self.object_manager, self.source_manager), parent=self)
        if dialog.exec() == QDialog.Accepted:
            domain_params = dialog.get_data()
            if domain_params:
                domain_uuid = self.object_manager.create_gbt_domain(domain_params)
                if domain_uuid is not None:
                    self.object_manager.set_active_object(domain_uuid)
                    self.selection_callback(domain_uuid)

                    mesh_list = self.object_manager.get_domain_mesh_names(domain_uuid)
                    self.log_message("GBT domain created successfully", type='success')
                    self.log_message(f"   Included mesh{'es' if len(mesh_list) > 1 else ''}: {mesh_list}")
                else:
                    self.log_message("GBT domain creation failed", type='error')
                    QMessageBox.critical(self, "Error", "Unable to create GBT domain")
            else:
                QMessageBox.critical(self, "Error", "Invalid GBT domain parameters")

    def create_gbtc_port(self):
        """Create a GBTC Port (GOLA)"""
        dialog = GBTCPortCreateDialog(managers=(self.object_manager, self.source_manager), parent=self)
        if dialog.exec() == QDialog.Accepted:

            params = dialog.get_data()
            if params is not None:
                item_uuid = self.object_manager.create_gbtc_port(params)

                if item_uuid is not None:
                    self.object_manager.set_active_object(item_uuid)
                    self.selection_callback(item_uuid)
                    self.log_message(f"GBTC Port created", type='success')
                else:
                    self.log_message(f"Failed to create the GBTC Port", type='error')
            else:
                self.log_message(f"Unable to create a GBTC Port with the selected parameters", type='error')

    def create_gbtc_mlsample(self):
        """Create a GBTC multi-layer sample"""
        samples = self.object_manager.get_objects_by_type()['GBTCSample']
        if len(samples) > 0:
            self.log_message(f"Only one GBTC Sample is allowed", type='error')
            return
        dialog = MultiLayerSampleCreateDialog(managers=(self.object_manager, self.source_manager), parent=self)
        if dialog.exec() == QDialog.Accepted:

            params = dialog.get_data()
            if params is not None:
                item_uuid = self.object_manager.create_gbtc_mlsample(params)

                if item_uuid is not None:
                    self.object_manager.set_active_object(item_uuid)
                    self.selection_callback(item_uuid)
                    self.log_message(f"GBTC Sample created", type='success')
                else:
                    self.log_message(f"Failed to create the GBTC Sample", type='error')
            else:
                self.log_message(f"Unable to create a GBTC Sample with the selected parameters", type='error')

    def apply_step_update(self):
        obj = self.object_manager.get_active_object()
        if obj is None:
            return

        try:
            object_name = obj['name']
            params = self.parameters.sections[obj['type']].get_parameters()
            self.object_manager.update_step(params)
            self.viewer.update()
            self.log_message(f"StepMesh {object_name} updated")
        except AttributeError as e:
            error_msg = f"Error: {e}"
            self.log_message(error_msg, type='error')
        except Exception as e:
            self.log_message(f"Step Mesh {obj['name']} update failed: {e}", type='error')

    def apply_shape_update(self):
        obj = self.object_manager.get_active_object()
        if obj is None:
            return

        try:
            object_name = obj['name']
            params = self.parameters.sections[obj['type']].get_parameters()
            self.object_manager.create_shape(params, update_selected=True)
            self.viewer.update()
            self.log_message(f"ShapeMesh {object_name} updated")
        except AttributeError as e:
            error_msg = f"Error: {e}"
            self.log_message(error_msg, type='error')
        except Exception as e:
            self.log_message(f"Shape Mesh {obj['name']} update failed: {e}", type='error')

    def apply_lens_update(self):
        obj = self.object_manager.get_active_object()
        if obj is None:
            return

        try:
            object_name = obj['name']
            self.parameters.sections[obj['type']].update_parameters(obj)
            self.viewer.update()
            self.log_message(f"Lens Mesh {object_name} updated")
        except AttributeError as e:
            error_msg = f"Error: {e}"
            self.log_message(error_msg, type='error')
        except Exception as e:
            self.log_message(f"Lens Mesh {obj['name']} update failed: {e}", type='error')

    def apply_domain_update(self):
        obj = self.object_manager.get_active_object()
        if obj is None:
            return

        try:
            params = self.parameters.sections[obj['type']].get_parameters()
            self.object_manager.update_gbt_domain(params)
            self.viewer.update()
            self.update_objects_list()
            self.log_message(f"Domain {obj['name']} updated", type='success')
        except AttributeError as e:
            error_msg = f"Error: {e}"
            self.log_message(error_msg, type='error')
        except Exception as e:
            self.log_message(f"Domain {obj['name']} update failed: {e}", type='error')

    def apply_grid_update(self):
        obj = self.object_manager.get_active_object()
        if obj is None:
            return

        try:
            self.parameters.sections[obj['type']].update_parameters(obj)
            self.viewer.update()
            self.log_message(f"Grid {obj['name']} updated", type='success')

        except ValueError:
            error_msg = "Error: Please enter valid numeric values"
            self.log_message(error_msg, type='error')
        except Exception as e:
            self.log_message(f"Grid {obj['name']} update failed: {e}", type='error')

    def apply_gbtc_update(self):
        obj = self.object_manager.get_active_object()
        if obj is None:
            return

        try:
            self.parameters.sections[obj['type']].update_parameters(obj)
            self.viewer.update()
            self.log_message(f"GBTC Port {obj['name']} updated", type='success')
        except Exception as e:
            self.log_message(f"GBTC Port {obj['name']} update failed: {e}", type='error')

    def apply_gbtc_mlsample_update(self):
        obj = self.object_manager.get_active_object()
        if obj is None:
            return

        try:
            self.parameters.sections[obj['type']].update_parameters(obj)
            self.viewer.update()
            self.log_message(f"GBTC Sample {obj['name']} updated", type='success')
        except Exception as e:
            self.log_message(f"GBTC Sample {obj['name']} update failed: {e}", type='error')


from inspect import signature

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QFormLayout, QCheckBox

from qosm.gui.dialogs import GBTCPortEdit
from qosm.gui.managers import RequestType

from qosm.gui.dialogs import StepMeshEdit, ShapeMeshEdit, GBEGridEdit, DomainEdit, NFGridEdit, FFRequestEdit, \
    GBTCRequestEdit, MultiLayerSampleEdit, BiconvexLensEdit


class ParametersTab(QWidget):
    """Parameters tab widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setStyleSheet('ParametersTab { padding: 0 };')

        # link objects
        self.object_manager = parent.object_manager if hasattr(parent, "object_manager") else None
        self.source_manager = parent.source_manager if hasattr(parent, "source_manager") else None
        self.request_manager = parent.request_manager if hasattr(parent, "request_manager") else None
        self.viewer = parent.viewer if hasattr(parent, "viewer") else None

        # link tabs
        self.construction_tab = parent.tabs.construction_tab if hasattr(parent, "tabs") else None
        self.requests_tab = parent.tabs.requests_tab if hasattr(parent, "tabs") else None

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setMaximumWidth(430)

        self.display_3dview_settings(layout)

        self.sections = {
            'None': QLabel('Nothing selected'),
            'StepMesh': StepMeshEdit(self.construction_tab.apply_step_update),
            'ShapeMesh': ShapeMeshEdit(self.construction_tab.apply_shape_update),
            'LensMesh': BiconvexLensEdit(self.construction_tab.apply_lens_update),
            'GBE': GBEGridEdit(self.construction_tab.apply_grid_update),
            'Domain': DomainEdit(self.construction_tab.apply_domain_update),
            'GBTCPort': GBTCPortEdit(self.construction_tab.apply_gbtc_update),
            'GBTCSample': MultiLayerSampleEdit(self.construction_tab.apply_gbtc_mlsample_update),
            RequestType.NEAR_FIELD.name: NFGridEdit(self.requests_tab.apply_request_update),
            RequestType.FAR_FIELD.name: FFRequestEdit(self.requests_tab.apply_request_update),
            RequestType.GBTC.name: GBTCRequestEdit(self.requests_tab.apply_request_update),
        }

        layout.addWidget(QLabel('\n\nParameters\n'))
        for sec_type, section in self.sections.items():
            layout.addWidget(section)
            section.setVisible(False)

        layout.addStretch()

    def display_3dview_settings(self, layout):

        view_group = QGroupBox('3D View')
        view_group_layout = QVBoxLayout()
        view_group.setLayout(view_group_layout)

        show_normals = QCheckBox('Show object normals (when possible)')

        def change_normal_settings():
            self.viewer.show_normals = show_normals.isChecked()
            self.viewer.update()

        show_normals.checkStateChanged.connect(change_normal_settings)
        view_group_layout.addWidget(show_normals)

        layout.addWidget(view_group)


    def display_parameters(self, tab=None):
        if tab == 'construction':
            item = self.object_manager.get_active_object()
        elif tab == 'requests':
            item = self.request_manager.get_active_request()
        else:
            for _, section in self.sections.items():
                section.setVisible(False)

            item = self.object_manager.get_active_object()
            if not item:
                item = self.request_manager.get_active_request()

        if item is None:
            self.sections['None'].setVisible(True)
            return

        item_type = item['type']
        if item_type in self.sections.keys():
            self.sections[item_type].setVisible(True)

            sig = signature(self.sections[item_type].fill)
            if len(sig.parameters) == 1:
                self.sections[item_type].fill(item['parameters'])
            elif len(sig.parameters) == 2:
                managers = (self.object_manager, self.source_manager)
                self.sections[item_type].fill(item['parameters'], managers)
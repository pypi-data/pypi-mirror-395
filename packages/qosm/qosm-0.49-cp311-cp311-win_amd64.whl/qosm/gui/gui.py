import pickle

import sys
from pathlib import Path
from datetime import datetime

from PySide6.QtCore import QLocale
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QTabWidget, QTextEdit,
                               QMessageBox, QFileDialog, QLabel, QWidgetAction)

from qosm.gui.tabs import ConstructionTab, RequestsTab, ParametersTab
from qosm.gui.view import GLViewer
from qosm.gui.managers import ObjectManager, RequestManager, SourceManager

from matplotlib import rcParams
from matplotlib import pyplot as plt


def create_arrow_icons():
    """Crée les icônes de flèches SVG"""
    temp_dir = Path.home() / '.temp_icons'
    temp_dir.mkdir(exist_ok=True)

    # Flèche haut sombre
    up_dark = temp_dir / 'arrow_up_dark.svg'
    up_dark.write_text('''<svg width="10" height="6" viewBox="0 0 10 6" xmlns="http://www.w3.org/2000/svg">
        <path d="M5 0L10 6H0L5 0Z" fill="#e0e0e0"/>
    </svg>''')

    # Flèche bas sombre
    down_dark = temp_dir / 'arrow_down_dark.svg'
    down_dark.write_text('''<svg width="10" height="6" viewBox="0 0 10 6" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 0H10L5 6L0 0Z" fill="#e0e0e0"/>
    </svg>''')

    # Flèche haut clair
    up_light = temp_dir / 'arrow_up_light.svg'
    up_light.write_text('''<svg width="10" height="6" viewBox="0 0 10 6" xmlns="http://www.w3.org/2000/svg">
        <path d="M5 0L10 6H0L5 0Z" fill="#2b2b2b"/>
    </svg>''')

    # Flèche bas clair
    down_light = temp_dir / 'arrow_down_light.svg'
    down_light.write_text('''<svg width="10" height="6" viewBox="0 0 10 6" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 0H10L5 6L0 0Z" fill="#2b2b2b"/>
    </svg>''')

    return temp_dir


def apply_dark_mode_to_plots():
    """Configure Matplotlib pour le mode sombre"""
    plt.style.use('dark_background')

    # Configuration complète des couleurs
    rcParams['figure.facecolor'] = '#2b2b2b'
    rcParams['axes.facecolor'] = '#1e1e1e'
    rcParams['axes.edgecolor'] = '#555555'
    rcParams['axes.labelcolor'] = '#e0e0e0'
    rcParams['text.color'] = '#e0e0e0'
    rcParams['xtick.color'] = '#e0e0e0'
    rcParams['ytick.color'] = '#e0e0e0'
    rcParams['grid.color'] = '#3d3d3d'
    rcParams['legend.facecolor'] = '#2b2b2b'
    rcParams['legend.edgecolor'] = '#555555'
    rcParams['legend.framealpha'] = 0.9

    # Couleurs des lignes (palette claire pour contraster)
    rcParams['axes.prop_cycle'] = plt.cycler('color',
                                             ['#4a9eff', '#ff6b6b', '#51cf66', '#ffd93d', '#a78bfa', '#ff8787',
                                              '#69db7c', '#ffa94d'])


def apply_light_mode_to_plots():
    """Configure Matplotlib pour le mode clair"""
    plt.style.use('default')

    # Configuration complète des couleurs
    rcParams['figure.facecolor'] = '#ffffff'
    rcParams['axes.facecolor'] = '#ffffff'
    rcParams['axes.edgecolor'] = '#2b2b2b'
    rcParams['axes.labelcolor'] = '#2b2b2b'
    rcParams['text.color'] = '#2b2b2b'
    rcParams['xtick.color'] = '#2b2b2b'
    rcParams['ytick.color'] = '#2b2b2b'
    rcParams['grid.color'] = '#d0d0d0'
    rcParams['legend.facecolor'] = '#ffffff'
    rcParams['legend.edgecolor'] = '#c0c0c0'
    rcParams['legend.framealpha'] = 0.9

    # Couleurs des lignes
    rcParams['axes.prop_cycle'] = plt.cycler('color',
                                             ['#1976d2', '#d32f2f', '#388e3c', '#f57c00', '#7b1fa2', '#c2185b',
                                              '#0097a7', '#689f38'])


class ConsoleWidget(QTextEdit):
    """Log console widget"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup console UI"""
        self.setMaximumHeight(150)
        self.setMinimumHeight(100)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: 'Courier New', monospace;
                font-size: 10pt;
                border: 1px solid #555555;
            }
        """)

    def log_message(self, message, type: str = 'log'):
        """Add message to log console"""
        color = {'log': '#aaa', 'error': '#ff4444', 'warning': '#ffcc66', 'success': '#66ee66'}
        style = {'log': 'normal', 'error': 'bold', 'warning': 'normal', 'success': 'normal'}
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f'<span style="color:{color[type]}; font-weight:{style[type]}" class="log_{type}">' + \
                            f'[{timestamp}] {message}</span>'
        self.append(formatted_message)
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


class SidebarTabs(QTabWidget):
    """Sidebar tabs widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.construction_tab = None
        self.requests_tab = None
        self.information_tab = None
        self.setup_ui()

    def setup_ui(self):
        """Setup sidebar tabs"""
        self.setMaximumWidth(255)

        # Construction tab
        self.construction_tab = ConstructionTab(self.parent_window)
        self.addTab(self.construction_tab, "Construction")

        # Requests tab
        self.requests_tab = RequestsTab(self.parent_window)
        self.addTab(self.requests_tab, "Requests")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QOSM - GUI")

        # Initialize variables
        self.viewer = None
        self.console = None
        self.tabs = None
        self.view_controls = None
        self.parameters_tab = None
        self.current_file = None

        # Sources management
        self.source_manager = SourceManager()

        # objects management
        self.object_manager = ObjectManager()

        # Requests management
        self.request_manager = RequestManager()

        # Create interface
        self.setup_ui()

    def setup_ui(self):
        """User interface setup"""

        # Create main horizontal layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Viewer section (center) with view controls and console
        viewer_section = QWidget()
        viewer_layout = QVBoxLayout()
        viewer_section.setLayout(viewer_layout)

        # Viewer in the middle
        self.viewer = GLViewer(src_manager=self.source_manager, obj_manager=self.object_manager,
                               req_manager=self.request_manager)
        viewer_layout.addWidget(self.viewer)

        # Console at the bottom
        self.console = ConsoleWidget()
        viewer_layout.addWidget(self.console)

        # Create tabs on the left (full height)
        self.tabs = SidebarTabs(self)

        self.parameters_tab = ParametersTab(self)
        self.tabs.construction_tab.connect_parameters(self.parameters_tab)
        self.tabs.requests_tab.connect_parameters(self.parameters_tab)

        # Menu bar
        self.create_menu_bar()

        main_layout.addWidget(self.tabs, 1)
        main_layout.addWidget(viewer_section, 2)
        main_layout.addWidget(self.parameters_tab, 3)

        # Connect callbacks after creating viewer
        self.connect_callbacks()

        # Welcome messages
        self.log_message("=== QOSM - GUI ===")

    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()

        def insert_label(label_str):
            label = QLabel(label_str)
            label.setStyleSheet("color: gray; margin: 6px;")  # Style facultatif
            label_action = QWidgetAction(self)
            label_action.setDefaultWidget(label)
            return label_action

        # File menu
        file_menu = menubar.addMenu('File')
        new_action = file_menu.addAction('\U0001F4C4 New Project')
        new_action.triggered.connect(self.new)
        new_action.setShortcut('Ctrl+N')
        open_action = file_menu.addAction('\U0001F4C1 Open Project')
        open_action.triggered.connect(self.open)
        open_action.setShortcut('Ctrl+O')
        save_action = file_menu.addAction('\U0001F4BE Save Project')
        save_action.triggered.connect(self.save)
        save_action.setShortcut('Ctrl+S')
        quit_action = file_menu.addAction('Exit')
        quit_action.setShortcut('Ctrl+Q')
        # @todo confirmation before, and propose to save !
        quit_action.triggered.connect(self.close)

        # Construction menu
        build_menu = menubar.addMenu('Construction')
        build_menu.addAction(insert_label('GBE / GBT Solver Objects'))
        import_step_action = build_menu.addAction('Import STEP')
        import_step_action.setShortcut('Ctrl+I')
        import_step_action.triggered.connect(self.tabs.construction_tab.import_step_file)
        shape_action = build_menu.addAction('Create Shape')
        shape_action.setShortcut('Ctrl+Shift+S')
        shape_action.triggered.connect(self.tabs.construction_tab.create_shape)
        lens_action = build_menu.addAction('Create Lens')
        lens_action.setShortcut('Ctrl+L')
        lens_action.triggered.connect(self.tabs.construction_tab.create_lens)
        build_menu.addSeparator()

        build_menu.addAction(insert_label('GBE / GBT Solver Pipeline Elements'))
        grid_action = build_menu.addAction('Create GBE Grid')
        grid_action.setShortcut('Ctrl+G')
        grid_action.triggered.connect(self.tabs.construction_tab.create_gbe_grid)

        domain_action = build_menu.addAction('Create GBT Domain')
        domain_action.setShortcut('Ctrl+D')
        domain_action.triggered.connect(self.tabs.construction_tab.create_domain)
        build_menu.addSeparator()

        build_menu.addAction(insert_label('GBTC Solver'))
        gbtc_port_action = build_menu.addAction('Add GBTC Port')
        gbtc_port_action.setShortcut('Ctrl+G+B')
        gbtc_port_action.triggered.connect(self.tabs.construction_tab.create_gbtc_port)
        gbtc_sample_action = build_menu.addAction('Add GBTC Multilayer Sample')
        gbtc_sample_action.setShortcut('Ctrl+M')
        gbtc_sample_action.triggered.connect(self.tabs.construction_tab.create_gbtc_mlsample)

        # Sources menu
        sources_menu = menubar.addMenu('Sources')
        feko_action = sources_menu.addAction('Near Field')
        feko_action.setShortcut('Ctrl+F')
        feko_action.setStatusTip('Create a near field source')
        feko_action.triggered.connect(self.tabs.construction_tab.create_nf_source)

        vsrc_action = sources_menu.addAction('Gaussian Beam')
        vsrc_action.setShortcut('Ctrl+B')
        vsrc_action.setStatusTip('Create a Gaussian beam source')
        vsrc_action.triggered.connect(self.tabs.construction_tab.create_gaussian_beam_source)

        horn_action = sources_menu.addAction('Horn')
        horn_action.setShortcut('Ctrl+H')
        horn_action.setStatusTip('Create a Horn')
        horn_action.triggered.connect(self.tabs.construction_tab.create_horn_source)

        # Request menu
        requests_menu = menubar.addMenu('Requests')
        requests_menu.addAction(insert_label('GBE / GBT Solver'))
        nf_action = requests_menu.addAction('Near Fields')
        nf_action.triggered.connect(self.tabs.requests_tab.create_near_field_request)
        nf_action.setShortcut('Ctrl+Shift+F')
        nf_action.setStatusTip('Add a Near Fields request associated to a domain')
        nf_action = requests_menu.addAction('Far Fields')
        nf_action.triggered.connect(self.tabs.requests_tab.create_far_field_request)
        nf_action.setShortcut('Ctrl+Alt+F')
        nf_action.setStatusTip('Add a Far Fields request associated to a horn')
        requests_menu.addSeparator()

        requests_menu.addAction(insert_label('GBTC Solver'))
        gbtc_action = requests_menu.addAction('GBTC Simulation')
        gbtc_action.triggered.connect(self.tabs.requests_tab.create_gbtc_request)
        gbtc_action.setStatusTip('Add a Gaussian Beam Tracing and Coupling request')
        requests_menu.addSeparator()

        requests_menu.addAction(insert_label('Simulation'))
        pipe_action = requests_menu.addAction('Build pipeline and simulate ')
        pipe_action.setShortcut(QKeySequence("Ctrl+Return"))
        pipe_action.setStatusTip('Build simulation pipeline and run it')
        pipe_action.triggered.connect(self.tabs.requests_tab.build)
        results_action = requests_menu.addAction('Display results')
        results_action.triggered.connect(lambda: self.tabs.requests_tab.display_results(None))
        results_action.setShortcut('Ctrl+R')
        results_action.setStatusTip('Display the simulated requests ')

        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        delete_action = edit_menu.addAction('Delete Selected Object')
        delete_action.setShortcut('Delete')
        delete_action.triggered.connect(self.delete_item)
        rename_action = edit_menu.addAction('Rename Selected Object')
        rename_action.setShortcut('F2')
        rename_action.triggered.connect(self.rename_item)

        # View menu
        view_menu = menubar.addMenu('View')
        fit_all_action = view_menu.addAction('Fit All objects')
        fit_all_action.setShortcut('F')
        fit_all_action.triggered.connect(self.viewer.fit_all_objects)
        view_menu.addSeparator()
        xy_view_action = view_menu.addAction('XY View (Front)')
        xy_view_action.setShortcut('1')
        xy_view_action.triggered.connect(self.viewer.set_view_xy)
        xz_view_action = view_menu.addAction('XZ View (Side)')
        xz_view_action.setShortcut('2')
        xz_view_action.triggered.connect(self.viewer.set_view_xz)
        yz_view_action = view_menu.addAction('YZ View (Top)')
        yz_view_action.setShortcut('3')
        yz_view_action.triggered.connect(self.viewer.set_view_yz)
        proj_toogle_view_action = view_menu.addAction('Perspective / Orthogonal View')
        proj_toogle_view_action.setShortcut('5')
        proj_toogle_view_action.triggered.connect(self.viewer.toggle_projection)

    def log_message(self, message, type: str = 'log'):
        """Add message to log console"""
        if self.console:
            self.console.log_message(message, type)

    def connect_callbacks(self):
        """Connect callbacks after viewer creation"""
        if self.viewer:
            self.tabs.construction_tab.selection_callback = self.update_gui
            self.tabs.requests_tab.selection_callback = self.update_gui
            self.viewer.selection_callback = self.update_gui
            self.viewer.log_callback = self.log_message

    def update_gui(self, item_uuid: str | None):
        if self.object_manager.exists(item_uuid):
            self.request_manager.set_active_request(None)
            self.tabs.setCurrentIndex(0)
        elif self.request_manager.exists(item_uuid):
            self.object_manager.set_active_object(None)
            self.tabs.setCurrentIndex(1)

        self.tabs.construction_tab.update_lists(update_params=False)
        self.tabs.requests_tab.update_lists(update_params=False)
        self.parameters_tab.display_parameters()

        self.viewer.update()

    def rename_item(self):
        if self.object_manager.exists(None):
            self.tabs.construction_tab.rename_object(None)
        elif self.request_manager.exists(None):
            self.tabs.requests_tab.rename_request(None)

    def delete_item(self,):
        if self.object_manager.exists(None):
            self.tabs.construction_tab.delete_object(None)
        elif self.request_manager.exists(None):
            self.tabs.requests_tab.delete_request(None)

    def reconnect_managers(self):
        self.request_manager.current_file = self.current_file

        # Construction tab
        self.tabs.construction_tab.object_manager = self.object_manager
        self.tabs.construction_tab.source_manager = self.source_manager
        # Request tab
        self.tabs.requests_tab.object_manager = self.object_manager
        self.tabs.requests_tab.request_manager = self.request_manager
        self.tabs.requests_tab.source_manager = self.source_manager
        # Parameters tab
        self.parameters_tab.object_manager = self.object_manager
        self.parameters_tab.request_manager = self.request_manager
        self.parameters_tab.source_manager = self.source_manager
        # 3D Viewer
        self.viewer.object_manager = self.object_manager
        self.viewer.source_manager = self.source_manager
        self.viewer.request_manager = self.request_manager

        self.update_gui(None)

    def new(self):

        reply = QMessageBox.question(
            self, "Create a new project ?",
            "Are you sure to discard any modification and create a new project ?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        self.setWindowTitle("QOSM - GUI")

        if reply == QMessageBox.Yes:
            self.current_file = None
            self.object_manager = ObjectManager()
            self.source_manager = SourceManager()
            self.request_manager = RequestManager()
            self.reconnect_managers()

    def save(self):
        """Save objects and sources to a binary .qosm file"""
        # Open file dialog to choose save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save QOSM File",
            "",
            "QOSM files (*.qosm);;All files (*.*)"
        )
        try:

            if file_path:
                # Add .qosm extension if not present
                if not file_path.endswith('.qosm'):
                    file_path += '.qosm'

                # Prepare data to save
                data = {
                    'object_manager': self.object_manager,
                    'source_manager': self.source_manager,
                    'request_manager': self.request_manager,
                    'sweep_data': self.tabs.requests_tab.sweep,
                }

                # @todo save the pipeline

                # Save to binary file using dill
                with open(file_path, 'wb') as file:
                    pickle.dump(data, file)

                self.log_message(f"File saved successfully to {file_path}", type='success')
                QMessageBox.information(self, "Success", f"File saved successfully to {file_path}")

        except Exception as e:
            self.log_message(f"Failed to save file: {file_path}", type='success')
            QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

    def open(self):
        """Load objects and sources from a binary .qosm file"""
        # Open file dialog to choose file to load
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open QOSM File",
            "",
            "QOSM files (*.qosm);;All files (*.*)"
        )
        try:
            if file_path:
                self.current_file = file_path

                # Load data from binary file
                with open(file_path, 'rb') as file:
                    data = pickle.load(file)
                # Restore objects and sources
                self.object_manager = data.get('object_manager', ObjectManager())
                self.source_manager = data.get('source_manager', SourceManager())
                self.request_manager = data.get('request_manager', RequestManager())

                if 'sweep_data' in data:
                    self.tabs.requests_tab.sweep = data['sweep_data']
                else:
                    self.tabs.requests_tab.sweep = {
                        'target': ('None', None),
                        'attribute': 'None',
                        'sweep': (0., 0., 1)
                    }

                self.reconnect_managers()
                self.setWindowTitle(f"QOSM - GUI \U00002192 {file_path}")

                self.log_message(f"File loaded successfully from {file_path}", type='success')

        except Exception as e:
            self.log_message(f"Failed to load file: {file_path}", type='error')
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")


def gui(argv):
    app = QApplication()
    app.setApplicationName("QOSM")
    app.setOrganizationName("IMT Atlantique / Terakalis")
    setup_style(app)
    QLocale.setDefault(QLocale.c())  # Locale C standard (always 2.3 and not 2,3)
    window = MainWindow()
    window.resize(1200, 800)
    window.showMaximized()
    sys.exit(app.exec())


def setup_style(self):
    icon_dir = create_arrow_icons()
    # Récupérer la couleur d'accentuation du système
    accent_color = self.palette().highlight().color()
    accent_hex = accent_color.name()
    accent_hover = accent_color.lighter(110).name()
    accent_pressed = accent_color.darker(110).name()

    if self.palette().window().color().lightness() < 128:
        apply_dark_mode_to_plots()
        up_arrow = str(icon_dir / 'arrow_up_dark.svg').replace('\\', '/')
        down_arrow = str(icon_dir / 'arrow_down_dark.svg').replace('\\', '/')
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: #2b2b2b; }}
            QWidget {{ background-color: #2b2b2b; color: #e0e0e0; font-family: 'Segoe UI', Arial; font-size: 9pt; }}
            QGroupBox {{ border: 2px solid #3d3d3d; border-radius: 6px; margin-top: 10px; padding-top: 12px; font-weight: bold; color: {accent_hex}; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 4px; }}
            QLineEdit {{ background-color: #3d3d3d; border: 1px solid #555; border-radius: 3px; padding: 4px; color: #e0e0e0; }}
            QLineEdit:focus {{ border: 2px solid {accent_hex}; }}
            QSpinBox, QDoubleSpinBox {{ background-color: #3d3d3d; border: 1px solid #555; border-radius: 3px; padding: 4px; padding-right: 18px; color: #e0e0e0; }}
            QSpinBox:focus, QDoubleSpinBox:focus {{ border: 2px solid {accent_hex}; }}
            QSpinBox::up-button, QDoubleSpinBox::up-button {{ background-color: #555555; border: none; border-top-right-radius: 3px; width: 16px; }}
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{ background-color: #666666; }}
            QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{ background-color: {accent_hex}; }}
            QSpinBox::down-button, QDoubleSpinBox::down-button {{ background-color: #555555; border: none; border-bottom-right-radius: 3px; width: 16px; }}
            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{ background-color: #666666; }}
            QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{ background-color: {accent_hex}; }}
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{ image: url({up_arrow}); width: 9px; height: 5px; }}
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{ image: url({down_arrow}); width: 9px; height: 5px; }}
            QComboBox {{ background-color: #3d3d3d; border: 1px solid #555; border-radius: 3px; padding: 4px 8px; color: #e0e0e0; }}
            QComboBox:focus {{ border: 2px solid {accent_hex}; }}
            QComboBox:hover {{ border: 1px solid #666; background-color: #454545; }}
            QComboBox::drop-down {{ border: none; width: 20px; }}
            QComboBox::down-arrow {{ image: url({down_arrow}); width: 9px; height: 5px; }}
            QComboBox QAbstractItemView {{ background-color: #3d3d3d; border: 1px solid #555; border-radius: 3px; selection-background-color: {accent_hex}; selection-color: white; color: #e0e0e0; padding: 4px; }}
            QComboBox QAbstractItemView::item {{ padding: 6px; border-radius: 2px; }}
            QComboBox QAbstractItemView::item:hover {{ background-color: #454545; }}
            QPushButton {{ background-color: {accent_hex}; color: white; border: none; border-radius: 4px; padding: 6px 16px; font-weight: 600; font-size: 9pt; }}
            QPushButton:hover {{ background-color: {accent_hover}; }}
            QPushButton:pressed {{ background-color: {accent_pressed}; }}
            QPushButton:disabled {{ background-color: #555; color: #888; }}    
            QPushButton#sweep_btn {{ background-color: #8b4513; padding: 6px 12px; font-size: 10pt; }}
            QPushButton#sweep_btn:hover {{ background-color: #a0522d; }}
            QPushButton#sweep_btn:pressed {{ background-color: #6b3410; }}
            QPushButton#build_btn {{ background-color: #0f7c35; padding: 6px 12px; font-size: 10pt; }}
            QPushButton#build_btn:hover {{ background-color: #12a043; }}
            QPushButton#build_btn:pressed {{ background-color: #0c5c26; }}
            QPushButton#cancel_btn {{ background-color: #d32f2f; }}
            QPushButton#cancel_btn:hover {{ background-color: #e53935; }}
            QPushButton#cancel_btn:pressed {{ background-color: #b71c1c; }}
            QPushButton#export_btn {{ padding: 6px 12px; font-size: 10pt; }}
            QTextEdit {{ background-color: #1e1e1e; border: 1px solid #3d3d3d; border-radius: 3px; padding: 6px; color: #e0e0e0; font-family: 'Consolas', 'Courier New'; }}
            QProgressBar {{ border: 1px solid #3d3d3d; border-radius: 3px; background-color: #3d3d3d; text-align: center; color: white; height: 18px; }}
            QProgressBar::chunk {{ background-color: {accent_hex}; border-radius: 2px; }}
            QCheckBox {{ spacing: 6px; }}
            QCheckBox::indicator {{ width: 16px; height: 16px; border-radius: 3px; border: 2px solid #555; background-color: #3d3d3d; }}
            QCheckBox::indicator:checked {{ background-color: {accent_hex}; border-color: {accent_pressed}; }}
            QListWidget {{ background-color: #1e1e1e; border: 1px solid #3d3d3d; border-radius: 3px; padding: 4px; color: #e0e0e0; }}
            QListWidget::item {{ padding: 6px; border-radius: 2px; }}
            QListWidget::item:selected {{ background-color: {accent_hex}; color: white; }}
            QListWidget::item:hover {{ background-color: #3d3d3d; }}
            QTabWidget::pane {{ border: 1px solid #3d3d3d; border-radius: 3px; background-color: #2b2b2b; }}
            QTabBar::tab {{ background-color: #3d3d3d; color: #e0e0e0; padding: 8px 16px; border-top-left-radius: 3px; border-top-right-radius: 3px; margin-right: 2px; }}
            QTabBar::tab:selected {{ background-color: {accent_hex}; color: white; }}
            QScrollBar:vertical {{ background-color: #2b2b2b; width: 12px; border-radius: 6px; margin: 0px; }}
            QScrollBar::handle:vertical {{ background-color: #555555; min-height: 25px; border-radius: 6px; margin: 2px; }}
            QScrollBar::handle:vertical:hover {{ background-color: #666666; }}
            QScrollBar::handle:vertical:pressed {{ background-color: {accent_hex}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
            QScrollBar:horizontal {{ background-color: #2b2b2b; height: 12px; border-radius: 6px; margin: 0px; }}
            QScrollBar::handle:horizontal {{ background-color: #555555; min-width: 25px; border-radius: 6px; margin: 2px; }}
            QScrollBar::handle:horizontal:hover {{ background-color: #666666; }}
            QScrollBar::handle:horizontal:pressed {{ background-color: {accent_hex}; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{ background: none; }}
        """)
    else:
        apply_light_mode_to_plots()
        up_arrow = str(icon_dir / 'arrow_up_light.svg').replace('\\', '/')
        down_arrow = str(icon_dir / 'arrow_down_light.svg').replace('\\', '/')
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: #f5f5f5; }}
            QWidget {{ background-color: #f5f5f5; color: #2b2b2b; font-family: 'Segoe UI', Arial; font-size: 9pt; }}
            QGroupBox {{ border: 2px solid #d0d0d0; border-radius: 6px; margin-top: 10px; padding-top: 12px; font-weight: bold; color: {accent_hex}; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 4px; }}
            QLineEdit {{ background-color: #ffffff; border: 1px solid #c0c0c0; border-radius: 3px; padding: 4px; color: #2b2b2b; }}
            QLineEdit:focus {{ border: 2px solid {accent_hex}; }}
            QSpinBox, QDoubleSpinBox {{ background-color: #ffffff; border: 1px solid #c0c0c0; border-radius: 3px; padding: 4px; padding-right: 18px; color: #2b2b2b; }}
            QSpinBox:focus, QDoubleSpinBox:focus {{ border: 2px solid {accent_hex}; }}
            QSpinBox::up-button, QDoubleSpinBox::up-button {{ background-color: #e0e0e0; border: none; border-top-right-radius: 3px; width: 16px; }}
            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{ background-color: #d0d0d0; }}
            QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{ background-color: {accent_hex}; }}
            QSpinBox::down-button, QDoubleSpinBox::down-button {{ background-color: #e0e0e0; border: none; border-bottom-right-radius: 3px; width: 16px; }}
            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{ background-color: #d0d0d0; }}
            QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{ background-color: {accent_hex}; }}
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{ image: url({up_arrow}); width: 9px; height: 5px; }}
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{ image: url({down_arrow}); width: 9px; height: 5px; }}
            QComboBox {{ background-color: #ffffff; border: 1px solid #c0c0c0; border-radius: 3px; padding: 4px 8px; color: #2b2b2b; }}
            QComboBox:focus {{ border: 2px solid {accent_hex}; }}
            QComboBox:hover {{ border: 1px solid #a0a0a0; background-color: #f8f8f8; }}
            QComboBox::drop-down {{ border: none; width: 20px; }}
            QComboBox::down-arrow {{ image: url({down_arrow}); width: 9px; height: 5px; }}
            QComboBox QAbstractItemView {{ background-color: #ffffff; border: 1px solid #c0c0c0; border-radius: 3px; selection-background-color: {accent_hex}; selection-color: white; color: #2b2b2b; padding: 4px; }}
            QComboBox QAbstractItemView::item {{ padding: 6px; border-radius: 2px; }}
            QComboBox QAbstractItemView::item:hover {{ background-color: #f0f0f0; }}
            QPushButton {{ background-color: {accent_hex}; color: white; border: none; border-radius: 4px; padding: 6px 16px; font-weight: 600; font-size: 9pt; }}
            QPushButton:hover {{ background-color: {accent_hover}; }}
            QPushButton:pressed {{ background-color: {accent_pressed}; }}
            QPushButton:disabled {{ background-color: #e0e0e0; color: #9e9e9e; }}
            QPushButton#sweep_btn {{ background-color: #d67d3e; padding: 6px 12px; font-size: 10pt; }}
            QPushButton#sweep_btn:hover {{ background-color: #e08f52; }}
            QPushButton#sweep_btn:pressed {{ background-color: #c56b2a; }}
            QPushButton#build_btn {{ background-color: #2e8b57; padding: 6px 12px; font-size: 10pt; }}
            QPushButton#build_btn:hover {{ background-color: #3cb371; }}
            QPushButton#build_btn:pressed {{ background-color: #256d43; }}
            QPushButton#cancel_btn {{ background-color: #e53935; }}
            QPushButton#cancel_btn:hover {{ background-color: #ef5350; }}
            QPushButton#cancel_btn:pressed {{ background-color: #c62828; }}
            QPushButton#export_btn {{ padding: 6px 12px; font-size: 10pt; }}
            QTextEdit {{ background-color: #ffffff; border: 1px solid #d0d0d0; border-radius: 3px; padding: 6px; color: #2b2b2b; font-family: 'Consolas', 'Courier New'; }}
            QProgressBar {{ border: 1px solid #d0d0d0; border-radius: 3px; background-color: #e8e8e8; text-align: center; color: #2b2b2b; height: 18px; }}
            QProgressBar::chunk {{ background-color: {accent_hex}; border-radius: 2px; }}
            QCheckBox {{ spacing: 6px; }}
            QCheckBox::indicator {{ width: 16px; height: 16px; border-radius: 3px; border: 2px solid #c0c0c0; background-color: #ffffff; }}
            QCheckBox::indicator:checked {{ background-color: {accent_hex}; border-color: {accent_pressed}; }}
            QListWidget {{ background-color: #ffffff; border: 1px solid #d0d0d0; border-radius: 3px; padding: 4px; color: #2b2b2b; }}
            QListWidget::item {{ padding: 6px; border-radius: 2px; }}
            QListWidget::item:selected {{ background-color: {accent_hex}; color: white; }}
            QListWidget::item:hover {{ background-color: #f0f0f0; }}
            QTabWidget::pane {{ border: 1px solid #d0d0d0; border-radius: 3px; background-color: #f5f5f5; }}
            QTabBar::tab {{ background-color: #e0e0e0; color: #2b2b2b; padding: 8px 16px; border-top-left-radius: 3px; border-top-right-radius: 3px; margin-right: 2px; }}
            QTabBar::tab:selected {{ background-color: {accent_hex}; color: white; }}
            QScrollBar:vertical {{ background-color: #f5f5f5; width: 12px; border-radius: 6px; margin: 0px; }}
            QScrollBar::handle:vertical {{ background-color: #c0c0c0; min-height: 25px; border-radius: 6px; margin: 2px; }}
            QScrollBar::handle:vertical:hover {{ background-color: #a0a0a0; }}
            QScrollBar::handle:vertical:pressed {{ background-color: {accent_hex}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
            QScrollBar:horizontal {{ background-color: #f5f5f5; height: 12px; border-radius: 6px; margin: 0px; }}
            QScrollBar::handle:horizontal {{ background-color: #c0c0c0; min-width: 25px; border-radius: 6px; margin: 2px; }}
            QScrollBar::handle:horizontal:hover {{ background-color: #a0a0a0; }}
            QScrollBar::handle:horizontal:pressed {{ background-color: {accent_hex}; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{ background: none; }}
        """)


if __name__ == "__main__":
    gui()

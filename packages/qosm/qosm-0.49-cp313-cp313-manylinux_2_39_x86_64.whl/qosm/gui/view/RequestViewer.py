from PySide6.QtWidgets import (QMainWindow, QPushButton, QTabWidget)
import matplotlib

from qosm.gui.managers import ResultViewManager

matplotlib.use('Agg')

class ResultMainWindow(QMainWindow):
    """Main window for managing multiple Near Field views as tabs"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Request Viewer")
        self.setMinimumWidth(1200)
        self.setMinimumHeight(800)

        # Central widget with QTabWidget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create result view manager
        self.view_manager = ResultViewManager(self.tab_widget)

        # Button to add new tab
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.setStyleSheet("padding-left: 10px; padding-right: 10px;")
        # self.add_tab_button.setMaximumWidth(30)
        self.add_tab_button.setToolTip("Add new view")
        self.tab_widget.setCornerWidget(self.add_tab_button)

        # Connect add button
        self.add_tab_button.clicked.connect(self.add_view)

    def set_available_requests(self, requests_dict):
        """Set available requests for all viewers"""
        self.view_manager.set_available_requests(requests_dict)

    def add_request(self, request_id, data_dict):
        """Add a single request to available requests"""
        self.view_manager.add_request(request_id, data_dict)

    def add_view(self, selected_request=None, viewer_type='NearField'):
        """Add a new view using the view manager"""
        return self.view_manager.add_view(selected_request, viewer_type)


def launch_gui_request_viewer(request_results=None):
    if request_results is None:
        request_results = {}
    if len(request_results) == 0:
        return

    # Create main window
    window = ResultMainWindow()

    # Set available requests
    window.set_available_requests(request_results)

    for req_uuid, req in list(request_results.items()):
        window.add_view(req_uuid, req['request_type'])

    # Show
    window.show()
    return window
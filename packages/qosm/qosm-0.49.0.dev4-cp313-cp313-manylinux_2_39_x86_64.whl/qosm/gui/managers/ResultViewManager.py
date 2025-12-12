# do not import directly from view to avoid cyclic import
from qosm.gui.view.requests.FarField import FarFieldViewer
from qosm.gui.view.requests.GBTC import GBTCViewer
from qosm.gui.view.requests.NearField import NearFieldViewer


class ResultViewManager:
    """Manager for handling different types of result viewers in tabs"""

    def __init__(self, tab_widget):
        self.tab_widget = tab_widget
        self.view_counter = 1
        self.registered_viewers = {}  # viewer_type -> viewer_class
        self.available_requests = {}  # Global storage of all available requests

        # Setup tab widget
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Register default viewers
        self.register_viewer('NearField', NearFieldViewer)
        self.register_viewer('FarField', FarFieldViewer)
        self.register_viewer('GBTCSim', GBTCViewer)

    def register_viewer(self, viewer_type, viewer_class):
        """Register a new viewer type"""
        self.registered_viewers[viewer_type] = viewer_class

    def set_available_requests(self, requests_dict):
        """Set the available requests for all viewers"""
        self.available_requests = requests_dict

    def add_request(self, request_id, data_dict):
        """Add a single request to available requests"""
        self.available_requests[request_id] = data_dict

    def add_view(self, selected_request=None, viewer_type='NearField'):
        """Add a new view of specified type"""
        if viewer_type not in self.registered_viewers:
            raise ValueError(f"Unknown viewer type: {viewer_type}")

        # Get requests compatible with this viewer type
        if viewer_type == 'NearField':
            compatible_requests = self.get_requests_by_type('NearField')
        if viewer_type == 'FarField':
            compatible_requests = self.get_requests_by_type('FarField')
        if viewer_type == 'GBTCSim':
            compatible_requests = self.get_requests_by_type('GBTCSim')
        else:
            # For future viewer types, add their compatible request types
            compatible_requests = self.available_requests

        if not compatible_requests:
            raise ValueError(f"No compatible requests available for viewer type: {viewer_type}")

        # If no specific request selected, use first compatible one
        if selected_request is None or selected_request not in compatible_requests:
            selected_request = list(compatible_requests.keys())[0]

        viewer_class = self.registered_viewers[viewer_type]
        viewer = viewer_class(
            compatible_requests,
            selected_request,
            self.view_counter,
            self.tab_widget
        )

        # Connect new view requests to this manager
        if hasattr(viewer, 'new_view_requested'):
            viewer.new_view_requested.connect(
                lambda data: self.add_view(viewer.current_request_id, viewer_type)
            )

        # Create tab name
        tab_name = self.create_tab_name(selected_request, self.view_counter)

        # Add tab
        tab_index = self.tab_widget.addTab(viewer, tab_name)
        self.tab_widget.setCurrentIndex(tab_index)

        self.view_counter += 1
        return viewer

    def create_tab_name(self, selected_request, view_id):
        """Create appropriate tab name based on viewer type and data"""
        base_name = f"View #{view_id}"

        if selected_request and selected_request in self.available_requests:
            data_dict = self.available_requests[selected_request]
            base_name = str(data_dict.get('req_name', selected_request))

        return base_name

    def close_tab(self, index):
        """Close a specific tab"""
        if self.tab_widget.count() > 1:  # Keep at least one tab
            self.tab_widget.removeTab(index)

    def get_active_viewer(self):
        """Get the currently active viewer"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            return self.tab_widget.widget(current_index)
        return None

    def get_all_viewers(self, viewer_type=None):
        """Get all viewers of a specific type, or all if type is None"""
        viewers = []
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if viewer_type is None:
                viewers.append(widget)
            elif isinstance(widget, self.registered_viewers.get(viewer_type, type(None))):
                viewers.append(widget)
        return viewers

    def get_requests_by_type(self, request_type):
        """Get all requests of a specific type"""
        filtered_requests = {}
        for req_id, data_dict in self.available_requests.items():
            if data_dict.get('request_type') == request_type:
                filtered_requests[req_id] = data_dict
        return filtered_requests


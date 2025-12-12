import os
import uuid
from enum import Enum

from qosm import Grid, VirtualSource
class RequestType(Enum):
    NEAR_FIELD = 'Near Field'
    FAR_FIELD = 'Far Field'
    GBTC = 'GBTC'

class RequestManager:
    """Gestionnaire des sources dans l'application principale"""

    def __init__(self):
        self.requests = {}
        self.counters = {
            RequestType.NEAR_FIELD.name: 0,
            RequestType.FAR_FIELD.name: 0,
            RequestType.GBTC.name: 0,
        }
        self.active_request_uuid = None
        self.current_file = None


    def add_request(self, req_type: RequestType, params: dict = None) -> bool:
        """Add a new request"""
        try:

            _uuid = str(uuid.uuid4())
            if req_type.name in self.counters:
                self.counters[req_type.name] += 1
                count = self.counters[req_type.name]
            else:
                count = 'NaN'
                return False

            _name = f"{req_type.value} {count}"

            self.requests[_uuid] = {
                'name': _name,
                'type': req_type.name,
                'enabled': True,
                'parameters': params
            }

            if self.active_request_uuid is None:
                self.active_request_uuid = _uuid

            return True
        except Exception as e:
            print(f"Error adding object: {e}")
            return False

    def remove_request(self, req_uuid) -> str:
        """Remove a request"""
        try:
            if req_uuid in self.requests:
                # Get object info for logging
                display_name = self.get_request_display_name(req_uuid)

                # Remove from objects dictionary
                self.requests.pop(req_uuid)

                return display_name

        except Exception as e:
            print(f"Error removing source: {e}")

        return None

    def set_request_name(self, name: str, req_uuid: str = None) -> bool:
        if req_uuid is None or req_uuid not in self.requests:
            return False
        self.requests[req_uuid]['name'] = name
        return True


    def toggle_enable_disable(self, req_uuid) -> bool:
        if req_uuid in self.requests:
            self.requests[req_uuid]['enabled'] = not self.requests[req_uuid]['enabled']
            return True
        else:
            return False

    def exists(self, req_uuid = None) -> bool:
        if not req_uuid:
            req_uuid = self.active_request_uuid
        return req_uuid is not None and req_uuid in self.requests

    ### ===============
    ### GETTERS
    ### ===============

    def get(self, req_uuid: str):
        """Return a request"""
        if self.exists(req_uuid):
            return self.requests[req_uuid]
        return None

    def get_active_request(self):
        """Return the active request"""
        if self.exists():
            return self.requests[self.active_request_uuid]
        return None

    def get_ordered_requests(self):
        """Return requests in consistent order for rendering"""
        return list(self.requests.items())

    def get_requests_by_type(self):
        """Return requests grouped by type"""
        requests_by_type = {
            RequestType.NEAR_FIELD.name: [],
            RequestType.FAR_FIELD.name: [],
            RequestType.GBTC.name: [],
        }

        for object_uuid, req in self.requests.items():
            type_name = req['type']
            if type_name in requests_by_type:
                requests_by_type[type_name].append((object_uuid, req))

        return requests_by_type

    @staticmethod
    def get_object_type_name(obj):
        pass

    def get_request_display_name(self, object_uuid):
        if object_uuid in self.requests:
            return self.requests[object_uuid].get('name', 'Undefined')
        return None

    ### ===============
    ### Setter
    ### ===============
    def set_active_request(self, req_uuid) -> bool:
        """Set the active request"""
        if self.exists(req_uuid):
            self.active_request_uuid = req_uuid
            return True
        return False

    def update_active_request(self, params: dict) -> bool:
        if not self.exists():
            return False

        self.get_active_request()['parameters'] = params
        return True
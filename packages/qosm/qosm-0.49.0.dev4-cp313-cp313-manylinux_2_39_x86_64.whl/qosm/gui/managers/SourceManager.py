import uuid
from typing import List, Optional

class SourceManager:
    """Gestionnaire des sources dans l'application principale"""

    def __init__(self):
        self.sources = {}
        self.active_source_uuid: Optional[str] = None

    @staticmethod
    def get_source_type_name(obj):
        """Return the type name of an object"""
        return obj['type']

    def add_source(self, src_type, name, params=None) -> bool:
        """Ajoute une nouvelle source"""
        if params is None:
            params = {}
        try:
            _uuid = str(uuid.uuid4())
            self.sources[_uuid] = {'name': name, 'type': src_type, 'parameters': params}
            if self.active_source_uuid is None:
                self.active_source_uuid = _uuid
            return True
        except Exception as e:
            print(f"Error adding source: {e}")
            return False

    def edit_source(self, src_uuid, params) -> bool:
        """Edit a source"""
        try:
            self.sources[src_uuid]['name'] = params['source_name']
            self.sources[src_uuid]['parameters'] = params
            return True
        except Exception as e:
            print(f"Error editing source: {e}")
            return False

    def remove_source(self, src_uuid: str) -> bool:
        """Remove a source"""
        if not src_uuid:
            src_uuid = self.active_source_uuid

        try:
            if src_uuid in self.sources:
                # Remove from objects dictionary
                self.sources.pop(src_uuid)

                if self.active_source_uuid == src_uuid:
                    self.active_source_uuid = None

                return True

        except Exception as e:
            print(f"Error removing object: {e}")

        return False

    def get_active_source(self):
        """Retourne la source active"""
        if self.active_source_uuid is not None and self.active_source_uuid in self.sources:
            return self.sources[self.active_source_uuid]
        return None

    def set_active_source(self, src_uuid: int) -> bool:
        """Définit la source active"""
        if src_uuid in self.sources:
            self.active_source_uuid = src_uuid
            return True
        return False

    def get_source_list(self) -> List[str]:
        """Retourne la liste des noms de sources"""
        return [source.name for source in self.sources]

    def exists(self, src_uuid: str = None) -> bool:
        if not src_uuid:
            src_uuid = self.active_source_uuid
        return src_uuid in self.sources

    def get_sources(self, only_type: str = None) -> List[tuple]:
        """Retourne la liste des noms de sources"""
        if not only_type:
            return [(src_uuid, src) for src_uuid, src in self.sources.items()]
        else:
            result = []
            for src_uuid, src in self.sources.items():
                if self.get_source_type_name(src) == only_type:
                    result.append((src_uuid, src))
            return result

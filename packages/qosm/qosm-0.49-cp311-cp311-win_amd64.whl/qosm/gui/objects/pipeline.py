class SimulationPipeline:
    def __init__(self, nodes_dict, active_src_uuid=None):
        """
        Initialize the SimulationPipeline.

        Args:
            nodes_dict (dict): Dictionary with 'uuid' -> item (dict)
            active_src_uuid (str, optional): UUID of the active source node
        """
        self.nodes_dict = nodes_dict
        self.active_src_uuid = active_src_uuid
        self._forward_connections = {}
        self._backward_connections = {}
        self._build_connections()

    def _build_connections(self):
        """Build forward and backward connection mappings."""
        self._forward_connections = {}
        self._backward_connections = {}

        for uuid, item in self.nodes_dict.items():
            if item is None:
                continue

            # Check if this is a valid node with parameters
            if item['type'].lower() not in ('gbe', 'domain', 'gbtcport', 'gbtcsample'):
                continue
            if 'parameters' in item and 'source' in item['parameters']:
                source_uuid = item['parameters']['source']
                if source_uuid == 'active_src_uuid':
                    source_uuid = self.active_src_uuid

                if source_uuid:
                    # Forward connection: source -> current node
                    if source_uuid not in self._forward_connections:
                        self._forward_connections[source_uuid] = []
                    self._forward_connections[source_uuid].append(uuid)

                    # Backward connection: current node -> source
                    self._backward_connections[uuid] = source_uuid

    def _get_node_name(self, uuid):
        """Get the name of a node, fallback to uuid if no name exists."""
        item = self.nodes_dict.get(uuid, {})
        return item.get('name', uuid)

    def _find_all_branches_from_node(self, start_uuid, show_id=True):
        """
        Find all branches starting from a given node.

        Args:
            start_uuid (str): UUID of the starting node
            show_id (bool): If True, return UUIDs; if False, return names

        Returns:
            list: List of branches, where each branch is a list of UUIDs or names
        """
        branches = []

        def dfs(current_uuid, current_path):
            # Get the identifier (UUID or name) for current node
            identifier = current_uuid if show_id else self._get_node_name(current_uuid)
            new_path = current_path + [identifier]

            # Get forward connections from current node
            forward_nodes = self._forward_connections.get(current_uuid, [])

            if not forward_nodes:
                # This is a leaf node, add the complete path as a branch
                branches.append(new_path)
            else:
                # Continue DFS for each forward connection
                for next_uuid in forward_nodes:
                    dfs(next_uuid, new_path)

        # Start DFS from the given node
        dfs(start_uuid, [])
        return branches

    def get_all_branches(self, show_id=True):
        """
        Get all possible branches in the pipeline.

        Args:
            show_id (bool): If True, return UUIDs; if False, return names

        Returns:
            list: List of all branches
        """
        all_branches = []

        # Find all root nodes (nodes that are not targets of any backward connection)
        root_nodes = set(self.nodes_dict.keys()) - set(self._backward_connections.keys())

        for root_uuid in root_nodes:
            branches = self._find_all_branches_from_node(root_uuid, show_id)
            all_branches.extend(branches)

        return all_branches

    def get_valid_branches(self, show_id=True):
        """
        Get all valid branches (starting from active_src_uuid).

        Args:
            show_id (bool): If True, return UUIDs; if False, return names

        Returns:
            list: List of valid branches, or empty list if no active source is set
        """
        if not self.active_src_uuid:
            return []

        if self.active_src_uuid not in self.nodes_dict:
            return []

        return self._find_all_branches_from_node(self.active_src_uuid, show_id)

    def set_active_source(self, uuid):
        """
        Set the active source UUID.

        Args:
            uuid (str): UUID of the active source node
        """
        self.active_src_uuid = uuid

    def get_node_info(self, uuid):
        """
        Get information about a specific node.

        Args:
            uuid (str): UUID of the node

        Returns:
            dict: Node information or None if not found
        """
        return self.nodes_dict.get(uuid)

    def get_forward_connections(self, uuid):
        """
        Get all nodes that this node connects to (forward connections).

        Args:
            uuid (str): UUID of the node

        Returns:
            list: List of UUIDs that this node connects to
        """
        return self._forward_connections.get(uuid, [])

    def get_backward_connection(self, uuid):
        """
        Get the node that this node connects from (backward connection).

        Args:
            uuid (str): UUID of the node

        Returns:
            str or None: UUID of the source node, or None if no backward connection
        """
        return self._backward_connections.get(uuid)

    def print_pipeline_structure(self):
        """Print a visual representation of the pipeline structure."""
        print("Pipeline Structure:")
        print("=" * 50)

        # Find root nodes
        root_nodes = set(self.nodes_dict.keys()) - set(self._backward_connections.keys())

        def print_tree(uuid, level=0):
            indent = "  " * level
            name = self._get_node_name(uuid)
            print(f"{indent}{name} ({uuid})")

            # Print forward connections
            forward_nodes = self._forward_connections.get(uuid, [])
            for next_uuid in forward_nodes:
                print_tree(next_uuid, level + 1)

        for root_uuid in root_nodes:
            print_tree(root_uuid)

class InvalidPipeline(Exception):
    def __init__(self, message="Unknown error"):
        self.message = message
        super().__init__(f'Invalid pipeline: {self.message}')


def show_branch_selector(pipeline):
    from PySide6.QtWidgets import (QApplication, QDialog)
    from qosm.gui.dialogs import PipelineBranchSelector
    import sys

    """
    Show the branch selector dialog and return selected branches.

    Args:
        pipeline (SimulationPipeline): The pipeline instance

    Returns:
        tuple: (accepted, selected_branches) where accepted is bool and
               selected_branches is list of selected branch paths
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    dialog = PipelineBranchSelector(pipeline)
    result = dialog.exec()

    if result == QDialog.Accepted:
        return True, dialog.get_selected_branches()
    else:
        return False, []


# Example usage
if __name__ == "__main__":
    # Sample data with types
    sample_nodes = {
        "node_1": {
            "name": "Input Source",
            "type": "gbe",
            "parameters": {}
        },
        "node_2": {
            "name": "Processor A",
            "type": "gbe",
            "parameters": {
                "source": "node_1"
            }
        },
        "node_3": {
            "name": "Processor B",
            "type": "domain",
            "parameters": {
                "source": "node_1"
            }
        },
        "node_4": {
            "name": "Filter",
            "type": "gbe",
            "parameters": {
                "source": "node_2"
            }
        },
        "node_5": {
            "name": "Output A",
            "type": "domain",
            "parameters": {
                "source": "node_4"
            }
        },
        "node_6": {
            "name": "Output B",
            "type": "gbe",
            "parameters": {
                "source": "node_3"
            }
        }
    }

    # Create pipeline
    pipeline = SimulationPipeline(sample_nodes, active_src_uuid="node_1")

    # Show dialog
    accepted, selected_branches = show_branch_selector(pipeline)

    if accepted:
        print(f"Selected {len(selected_branches)} branches:")
        for i, branch in enumerate(selected_branches, 1):
            print(f"  Branch {i}: {' → '.join(branch)}")
    else:
        print("Dialog was cancelled.")
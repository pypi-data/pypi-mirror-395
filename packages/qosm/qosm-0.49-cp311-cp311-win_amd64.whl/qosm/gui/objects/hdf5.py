import h5py
import numpy as np
import os
from datetime import datetime
from PySide6.QtWidgets import QFileDialog, QMessageBox, QProgressDialog, QApplication
from PySide6.QtCore import Qt


class HDF5Exporter:
    """Class for exporting simulation data to HDF5 format"""

    def __init__(self, parent=None):
        self.parent = parent

    def export_single_request(self, data_dict, suggested_filename=None):
        """Export a single request's data to HDF5"""
        if not data_dict:
            QMessageBox.warning(self.parent, "Export Error", "No data available to export.")
            return False

        # Generate suggested filename if not provided
        if not suggested_filename:
            req_name = str(data_dict.get('req_name', 'unknown_request'))
            # Clean filename for filesystem compatibility
            clean_name = "".join(c for c in req_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            suggested_filename = f"{clean_name}.h5"

        # Open file dialog
        filename, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Export Request Data to HDF5",
            suggested_filename,
            "HDF5 Files (*.h5 *.hdf5);;All Files (*)"
        )

        if not filename:
            return False

        try:
            self._write_single_request_to_hdf5(filename, data_dict)
            QMessageBox.information(
                self.parent,
                "Export Successful",
                f"Request data exported successfully to:\n{filename}"
            )
            return True
        except Exception as e:
            QMessageBox.critical(
                self.parent,
                "Export Error",
                f"Failed to export data:\n{str(e)}"
            )
            return False

    def export_all_results(self, results_dict, suggested_filename=None):
        """Export all simulation results to a single HDF5 file"""
        if not results_dict:
            QMessageBox.warning(self.parent, "Export Error", "No results available to export.")
            return False

        # Generate suggested filename if not provided
        if not suggested_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            suggested_filename = f"simulation_results_{timestamp}.h5"

        # Open file dialog
        filename, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Export All Results to HDF5",
            suggested_filename,
            "HDF5 Files (*.h5 *.hdf5);;All Files (*)"
        )

        if not filename:
            return False

        # Create progress dialog
        progress = QProgressDialog("Exporting all results to HDF5...", "Cancel", 0, len(results_dict), self.parent)
        progress.setWindowTitle("Exporting Results")
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.show()

        try:
            self._write_all_results_to_hdf5(filename, results_dict, progress)

            if not progress.wasCanceled():
                QMessageBox.information(
                    self.parent,
                    "Export Successful",
                    f"All simulation results exported successfully to:\n{filename}"
                )
                return True
            else:
                # Clean up incomplete file
                if os.path.exists(filename):
                    os.remove(filename)
                return False

        except Exception as e:
            progress.close()
            QMessageBox.critical(
                self.parent,
                "Export Error",
                f"Failed to export results:\n{str(e)}"
            )
            return False
        finally:
            progress.close()

    def _write_single_request_to_hdf5(self, filename, data_dict):
        """Write a single request's data to HDF5 file"""
        with h5py.File(filename, 'w') as f:
            # Add metadata
            self._add_metadata(f, "Single Request Export")

            # Create request group
            req_group = f.create_group("request")
            self._write_request_data(req_group, data_dict)

    def _write_all_results_to_hdf5(self, filename, results_dict, progress=None):
        """Write all results to HDF5 file"""
        with h5py.File(filename, 'w') as f:
            # Add metadata
            self._add_metadata(f, "All Results Export")

            # Create requests group
            requests_group = f.create_group("requests")

            for i, (request_id, data_dict) in enumerate(results_dict.items()):
                if progress and progress.wasCanceled():
                    break

                # Create individual request group
                req_group = requests_group.create_group(f"request_{request_id}")
                self._write_request_data(req_group, data_dict)

                if progress:
                    progress.setValue(i + 1)
                    QApplication.processEvents()

    def _write_request_data(self, group, data_dict):
        """Write request data to an HDF5 group"""
        # Store basic request information
        info_group = group.create_group("info")

        # Store string attributes safely
        for key in ['req_name', 'req_field', 'request_type', 'domain_name']:
            value = data_dict.get(key, 'N/A')
            if value is not None:
                info_group.attrs[key] = str(value)

        # Store UUID if available
        if 'req_uuid' in data_dict:
            info_group.attrs['req_uuid'] = str(data_dict['req_uuid'])

        # Store domain UUID if available
        if 'domain_uuid' in data_dict:
            info_group.attrs['domain_uuid'] = str(data_dict['domain_uuid'])

        # Store grid information
        if 'grid' in data_dict:
            grid_group = group.create_group("grid")
            grid_info = data_dict['grid']

            # Store grid parameters
            if 'n' in grid_info:
                grid_group.attrs['n'] = grid_info['n']

            if 'u_range' in grid_info:
                grid_group.create_dataset('u_range', data=np.array(grid_info['u_range']))

            if 'v_range' in grid_info:
                grid_group.create_dataset('v_range', data=np.array(grid_info['v_range']))

            # Store plane type if available
            if 'plane' in grid_info:
                grid_group.attrs['plane'] = str(grid_info['plane'])

        # Store sweep information
        if 'sweep_values' in data_dict:
            sweep_group = group.create_group("sweep")
            sweep_group.create_dataset('values', data=np.array(data_dict['sweep_values']))

            if 'sweep_attribute' in data_dict:
                sweep_group.attrs['attribute'] = str(data_dict['sweep_attribute'])

        # Store field data (main simulation results)
        if 'data' in data_dict and data_dict['data']:
            data_group = group.create_group("field_data")
            field_data_list = data_dict['data']

            # Store number of iterations
            data_group.attrs['num_iterations'] = len(field_data_list)

            for i, field_data in enumerate(field_data_list):
                if isinstance(field_data, np.ndarray):
                    # Handle complex data properly
                    if np.iscomplexobj(field_data):
                        # Store complex data as compound dataset with real and imaginary parts
                        iteration_group = data_group.create_group(f"iteration_{i}")
                        iteration_group.create_dataset('real', data=field_data.real)
                        iteration_group.create_dataset('imag', data=field_data.imag)
                        iteration_group.attrs['dtype'] = 'complex'
                        iteration_group.attrs['shape'] = field_data.shape
                    else:
                        # Store real data directly
                        data_group.create_dataset(f"iteration_{i}", data=field_data)

        # Store any additional parameters
        if 'parameters' in data_dict:
            params_group = group.create_group("parameters")
            self._store_parameters(params_group, data_dict['parameters'])

    def _store_parameters(self, group, params_dict):
        """Store parameters dictionary in HDF5 group"""
        for key, value in params_dict.items():
            try:
                if isinstance(value, (int, float, bool)):
                    group.attrs[key] = value
                elif isinstance(value, str):
                    group.attrs[key] = value
                elif isinstance(value, (list, tuple)) and len(value) > 0:
                    # Convert to numpy array for storage
                    if all(isinstance(x, (int, float)) for x in value):
                        group.create_dataset(key, data=np.array(value))
                    else:
                        # Store as string array
                        group.attrs[key] = str(value)
                elif isinstance(value, np.ndarray):
                    group.create_dataset(key, data=value)
                else:
                    # Store as string representation
                    group.attrs[key] = str(value)
            except Exception as e:
                # If storage fails, store as string
                group.attrs[f"{key}_str"] = str(value)

    def _add_metadata(self, file_handle, export_type):
        """Add metadata to HDF5 file"""
        file_handle.attrs['export_type'] = export_type
        file_handle.attrs['export_timestamp'] = datetime.now().isoformat()
        file_handle.attrs['software'] = 'QOSM Near Field Viewer'
        file_handle.attrs['version'] = '1.0'
        file_handle.attrs['hdf5_version'] = h5py.version.hdf5_version
        file_handle.attrs['h5py_version'] = h5py.version.version


class HDF5Loader:
    """Class for loading simulation data from HDF5 format"""

    @staticmethod
    def load_single_request(filename):
        """Load a single request from HDF5 file"""
        try:
            with h5py.File(filename, 'r') as f:
                if 'request' in f:
                    return HDF5Loader._read_request_data(f['request'])
                else:
                    raise ValueError("Invalid HDF5 file format: no request data found")
        except Exception as e:
            raise Exception(f"Failed to load HDF5 file: {str(e)}")

    @staticmethod
    def load_all_results(filename):
        """Load all results from HDF5 file"""
        try:
            results = {}
            with h5py.File(filename, 'r') as f:
                if 'requests' in f:
                    requests_group = f['requests']
                    for req_key in requests_group.keys():
                        req_group = requests_group[req_key]
                        # Extract request ID from group name
                        request_id = req_key.replace('request_', '')
                        results[request_id] = HDF5Loader._read_request_data(req_group)
                else:
                    raise ValueError("Invalid HDF5 file format: no requests data found")
            return results
        except Exception as e:
            raise Exception(f"Failed to load HDF5 file: {str(e)}")

    @staticmethod
    def _read_request_data(group):
        """Read request data from HDF5 group"""
        data_dict = {}

        # Read basic information
        if 'info' in group:
            info_group = group['info']
            for key in info_group.attrs.keys():
                data_dict[key] = info_group.attrs[key]

        # Read grid information
        if 'grid' in group:
            grid_group = group['grid']
            grid_info = {}

            for key in grid_group.attrs.keys():
                grid_info[key] = grid_group.attrs[key]

            for key in grid_group.keys():
                grid_info[key] = grid_group[key][...]

            data_dict['grid'] = grid_info

        # Read sweep information
        if 'sweep' in group:
            sweep_group = group['sweep']
            if 'values' in sweep_group:
                data_dict['sweep_values'] = sweep_group['values'][...].tolist()
            for key in sweep_group.attrs.keys():
                data_dict[key] = sweep_group.attrs[key]

        # Read field data
        if 'field_data' in group:
            data_group = group['field_data']
            field_data_list = []

            # Get number of iterations
            num_iterations = data_group.attrs.get('num_iterations', 0)

            for i in range(num_iterations):
                iteration_key = f"iteration_{i}"
                if iteration_key in data_group:
                    # Handle different data storage formats
                    if isinstance(data_group[iteration_key], h5py.Group):
                        # Complex data stored as group with real/imag
                        iteration_group = data_group[iteration_key]
                        if 'real' in iteration_group and 'imag' in iteration_group:
                            real_data = iteration_group['real'][...]
                            imag_data = iteration_group['imag'][...]
                            complex_data = real_data + 1j * imag_data
                            field_data_list.append(complex_data)
                    else:
                        # Direct dataset
                        field_data_list.append(data_group[iteration_key][...])

            data_dict['data'] = field_data_list

        # Read parameters
        if 'parameters' in group:
            params_group = group['parameters']
            parameters = {}

            for key in params_group.attrs.keys():
                parameters[key] = params_group.attrs[key]

            for key in params_group.keys():
                parameters[key] = params_group[key][...].tolist()

            data_dict['parameters'] = parameters

        return data_dict
from io import StringIO
import re

from PySide6.QtCore import QThread, Signal
from numpy import loadtxt, array, zeros, min, max, stack, reshape, linspace


class TicraFileLoader(QThread):
    """
    Background thread for loading TICRA near-field files (.grd format).

    This thread loads and parses TICRA GRD files asynchronously to avoid
    blocking the UI during file operations.

    Signals:
        progress (int): Emitted during loading with progress percentage (0-100)
        finished_loading (dict): Emitted when loading completes successfully with data
        error_occurred (str): Emitted when an error occurs with error message

    Attributes:
        grd_e_path (str): Path to the GRD file containing electric field data
        grd_h_path (str): Path to the GRD file containing magnetic field data
        z_plane (float): Z coordinate of the XY plane
    """
    progress = Signal(int)
    finished_loading = Signal(dict)
    error_occurred = Signal(str)

    def __init__(self, grd_e_path, grd_h_path, z_plane=0.0):
        """
        Initialize the TICRA file loader.

        Args:
            grd_e_path (str): Path to the GRD file containing electric field data
            grd_h_path (str): Path to the GRD file containing magnetic field data
            z_plane (float): Z coordinate of the XY plane (default: 0.0)
        """
        super().__init__()
        self.grd_e_path = grd_e_path
        self.grd_h_path = grd_h_path
        self.z_plane = z_plane

    def run(self):
        """
        Main thread execution method.

        Loads TICRA files and emits appropriate signals based on success or failure.
        """
        try:
            data = self.load_ticra_files(self.grd_e_path, self.grd_h_path, self.z_plane)
            self.finished_loading.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def load_ticra_files(self, grd_e_path, grd_h_path, z_plane):
        """
        Load TICRA GRD near-field files.

        Args:
            grd_e_path (str): Path to the GRD file containing electric field data
            grd_h_path (str): Path to the GRD file containing magnetic field data
            z_plane (float): Z coordinate of the XY plane

        Returns:
            dict: Combined data dictionary containing:
                - metadata: File metadata and configuration
                - grid_info: Spatial grid information
                - e_fields: Electric field data
                - h_fields: Magnetic field data
                - frequencies: List of frequencies
                - points: Spatial coordinates
        """
        # Load E field file (electric fields)
        self.progress.emit(20)
        data = self.parse_grd_file(grd_e_path, z_plane)

        # Load H field file (magnetic fields)
        self.progress.emit(60)
        data['h_field'] = self.parse_grd_h_file(grd_h_path)

        self.progress.emit(100)
        return data

    @staticmethod
    def parse_grd_file(filepath, z_plane):
        """
        Parse a TICRA GRD file (near-field data).

        Args:
            filepath (str): Path to the GRD file
            z_plane (float): Z coordinate of the XY plane

        Returns:
            dict: Parsed data containing:
                - e_field: Electric field data
                - h_field: Magnetic field data (empty for this format)
                - points: Spatial coordinates
                - grid_info: Spatial grid coordinates and ranges
                - frequency_GHz: Frequency in GHz
                - metadata: File metadata and configuration info
        """
        data = {
            'e_field': array([]),
            'h_field': array([]),
            'points': array([]),
            'grid_info': {
                'x_range': [float('inf'), float('-inf'), 0],
                'y_range': [float('inf'), float('-inf'), 0],
                'z_range': [float('inf'), float('-inf'), 0]
            },
            'frequency_GHz': 0,
            'metadata': {}
        }

        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Parse header information
        header_end = 0
        for i, line in enumerate(lines):
            line = line.strip()

            if line.startswith('VERSION:'):
                data['metadata']['version'] = line.split(':', 1)[1].strip()
            elif 'Field data in' in line:
                data['metadata']['field_type'] = line
            elif 'SOURCE_FIELD_NAME:' in line:
                data['metadata']['source_name'] = line.split(':', 1)[1].strip()
            elif 'FREQUENCY_NAME:' in line:
                data['metadata']['frequency_name'] = line.split(':', 1)[1].strip()
            elif 'FREQUENCIES [GHz]:' in line:
                # Next line should contain the frequency
                if i + 1 < len(lines):
                    freq_line = lines[i + 1].strip()
                    try:
                        freq = float(freq_line)
                        data['frequency_GHz'] = freq
                    except ValueError:
                        pass
            elif line == '++++':
                header_end = i + 1
                break

        if header_end == 0:
            raise ValueError("Could not find header end marker '++++' in file")

        # Parse dataset identifier (always 1)
        dataset_line = lines[header_end].strip()
        dataset_id = int(dataset_line)

        # Parse TICRA format parameters
        # NSET, ICOMP, NCOMP, IGRID
        grid_line = lines[header_end + 1].strip()
        grid_params = grid_line.split()

        if len(grid_params) < 4:
            raise ValueError(f"Invalid grid configuration line: {grid_line}")

        # Extract TICRA parameters
        nset = int(grid_params[0])  # Number of field sets or beams
        icomp = int(grid_params[1])  # Control parameter of field components
        ncomp = int(grid_params[2])  # Number of components
        igrid = int(grid_params[3])  # Control parameter of field grid type

        # Parse offset parameters (to be ignored)
        offset_line = lines[header_end + 2].strip()
        offset_params = offset_line.split()

        # Parse spatial bounds
        bounds_line = lines[header_end + 3].strip()
        bounds = [float(x) for x in bounds_line.split()]

        if len(bounds) < 4:
            raise ValueError(f"Invalid bounds line: {bounds_line}")

        x_min, y_min, x_max, y_max = bounds[:4]

        # Parse grid dimensions
        # NX, NY, KLIMIT
        dims_line = lines[header_end + 4].strip()
        dims = [int(x) for x in dims_line.split()]

        if len(dims) < 3:
            raise ValueError(f"Invalid dimensions line: {dims_line}")

        nx_samples = dims[0]  # Number of columns
        ny_samples = dims[1]  # Number of rows
        klimit = dims[2]  # Specification of limits in a 2D grid
        # =0 Each row contains data for all NX columns
        # =1 Number of data points per row defined in following records

        # Update grid info with actual ranges
        data['grid_info']['x_range'] = [x_min, x_max, nx_samples]
        data['grid_info']['y_range'] = [y_min, y_max, ny_samples]
        data['grid_info']['z_range'] = [z_plane, z_plane, 1]  # Single plane at z_plane

        # Parse field data
        field_data_start = header_end + 5
        field_lines = lines[field_data_start:]

        # Combine all field data lines
        field_text = ' '.join(line.strip() for line in field_lines if line.strip())

        # Parse numeric values
        try:
            values = [float(x) for x in field_text.split()]
        except ValueError as e:
            raise ValueError(f"Error parsing field data: {e}")

        # The data appears to be interleaved real/imaginary pairs for x,y,z components
        # Format: re_x im_x re_y im_y re_z im_z (repeated for each grid point)
        components_per_point = 6  # 3 components × 2 (real/imag)
        expected_total = nx_samples * ny_samples * components_per_point

        if len(values) < expected_total:
            raise ValueError(f"Insufficient field data: expected {expected_total}, got {len(values)}")

        # Reshape data into field components
        field_data = array(values[:expected_total]).reshape(nx_samples * ny_samples, components_per_point)

        # Create complex field array
        e_field = zeros((nx_samples * ny_samples, 3), dtype=complex)
        e_field[:, 0] = field_data[:, 0] + 1j * field_data[:, 1]  # Ex
        e_field[:, 1] = field_data[:, 2] + 1j * field_data[:, 3]  # Ey
        e_field[:, 2] = field_data[:, 4] + 1j * field_data[:, 5]  # Ez

        data['e_field'] = e_field

        # Generate grid coordinates
        x_coords = linspace(x_min, x_max, nx_samples)
        y_coords = linspace(y_min, y_max, ny_samples)

        # Create coordinate grid
        points = zeros((nx_samples * ny_samples, 3))
        idx = 0
        for j in range(ny_samples):
            for i in range(nx_samples):
                points[idx, 0] = x_coords[i]
                points[idx, 1] = y_coords[j]
                points[idx, 2] = z_plane  # Use provided z_plane coordinate
                idx += 1

        data['points'] = points

        # Store grid metadata
        data['metadata'].update({
            'dataset_id': dataset_id,
            'nset': nset,
            'icomp': icomp,
            'ncomp': ncomp,
            'igrid': igrid,
            'nx': nx_samples,
            'ny': ny_samples,
            'klimit': klimit,
            'z_plane': z_plane
        })

        return data

    @staticmethod
    def parse_grd_h_file(filepath):
        """
        Parse a TICRA GRD file for magnetic field data.

        Args:
            filepath (str): Path to the GRD file containing magnetic field data

        Returns:
            numpy.ndarray: Magnetic field data array
        """
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Find header end
        header_end = 0
        for i, line in enumerate(lines):
            if line.strip() == '++++':
                header_end = i + 1
                break

        if header_end == 0:
            raise ValueError("Could not find header end marker '++++' in magnetic field file")

        # Parse dataset identifier (always 1)
        dataset_line = lines[header_end].strip()
        dataset_id = int(dataset_line)

        # Parse TICRA format parameters (same format as E field)
        # NSET, ICOMP, NCOMP, IGRID
        grid_line = lines[header_end + 1].strip()
        grid_params = grid_line.split()

        if len(grid_params) < 4:
            raise ValueError(f"Invalid grid configuration line: {grid_line}")

        # Parse offset parameters (ignored)
        offset_line = lines[header_end + 2].strip()

        # Parse spatial bounds
        bounds_line = lines[header_end + 3].strip()
        bounds = [float(x) for x in bounds_line.split()]

        # Parse grid dimensions
        # NX, NY, KLIMIT
        dims_line = lines[header_end + 4].strip()
        dims = [int(x) for x in dims_line.split()]

        if len(dims) < 3:
            raise ValueError(f"Invalid dimensions line: {dims_line}")

        nx_samples = dims[0]  # Number of columns
        ny_samples = dims[1]  # Number of rows
        klimit = dims[2]  # Specification of limits in a 2D grid

        # Parse magnetic field data
        field_data_start = header_end + 5
        field_lines = lines[field_data_start:]

        # Combine all field data lines
        field_text = ' '.join(line.strip() for line in field_lines if line.strip())

        # Parse numeric values
        try:
            values = [float(x) for x in field_text.split()]
        except ValueError as e:
            raise ValueError(f"Error parsing magnetic field data: {e}")

        # The data appears to be interleaved real/imaginary pairs for x,y,z components
        components_per_point = 6  # 3 components × 2 (real/imag)
        expected_total = nx_samples * ny_samples * components_per_point

        if len(values) < expected_total:
            raise ValueError(f"Insufficient magnetic field data: expected {expected_total}, got {len(values)}")

        # Reshape data into field components
        field_data = array(values[:expected_total]).reshape(nx_samples * ny_samples, components_per_point)

        # Create complex field array
        h_field = zeros((nx_samples * ny_samples, 3), dtype=complex)
        h_field[:, 0] = field_data[:, 0] + 1j * field_data[:, 1]  # Hx
        h_field[:, 1] = field_data[:, 2] + 1j * field_data[:, 3]  # Hy
        h_field[:, 2] = field_data[:, 4] + 1j * field_data[:, 5]  # Hz

        return h_field
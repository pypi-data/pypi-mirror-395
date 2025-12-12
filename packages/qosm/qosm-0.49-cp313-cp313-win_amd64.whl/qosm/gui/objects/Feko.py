from io import StringIO

from PySide6.QtCore import QThread, Signal
from numpy import loadtxt, array, zeros, min, max, stack, unique


class FekoFileLoader(QThread):
    """
    Background thread for loading FEKO near-field files.

    This thread loads and parses FEKO EFE (electric field) and HFE (magnetic field)
    files asynchronously to avoid blocking the UI during file operations.

    Signals:
        progress (int): Emitted during loading with progress percentage (0-100)
        finished_loading (dict): Emitted when loading completes successfully with data
        error_occurred (str): Emitted when an error occurs with error message

    Attributes:
        efe_path (str): Path to the EFE file (electric fields)
        hfe_path (str): Path to the HFE file (magnetic fields)
    """
    progress = Signal(int)
    finished_loading = Signal(dict)
    error_occurred = Signal(str)

    def __init__(self, efe_path, hfe_path):
        """
        Initialize the FEKO file loader.

        Args:
            efe_path (str): Path to the EFE file containing electric field data
            hfe_path (str): Path to the HFE file containing magnetic field data
        """
        super().__init__()
        self.efe_path = efe_path
        self.hfe_path = hfe_path

    def run(self):
        """
        Main thread execution method.

        Loads FEKO files and emits appropriate signals based on success or failure.
        """
        try:
            data = self.load_feko_files(self.efe_path, self.hfe_path)
            self.finished_loading.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def load_feko_files(self, efe_path, hfe_path):
        """
        Load FEKO EFE and HFE near-field files.

        Args:
            efe_path (str): Path to the EFE file
            hfe_path (str): Path to the HFE file

        Returns:
            dict: Combined data dictionary containing:
                - metadata: File metadata and configuration
                - grid_info: Spatial grid information
                - e_fields: Electric field data
                - h_fields: Magnetic field data
                - frequencies: List of frequencies
        """
        # Load EFE file (electric fields)
        self.progress.emit(20)
        data = self.parse_efe_file(efe_path)

        # Load HFE file (magnetic fields)
        self.progress.emit(60)
        data['h_field'] = self.parse_hfe_file(hfe_path)

        self.progress.emit(100)
        return data

    @staticmethod
    def get_file_data(f):
        # Skip header lines (detected via '#')
        data_lines = [line for line in f if
                      not line.strip().startswith('#') and not line.strip().startswith('**') and line.strip()]

        # Parse the numeric data
        data = loadtxt(StringIO("".join(data_lines)))

        # Create structured array for clarity
        dtype = [
            ('x', float), ('y', float), ('z', float),
            ('re_x', float), ('im_x', float),
            ('re_y', float), ('im_y', float),
            ('re_z', float), ('im_z', float)
        ]
        file_data = array([tuple(row) for row in data], dtype=dtype)
        field = zeros((file_data['x'].shape[0], 3), dtype=complex)
        field[:, 0] = file_data['re_x'] + file_data['im_x'] * 1j
        field[:, 1] = file_data['re_y'] + file_data['im_y'] * 1j
        field[:, 2] = file_data['re_z'] + file_data['im_z'] * 1j
        return field, file_data

    @staticmethod
    def parse_efe_file(filepath):
        """
        Parse a FEKO EFE file (Cartesian near-field electric data).

        Args:
            filepath (str): Path to the EFE file

        Returns:
            dict: Parsed data containing:
                - fields: Electric field data indexed by coordinates and frequency
                - grid_info: Spatial grid coordinates and ranges
                - frequencies: List of frequencies found in the file
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
            # Parse field data
            data['e_field'], file_data = FekoFileLoader.get_file_data(f)

            data['points'] = stack([file_data['x'], file_data['y'], file_data['z']], axis=1)

            data['grid_info']['x_range'][0] = min(file_data['x'])
            data['grid_info']['x_range'][1] = max(file_data['x'])
            data['grid_info']['x_range'][2] = unique(file_data['x']).shape[0]
            data['grid_info']['y_range'][0] = min(file_data['y'])
            data['grid_info']['y_range'][1] = max(file_data['y'])
            data['grid_info']['y_range'][2] = unique(file_data['y']).shape[0]
            data['grid_info']['z_range'][0] = min(file_data['z'])
            data['grid_info']['z_range'][1] = max(file_data['z'])
            data['grid_info']['z_range'][2] = unique(file_data['z']).shape[0]

        with open(filepath, 'r') as f:
            lines = f.readlines()

            # Parse header to extract metadata
            for i, line in enumerate(lines):
                if line.startswith('#'):
                    # Extract header information
                    if 'frequency' in line.lower():
                        # Search for frequency in the line
                        part = line.split()[1]
                        try:
                            freq = float(part)
                            if freq > 1e9:  # Probably in Hz
                                freq = freq / 1e9  # Convert to GHz
                            data['frequency_GHz'] = freq
                            break
                        except ValueError:
                            continue
                    elif 'Request' in line or 'Configuration' in line:
                        data['metadata']['configuration'] = line.split('#')[-1].strip()
                    elif 'Units' in line:
                        data['metadata']['units'] = line.split('#')[-1].strip()
                    elif 'no. of' in line.lower():
                        parts = line.split('Samples:')
                        if len(parts) == 2:
                            dim = parts[0].split()[-1].replace(' ', '')
                            num = float(parts[1].replace(' ', ''))
                            if dim.lower() == 'x':
                                data['grid_info']['x_range'][2] = num
                            elif dim.lower() == 'y':
                                data['grid_info']['y_range'][2] = num
                            elif dim.lower() == 'z':
                                data['grid_info']['z_range'][2] = num

            data['metadata']['source_name'] = data['metadata']['configuration'].replace('Request Name:', '').replace(' ', '')
        return data

    @staticmethod
    def parse_hfe_file(filepath):
        """
        Parse a FEKO HFE file (near-field magnetic data).

        Args:
            filepath (str): Path to the HFE file

        Returns:
            dict: Parsed magnetic field data with structure:
                - fields: Magnetic field data indexed by coordinates and frequency
        """
        data = array([])

        with open(filepath, 'r') as f:
            data, _ = FekoFileLoader.get_file_data(f)

        return data

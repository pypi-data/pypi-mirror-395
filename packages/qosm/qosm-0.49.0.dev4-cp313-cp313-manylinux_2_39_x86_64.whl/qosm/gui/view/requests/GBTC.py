import numpy as np
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox,
                               QPushButton, QGridLayout, QGroupBox, QSizePolicy, QFileDialog, QMessageBox, QDialog,
                               QDoubleSpinBox, QProgressDialog, QCheckBox)
from PySide6.QtCore import Qt, Signal
import matplotlib
from qosm.gui.objects import HDF5Exporter
import skrf as rf

matplotlib.use('Agg')  # Force Agg backend before any other matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os


def moving_average(data, half_window_size, full_length: bool = False):
    """
    Calculate moving average of a data series using convolution.

    Applies a uniform window to smooth noisy data while preserving
    the overall trend characteristics.

    Parameters
    ----------
    data : array_like
        Input data series to be smoothed.
    half_window_size : int
        Half-size of the moving average window. Must be positive integer.
    full_length : bool
        Return an array of the same dimension than data if True (padding with NaN)

    Returns
    -------
    ndarray
        Smoothed data series with length (len(data) - window_size + 1).

    Notes
    -----
    - Uses numpy.convolve with 'valid' mode for computation
    - Output length is reduced by (window_size - 1) points
    - All window weights are equal (uniform averaging)
    """
    i_start = half_window_size
    i_end = len(data) - half_window_size

    moving_avg = np.zeros_like(data, dtype=complex) * (np.nan + 0j * np.nan)
    for i in range(i_start, i_end):
        moving_avg[i] = np.mean(data[i - half_window_size:i + half_window_size])

    if not full_length:
        moving_avg = moving_avg[i_start:i_end]
    return moving_avg


def filter_s2p(s2p: rf.Network | str, half_window_size):
    """
    Apply moving average filter to S-parameter data.

    Smooths all four S-parameters of a 2-port network using moving average
    filtering to reduce measurement noise while preserving spectral features.

    Parameters
    ----------
    s2p : skrf.Network or str
        Input S-parameter data as Network object or filepath to S2P file.
    half_window_size : int
        Moving average window size. If < 1, no filtering is applied.

    Returns
    -------
    skrf.Network
        Filtered S-parameter network with same frequency grid as input.
        Unfiltered regions are filled with NaN values.

    Notes
    -----
    - Filtering reduces valid data range by (window_size - 1) points
    - Edge regions are set to NaN to maintain frequency grid consistency
    - All four S-parameters (S11, S12, S21, S22) are filtered identically
    """
    if isinstance(s2p, str):
        s_file = rf.Network(s2p)
        frequencies_GHz = s_file.f * 1e-9
    else:
        s_file = s2p
        frequencies_GHz = s_file.f * 1e-9

    if half_window_size < 1:
        return s_file

    # Initialize with NaN and fill filtered regions
    S = np.zeros((frequencies_GHz.shape[0], 2, 2), dtype=complex) * (np.nan + 0j * np.nan)
    S[:, 0, 0] = moving_average(s_file.s[:, 0, 0], half_window_size, full_length=True)
    S[:, 0, 1] = moving_average(s_file.s[:, 0, 1], half_window_size, full_length=True)
    S[:, 1, 0] = moving_average(s_file.s[:, 1, 0], half_window_size, full_length=True)
    S[:, 1, 1] = moving_average(s_file.s[:, 1, 1], half_window_size, full_length=True)

    return rf.Network(s=S, f=frequencies_GHz, f_unit='GHz')


class GBTCCanvas(FigureCanvas):
    """Integrated matplotlib canvas for displaying GBTC S-parameters in 2x2 grid"""

    def __init__(self, parent=None):
        self.figure = Figure(figsize=(12, 10))
        super().__init__(self.figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # Store current plot data for export
        self.current_plot_data = None
        self.current_plot_info = None

    def plot_s_parameters(self, data_dict, show_gbtc=True, show_pw=True, show_port1=True, show_port2=True,
                          show_s2p=False, s2p_network=None, s2p_filename=None, s2p_filter_size=0, iteration=0,
                          iteration_info=None):
        """
        Display S-parameters in 2x2 grid layout:
        [0,0]: mag S11 et S22 (reflection)
        [0,1]: phase S11 et S22 (reflection)
        [1,0]: mag S12 et S21 (transmission)
        [1,1]: phase S12 et S21 (transmission)

        Args:
            data_dict: Dictionary containing GBTC simulation results
            show_gbtc: bool, whether to show GBTC results
            show_pw: bool, whether to show PW results
            show_port1: bool, whether to show port 1 parameters (S11, S21)
            show_port2: bool, whether to show port 2 parameters (S22, S12)
            show_s2p: bool, whether to show S2P file data
            s2p_network: skrf.Network object for S2P data
            s2p_filename: string, name of the S2P file for legend
            s2p_filter_size: int, half window size for moving average filter (0 = no filtering)
            iteration: int, which iteration to display (0-based index)
            iteration_info: str, formatted iteration information for title
        """
        # Clear figure
        self.figure.clear()

        # Get data
        gbtc_data = data_dict['data']
        sweep_frequency_values = data_dict.get('sweep_frequency_values', [])
        compare_plane_wave = data_dict.get('compare_plane_wave', False)

        has_gbtc_data = gbtc_data and len(sweep_frequency_values) > 0
        has_s2p_data = show_s2p and s2p_network is not None

        if not has_gbtc_data and not has_s2p_data:
            # No data to plot
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available for plotting',
                    ha='center', va='center', transform=ax.transAxes, fontsize=16)
            self.draw()
            return

        # Check what parameters to plot
        if not show_port1 and not show_port2:
            # No parameters selected
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No S-parameters selected for display',
                    ha='center', va='center', transform=ax.transAxes, fontsize=16)
            self.draw()
            return

        # Create 2x2 subplot grid
        ax_r_mag = self.figure.add_subplot(2, 2, 1)  # [0,0]: Reflection magnitude
        ax_r_phase = self.figure.add_subplot(2, 2, 2)  # [0,1]: Reflection phase
        ax_t_mag = self.figure.add_subplot(2, 2, 3)  # [1,0]: Transmission magnitude
        ax_t_phase = self.figure.add_subplot(2, 2, 4)  # [1,1]: Transmission phase

        # Plot colors and line styles
        colors = {
            'gbtc': {'S11': 'dodgerblue', 'S12': 'dodgerblue', 'S21': 'darkorange', 'S22': 'darkorange'},
            'pw': {'S11': 'crimson', 'S12': 'crimson', 'S21': 'darkcyan', 'S22': 'darkcyan'},
            's2p': {'S11': 'mediumorchid', 'S12': 'mediumorchid', 'S21': 'indigo', 'S22': 'indigo'},
        }
        line_styles = {'gbtc': '-', 'pw': '-', 's2p': '--'}

        # X-axis is always frequency
        x_values = np.array(sweep_frequency_values) if has_gbtc_data else None
        x_label = 'Frequency (GHz)'

        # Track what gets plotted for legend management
        plotted_items = {'r_mag': [], 'r_phase': [], 't_mag': [], 't_phase': []}

        # Plot GBTC and PW data
        if has_gbtc_data:
            for method in ['gbtc', 'pw']:
                if method == 'gbtc' and not show_gbtc:
                    continue
                if method == 'pw' and (not show_pw or not compare_plane_wave):
                    continue

                method_data = gbtc_data.get(method, {})
                if not method_data:
                    continue

                # Define parameter mapping
                param_mapping = {
                    'reflection': ['S11', 'S22'],
                    'transmission': ['S12', 'S21']
                }

                for param_type in ['reflection', 'transmission']:
                    if (param_type == 'reflection' and not show_port1 and not show_port2) or \
                            (param_type == 'transmission' and not show_port1 and not show_port2):
                        continue

                    for param in param_mapping[param_type]:
                        # Check if this parameter should be shown based on port selection
                        if param in ['S11', 'S21'] and not show_port1:
                            continue
                        if param in ['S22', 'S12'] and not show_port2:
                            continue
                        param_data = method_data.get(param, [])
                        if len(param_data) == 0:
                            print(f"Warning: No data for {method} {param}")
                            continue

                        # Convert to numpy array
                        param_array = np.array(param_data)

                        # Handle different data formats: KxN (iterations) or Nx1 (legacy)
                        if param_array.ndim == 2:
                            # New format: KxN where K is number of iterations
                            num_iterations, num_points = param_array.shape

                            # Check if requested iteration exists
                            if iteration >= num_iterations:
                                print(f"Warning: Iteration {iteration} not available for {method} {param}. "
                                      f"Available iterations: 0-{num_iterations - 1}. Using iteration 0.")
                                iteration_to_use = 0
                            else:
                                iteration_to_use = iteration

                            # Extract data for the specific iteration
                            param_iteration_data = param_array[iteration_to_use, :]

                        elif param_array.ndim == 1:
                            # Legacy format: Nx1 - treat as single iteration
                            param_iteration_data = param_array
                            if iteration > 0:
                                print(f"Warning: Only one iteration available for {method} {param}, "
                                      f"but iteration {iteration} was requested.")
                        else:
                            print(f"Error: Unexpected data format for {method} {param}")
                            continue

                        # Find valid (non-NaN and significant) indices
                        valid_mask = ~(np.isnan(param_iteration_data.real) | np.isnan(param_iteration_data.imag))
                        # Only plot if abs(parameter) > 1e-9
                        significant_mask = np.abs(param_iteration_data) > 1e-9
                        plot_mask = valid_mask & significant_mask

                        if not np.any(plot_mask):
                            continue  # All values are NaN or too small

                        x_valid = x_values[plot_mask]
                        param_valid = param_iteration_data[plot_mask]

                        # Calculate magnitude and phase
                        magnitude_db = 20 * np.log10(np.abs(param_valid))
                        phase_deg = np.angle(param_valid, deg=True)

                        # Plot parameters
                        color = colors[method][param]
                        linestyle = line_styles[method]
                        label = f'{param} ({method.upper()})'

                        # Select appropriate axes based on parameter type
                        if param_type == 'reflection':
                            # Plot on reflection axes
                            ax_r_mag.plot(x_valid, magnitude_db, color=color, linestyle=linestyle,
                                          linewidth=2, label=label)
                            ax_r_phase.plot(x_valid, phase_deg, color=color, linestyle=linestyle,
                                            linewidth=2, label=label)
                            plotted_items['r_mag'].append(label)
                            plotted_items['r_phase'].append(label)
                        else:  # transmission
                            # Plot on transmission axes
                            ax_t_mag.plot(x_valid, magnitude_db, color=color, linestyle=linestyle,
                                          linewidth=2, label=label)
                            ax_t_phase.plot(x_valid, phase_deg, color=color, linestyle=linestyle,
                                            linewidth=2, label=label)
                            plotted_items['t_mag'].append(label)
                            plotted_items['t_phase'].append(label)

        # Plot S2P data
        if has_s2p_data:
            # Apply filtering if requested
            if s2p_filter_size > 0:
                s2p_network_filtered = filter_s2p(s2p_network, s2p_filter_size)
            else:
                s2p_network_filtered = s2p_network

            # Get frequency data from S2P file (convert to GHz if needed)
            s2p_freq = s2p_network_filtered.frequency.f
            if np.max(s2p_freq) > 1e6:  # Assume Hz, convert to GHz
                s2p_freq_ghz = s2p_freq / 1e9
            else:  # Assume already in GHz
                s2p_freq_ghz = s2p_freq

            # Create legend label - always use "s2p" without filename or filter info
            short_name = "s2p"

            # Parameter mapping for S2P
            s2p_param_mapping = {
                'reflection': [('S11', 0, 0), ('S22', 1, 1)],
                'transmission': [('S12', 0, 1), ('S21', 1, 0)]
            }

            for param_type in ['reflection', 'transmission']:
                if (param_type == 'reflection' and not show_port1 and not show_port2) or \
                        (param_type == 'transmission' and not show_port1 and not show_port2):
                    continue

                for param_name, i, j in s2p_param_mapping[param_type]:
                    # Check if this parameter should be shown based on port selection
                    if param_name in ['S11', 'S21'] and not show_port1:
                        continue
                    if param_name in ['S22', 'S12'] and not show_port2:
                        continue
                    if s2p_network_filtered.number_of_ports < max(i + 1, j + 1):
                        continue  # Parameter not available

                    s_param_data = s2p_network_filtered.s[:, i, j]

                    # Only plot if abs(parameter) > 1e-9
                    significant_mask = np.abs(s_param_data) > 1e-9
                    if not np.any(significant_mask):
                        continue

                    s2p_freq_valid = s2p_freq_ghz[significant_mask]
                    s_param_valid = s_param_data[significant_mask]

                    # Calculate magnitude and phase
                    magnitude_db = 20 * np.log10(np.abs(s_param_valid))
                    phase_deg = np.angle(s_param_valid, deg=True)

                    # Plot parameters
                    color = colors['s2p'][param_name]
                    linestyle = line_styles['s2p']
                    label = f'{param_name} ({short_name})'

                    # Select appropriate axes based on parameter type
                    if param_type == 'reflection':
                        ax_r_mag.plot(s2p_freq_valid, magnitude_db, color=color, linestyle=linestyle,
                                      linewidth=2, label=label)
                        ax_r_phase.plot(s2p_freq_valid, phase_deg, color=color, linestyle=linestyle,
                                        linewidth=2, label=label)
                        plotted_items['r_mag'].append(label)
                        plotted_items['r_phase'].append(label)
                    else:  # transmission
                        ax_t_mag.plot(s2p_freq_valid, magnitude_db, color=color, linestyle=linestyle,
                                      linewidth=2, label=label)
                        ax_t_phase.plot(s2p_freq_valid, phase_deg, color=color, linestyle=linestyle,
                                        linewidth=2, label=label)
                        plotted_items['t_mag'].append(label)
                        plotted_items['t_phase'].append(label)

        # Format subplots
        # Reflection magnitude [0,0]
        if (show_port1 or show_port2) and plotted_items['r_mag']:
            ax_r_mag.set_ylabel('Magnitude (dB)')
            ax_r_mag.set_title('Reflection - Magnitude (S11, S22)')
            ax_r_mag.grid(True, alpha=0.3)
            ax_r_mag.legend(loc='upper right')
        else:
            ax_r_mag.set_title('Reflection - Magnitude')
            ax_r_mag.text(0.5, 0.5, 'No reflection data', ha='center', va='center',
                          transform=ax_r_mag.transAxes, fontsize=12)

        # Reflection phase [0,1]
        if (show_port1 or show_port2) and plotted_items['r_phase']:
            ax_r_phase.set_ylabel('Phase (degrees)')
            ax_r_phase.set_title('Reflection - Phase (S11, S22)')
            ax_r_phase.grid(True, alpha=0.3)
            ax_r_phase.legend(loc='upper right')
        else:
            ax_r_phase.set_title('Reflection - Phase')
            ax_r_phase.text(0.5, 0.5, 'No reflection data', ha='center', va='center',
                            transform=ax_r_phase.transAxes, fontsize=12)

        # Transmission magnitude [1,0]
        if (show_port1 or show_port2) and plotted_items['t_mag']:
            ax_t_mag.set_xlabel(x_label)
            ax_t_mag.set_ylabel('Magnitude (dB)')
            ax_t_mag.set_title('Transmission - Magnitude (S12, S21)')
            ax_t_mag.grid(True, alpha=0.3)
            ax_t_mag.legend(loc='upper right')
        else:
            ax_t_mag.set_xlabel(x_label)
            ax_t_mag.set_title('Transmission - Magnitude')
            ax_t_mag.text(0.5, 0.5, 'No transmission data', ha='center', va='center',
                          transform=ax_t_mag.transAxes, fontsize=12)

        # Transmission phase [1,1]
        if (show_port1 or show_port2) and plotted_items['t_phase']:
            ax_t_phase.set_xlabel(x_label)
            ax_t_phase.set_ylabel('Phase (degrees)')
            ax_t_phase.set_title('Transmission - Phase (S12, S21)')
            ax_t_phase.grid(True, alpha=0.3)
            ax_t_phase.legend(loc='upper right')
        else:
            ax_t_phase.set_xlabel(x_label)
            ax_t_phase.set_title('Transmission - Phase')
            ax_t_phase.text(0.5, 0.5, 'No transmission data', ha='center', va='center',
                            transform=ax_t_phase.transAxes, fontsize=12)

        # Create main title with iteration information
        title_parts = []
        if has_gbtc_data and iteration_info:
            title_parts.append(iteration_info)
        if has_s2p_data and s2p_filename:
            short_name = os.path.splitext(os.path.basename(s2p_filename))[0]
            title_parts.append(f"S2P: {short_name}")

        if title_parts:
            title = f'S-Parameters - {" | ".join(title_parts)}'
        else:
            title = 'S-Parameters'

        self.figure.suptitle(title, fontsize=14, y=0.95)

        # Adjust layout
        self.figure.tight_layout(rect=[0, 0, 1, 0.93])

        # Store current plot data for export
        export_title = f'S-Parameters'
        if has_gbtc_data:
            export_title += f' - {data_dict.get("req_name", "Simulation")}'
        if iteration_info:
            export_title += f' - {iteration_info}'
        if has_s2p_data and s2p_filename:
            short_name = os.path.splitext(os.path.basename(s2p_filename))[0]
            export_title += f' - S2P: {short_name}'

        self.current_plot_data = {
            'x_values': x_values,
            'x_label': x_label,
            'gbtc_data': gbtc_data.get('gbtc', {}) if has_gbtc_data else {},
            'pw_data': gbtc_data.get('pw', {}) if has_gbtc_data else {},
            'show_gbtc': show_gbtc,
            'show_pw': show_pw,
            'show_port1': show_port1,
            'show_port2': show_port2,
            'show_s2p': show_s2p,
            's2p_network': s2p_network,
            's2p_filename': s2p_filename,
            's2p_filter_size': s2p_filter_size,
            'iteration': iteration,
            'iteration_info': iteration_info,
            'title': export_title,
            'compare_plane_wave': compare_plane_wave
        }

        # Update canvas
        self.draw()

    def export_image(self, filename, dpi=300, bbox_inches='tight'):
        """Export current plot to image file"""
        if self.current_plot_data is None:
            raise ValueError("No plot data available for export")

        try:
            self.figure.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    def export_high_quality_image(self, filename, figsize=(12, 10), dpi=300):
        """Export current figure in high resolution"""
        if self.current_plot_data is None:
            raise ValueError("No plot data available for export")

        try:
            # Simply export the current figure with high DPI
            # Temporarily adjust figure size if needed
            original_size = self.figure.get_size_inches()
            self.figure.set_size_inches(figsize)

            # Save with high DPI
            self.figure.savefig(filename, dpi=dpi, bbox_inches='tight')

            # Restore original size
            self.figure.set_size_inches(original_size)
            self.draw()  # Refresh the display

            return True

        except Exception as e:
            print(f"Error saving high-quality image: {e}")
            return False


class GBTCViewer(QWidget):
    """Main widget for visualizing GBTC S-parameter results"""

    # Signal emitted when a new view is requested
    new_view_requested = Signal(dict)

    def __init__(self, available_requests, selected_request=None, view_id=1, parent=None):
        super().__init__(parent)
        self.request = available_requests.get('GBTCSim', {})
        self.view_id = view_id

        # Display options
        self.show_gbtc = True
        self.show_pw = True
        self.show_port1 = True  # S11, S21
        self.show_port2 = True  # S22, S12

        # S2P file options
        self.show_s2p = False
        self.s2p_network = None
        self.s2p_filename = None
        self.s2p_filter_size = 0

        # Iteration control
        self.current_iteration = 0
        self.max_iterations = self._get_max_iterations()

        self.setup_ui()
        self.update_display()

    def _get_max_iterations(self):
        """Determine the maximum number of iterations available in the data"""
        max_iter = 1  # Default to 1 iteration (legacy format)

        try:
            gbtc_data = self.request.get('data', {})

            for method in ['gbtc', 'pw']:
                method_data = gbtc_data.get(method, {})
                if not method_data:
                    continue

                for param in ['S11', 'S12', 'S21', 'S22']:
                    param_data = method_data.get(param, [])
                    if len(param_data) == 0:
                        continue

                    param_array = np.array(param_data)
                    if param_array.ndim == 2:
                        # KxN format: K iterations, N frequency points
                        num_iterations = param_array.shape[0]
                        max_iter = max(max_iter, num_iterations)

        except Exception as e:
            print(f"Error determining max iterations: {e}")

        return max_iter

    def _get_iteration_info(self, iteration):
        """Get iteration parameter information for display in title

        Args:
            iteration: Current iteration index

        Returns:
            str: Formatted string with parameter name and value, or None if not available
        """
        try:
            # Get sweep information from self.request
            sweep_values = self.request.get('sweep_values', [])
            sweep_parameter = self.request.get('sweep_attribute', '')
            sweep_target_name = self.request.get('sweep_target_name', '')

            # Convert to numpy array if it isn't already, and handle empty cases
            if sweep_values is not None:
                sweep_values = np.array(sweep_values)

            # Check if we have valid data
            if (sweep_values is not None and
                    len(sweep_values) > 0 and
                    sweep_parameter and
                    len(sweep_values) > iteration):

                param_value = sweep_values[iteration]

                # Format the value appropriately
                if isinstance(param_value, (int, float, np.integer, np.floating)):
                    if param_value == int(param_value):
                        value_str = f"{int(param_value)}"
                    else:
                        # Use appropriate precision based on magnitude
                        if abs(param_value) >= 1000:
                            value_str = f"{param_value:.0f}"
                        elif abs(param_value) >= 100:
                            value_str = f"{param_value:.1f}"
                        elif abs(param_value) >= 10:
                            value_str = f"{param_value:.2f}"
                        else:
                            value_str = f"{param_value:.3f}"
                else:
                    value_str = str(param_value)

                # Determine unit based on parameter name
                unit = ""
                if sweep_parameter in ['pose.x', 'pose.y', 'pose.z']:
                    unit = "mm"
                elif sweep_parameter in ['pose.rx', 'pose.ry', 'pose.rz']:
                    unit = "deg"

                # Format as "{parameter}: {value} {unit}"
                if unit:
                    return f"{sweep_target_name} → {sweep_parameter}: {value_str} {unit}"
                else:
                    return f"{sweep_target_name} → {sweep_parameter}: {value_str}"

            # Check if there are multiple iterations
            if self.max_iterations > 1:
                return f"Iteration {iteration}"
            else:
                # Single iteration case - don't show iteration info
                return None

        except Exception as e:
            print(f"Error getting iteration info: {e}")
            print(f"sweep_values type: {type(self.request.get('sweep_values', []))}")
            print(f"sweep_values content: {self.request.get('sweep_values', [])}")
            print(f"sweep_parameter: {self.request.get('sweep_parameter', '')}")
            return f"Iteration {iteration}"

    def load_s2p_file(self):
        """Load S2P file using file dialog"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load S2P File",
            "",
            "S2P Files (*.s2p);;All Files (*)"
        )

        if filename:
            try:
                # Load the S2P file using scikit-rf
                network = rf.Network(filename)

                # Store the network and filename
                self.s2p_network = network
                self.s2p_filename = filename

                # Update the checkbox and button text
                short_name = os.path.splitext(os.path.basename(filename))[0]
                if len(short_name) > 20:
                    short_name = short_name[:17] + "..."

                self.s2p_checkbox.setText(f"S2P: {short_name}")
                self.s2p_checkbox.setEnabled(True)
                self.s2p_checkbox.setChecked(True)
                self.show_s2p = True

                # Update display
                self.update_display()

            except Exception as e:
                QMessageBox.critical(self, "Error Loading S2P File",
                                     f"Failed to load S2P file:\n{str(e)}")
                self.clear_s2p_data()

    def clear_s2p_data(self):
        """Clear loaded S2P data"""
        self.s2p_network = None
        self.s2p_filename = None
        self.show_s2p = False
        self.s2p_checkbox.setText("S2P File")
        self.s2p_checkbox.setChecked(False)
        self.s2p_checkbox.setEnabled(False)
        self.update_display()

    def export_s2p_current_iteration(self):
        """Export current iteration GBTC data as S2P (Touchstone) file"""
        try:
            # Get current data
            data_dict = self.request
            gbtc_data = data_dict.get('data', {})
            sweep_frequency_values = data_dict.get('sweep_frequency_values', [])

            if not gbtc_data or len(sweep_frequency_values) == 0:
                QMessageBox.warning(self, "Export Error", "No GBTC data available to export.")
                return

            # Get frequencies (assume they are in GHz)
            frequencies = np.array(sweep_frequency_values)

            # Initialize S-parameter matrix for current iteration
            num_freqs = len(frequencies)
            S_matrix = np.zeros((num_freqs, 2, 2), dtype=complex)

            # Extract S-parameters for current iteration
            method = 'gbtc'  # Export GBTC data by default
            method_data = gbtc_data.get(method, {})

            if not method_data:
                QMessageBox.warning(self, "Export Error", f"No {method.upper()} data available to export.")
                return

            # Parameter mapping: S[i,j] where i=row, j=col (0-indexed)
            s_params = ['S11', 'S12', 'S21', 'S22']
            s_indices = [(0, 0), (0, 1), (1, 0), (1, 1)]

            all_data_available = True
            for param, (i, j) in zip(s_params, s_indices):
                param_data = method_data.get(param, [])
                if len(param_data) == 0:
                    print(f"Warning: No data for {param}")
                    all_data_available = False
                    continue

                # Convert to numpy array and handle iteration
                param_array = np.array(param_data)

                if param_array.ndim == 2:
                    # KxN format: K iterations, N frequency points
                    num_iterations, num_points = param_array.shape
                    if self.current_iteration >= num_iterations:
                        iteration_to_use = 0
                        print(f"Warning: Using iteration 0 instead of {self.current_iteration} for {param}")
                    else:
                        iteration_to_use = self.current_iteration

                    param_iteration_data = param_array[iteration_to_use, :]

                elif param_array.ndim == 1:
                    # Legacy format: single iteration
                    param_iteration_data = param_array
                    if self.current_iteration > 0:
                        print(f"Warning: Only one iteration available for {param}")
                else:
                    print(f"Error: Unexpected data format for {param}")
                    all_data_available = False
                    continue

                # Check data length matches frequency array
                if len(param_iteration_data) != num_freqs:
                    print(f"Warning: Data length mismatch for {param}: {len(param_iteration_data)} vs {num_freqs}")
                    # Truncate or pad as needed
                    if len(param_iteration_data) < num_freqs:
                        # Pad with NaN
                        padded_data = np.full(num_freqs, np.nan + 1j * np.nan, dtype=complex)
                        padded_data[:len(param_iteration_data)] = param_iteration_data
                        param_iteration_data = padded_data
                    else:
                        # Truncate
                        param_iteration_data = param_iteration_data[:num_freqs]

                # Store in S-matrix
                S_matrix[:, i, j] = param_iteration_data

            if not all_data_available:
                response = QMessageBox.question(
                    self, "Incomplete Data",
                    "Some S-parameters are missing. Do you want to export with available data?\n"
                    "Missing parameters will be filled with zeros.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if response == QMessageBox.StandardButton.No:
                    return

            # Create scikit-rf Network object
            # Convert frequencies to Hz (scikit-rf expects Hz by default)
            freq_hz = frequencies * 1e9  # Convert GHz to Hz

            try:
                network = rf.Network(s=S_matrix, f=freq_hz, f_unit='Hz')
            except Exception as e:
                QMessageBox.critical(self, "Export Error",
                                     f"Failed to create network object:\n{str(e)}")
                return

            # Generate suggested filename
            req_name = str(data_dict.get('req_name', 'gbtc_sim'))
            clean_name = "".join(c for c in req_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_name = clean_name.replace(' ', '_')

            # Add iteration info to filename
            iteration_info = self._get_iteration_info(self.current_iteration)
            if iteration_info is not None and 'Iteration' not in iteration_info:
                # Extract parameter value for filename
                if '→' in iteration_info and ':' in iteration_info:
                    param_part = iteration_info.split('→')[1].strip()
                    param_name = param_part.split(':')[0].strip().replace('.', '_')
                    param_value = param_part.split(':')[1].strip().split()[0]  # Remove unit
                    iter_suffix = f"_{param_name}_{param_value}"
                else:
                    iter_suffix = f"_iter{self.current_iteration}"
            else:
                iter_suffix = f"_iter{self.current_iteration}"

            suggested_filename = f"{clean_name}{iter_suffix}_gbtc.s2p"

            # Open file dialog
            filename, selected_filter = QFileDialog.getSaveFileName(
                self,
                "Export S-Parameters as S2P (Touchstone)",
                suggested_filename,
                "S2P Files (*.s2p);;All Files (*)"
            )

            if filename:
                try:
                    # Ensure .s2p extension
                    if not filename.lower().endswith('.s2p'):
                        filename += '.s2p'

                    # Write S2P file
                    network.write_touchstone(filename)

                    QMessageBox.information(
                        self, "Export Successful",
                        f"S-parameters exported successfully to:\n{filename}\n\n"
                        f"Method: {method.upper()}\n"
                        f"Iteration: {self.current_iteration}\n"
                        f"Frequency points: {len(frequencies)}\n"
                        f"Frequency range: {frequencies[0]:.3f} - {frequencies[-1]:.3f} GHz"
                    )

                except Exception as e:
                    QMessageBox.critical(self, "Export Error",
                                         f"Failed to write S2P file:\n{str(e)}")

        except Exception as e:
            QMessageBox.critical(self, "Export Error",
                                 f"An error occurred during S2P export:\n{str(e)}")

    def setup_ui(self):
        """User interface setup"""
        layout = QVBoxLayout(self)

        # Request selection
        request_group = QGroupBox("Request Selection")
        request_layout = QGridLayout(request_group)

        request_layout.addWidget(QLabel("Request:"), 0, 0)
        request_label = QLabel('GBTC Simulation')
        request_layout.addWidget(request_label, 0, 1)

        layout.addWidget(request_group)

        # S2P File controls
        s2p_group = QGroupBox("S2P File")
        s2p_layout = QHBoxLayout(s2p_group)

        # Left column: Load and Clear buttons
        left_layout = QHBoxLayout()

        # Load S2P button
        self.load_s2p_button = QPushButton("Load S2P File")
        self.load_s2p_button.setToolTip("Load Touchstone S2P file for comparison")
        self.load_s2p_button.clicked.connect(self.load_s2p_file)
        left_layout.addWidget(self.load_s2p_button)

        # Clear S2P button
        self.clear_s2p_button = QPushButton("Clear S2P")
        self.clear_s2p_button.setToolTip("Clear loaded S2P file")
        self.clear_s2p_button.clicked.connect(self.clear_s2p_data)
        left_layout.addWidget(self.clear_s2p_button)

        # S2P checkbox
        self.s2p_checkbox = QCheckBox("S2P File")
        self.s2p_checkbox.setEnabled(False)
        self.s2p_checkbox.setChecked(False)
        self.s2p_checkbox.toggled.connect(self.on_s2p_toggled)
        left_layout.addWidget(self.s2p_checkbox)

        s2p_layout.addLayout(left_layout)
        s2p_layout.addStretch()

        # Right column: Filter controls
        right_layout = QHBoxLayout()
        right_layout.addWidget(QLabel("Filter:"))

        self.filter_spinbox = QSpinBox()
        self.filter_spinbox.setMinimum(0)
        self.filter_spinbox.setMaximum(100)
        self.filter_spinbox.setValue(0)
        self.filter_spinbox.setSuffix(" pts")
        self.filter_spinbox.setToolTip("Half window size for moving average filter\n0 = no filtering")
        self.filter_spinbox.valueChanged.connect(self.on_filter_changed)
        right_layout.addWidget(self.filter_spinbox)

        s2p_layout.addLayout(right_layout)
        layout.addWidget(s2p_group)

        # Display controls
        controls_group = QGroupBox("Display Controls")
        controls_layout = QHBoxLayout(controls_group)

        # Iteration control
        controls_layout.addWidget(QLabel("Iteration:"))

        self.iteration_spinbox = QSpinBox()
        self.iteration_spinbox.setMinimum(0)
        self.iteration_spinbox.setMaximum(max(0, self.max_iterations - 1))
        self.iteration_spinbox.setValue(self.current_iteration)

        # Update tooltip with parameter info if available
        tooltip_text = f"Select iteration (0 to {self.max_iterations - 1})"
        sweep_attribute = self.request.get('sweep_attribute', '')
        if sweep_attribute:
            tooltip_text += f"\nParameter: {sweep_attribute}"
        self.iteration_spinbox.setToolTip(tooltip_text)

        self.iteration_spinbox.valueChanged.connect(self.on_iteration_changed)
        controls_layout.addWidget(self.iteration_spinbox)

        # Iteration info label
        self.iteration_info_label = QLabel(f"/ {self.max_iterations - 1}")
        controls_layout.addWidget(self.iteration_info_label)

        # Add some spacing
        controls_layout.addStretch()

        # Method selection checkboxes
        controls_layout.addWidget(QLabel("Methods:"))

        self.gbtc_checkbox = QCheckBox("GBTC")
        self.gbtc_checkbox.setChecked(self.show_gbtc)
        self.gbtc_checkbox.toggled.connect(self.on_gbtc_toggled)
        controls_layout.addWidget(self.gbtc_checkbox)

        self.pw_checkbox = QCheckBox("PW")
        self.pw_checkbox.setChecked(self.show_pw)
        self.pw_checkbox.toggled.connect(self.on_pw_toggled)
        controls_layout.addWidget(self.pw_checkbox)

        # Spacing
        controls_layout.addStretch()

        # Parameter selection checkboxes - Changed to Port 1/Port 2
        controls_layout.addWidget(QLabel("Parameters:"))

        self.port1_checkbox = QCheckBox("Port 1")
        self.port1_checkbox.setToolTip("Port 1 parameters (S11, S21)")
        self.port1_checkbox.setChecked(self.show_port1)
        self.port1_checkbox.toggled.connect(self.on_port1_toggled)
        controls_layout.addWidget(self.port1_checkbox)

        self.port2_checkbox = QCheckBox("Port 2")
        self.port2_checkbox.setToolTip("Port 2 parameters (S22, S12)")
        self.port2_checkbox.setChecked(self.show_port2)
        self.port2_checkbox.toggled.connect(self.on_port2_toggled)
        controls_layout.addWidget(self.port2_checkbox)

        # Spacing
        controls_layout.addStretch()

        # Export buttons
        export_layout = QHBoxLayout()

        self.export_button = QPushButton("Export Image")
        self.export_button.setToolTip("Export current plot as image")
        self.export_button.clicked.connect(self.export_current_plot)
        export_layout.addWidget(self.export_button)

        # Export S2P button
        self.export_s2p_button = QPushButton("Export S2P")
        self.export_s2p_button.setToolTip("Export current iteration GBTC data as S2P (Touchstone) file")
        self.export_s2p_button.clicked.connect(self.export_s2p_current_iteration)
        export_layout.addWidget(self.export_s2p_button)

        # Export HDF5 button
        self.export_hdf5_button = QPushButton("Export HDF5")
        self.export_hdf5_button.setToolTip("Export current request data to HDF5 format")
        self.export_hdf5_button.clicked.connect(self.export_hdf5_data)
        export_layout.addWidget(self.export_hdf5_button)

        controls_layout.addLayout(export_layout)
        layout.addWidget(controls_group)

        # Canvas for display
        self.canvas = GBTCCanvas(self)
        layout.addWidget(self.canvas)

        # Initialize HDF5 exporter
        self.hdf5_exporter = HDF5Exporter(self)

    def on_iteration_changed(self, value):
        """Callback for iteration spinbox change"""
        self.current_iteration = value
        self.update_display()

    def on_gbtc_toggled(self, checked):
        """Callback for GBTC checkbox toggle"""
        self.show_gbtc = checked
        self.update_display()

    def on_pw_toggled(self, checked):
        """Callback for PW checkbox toggle"""
        self.show_pw = checked
        self.update_display()

    def on_port1_toggled(self, checked):
        """Callback for port 1 checkbox toggle"""
        self.show_port1 = checked
        self.update_display()

    def on_port2_toggled(self, checked):
        """Callback for port 2 checkbox toggle"""
        self.show_port2 = checked
        self.update_display()

    def on_s2p_toggled(self, checked):
        """Callback for S2P checkbox toggle"""
        self.show_s2p = checked
        self.update_display()

    def on_filter_changed(self, value):
        """Callback for filter spinbox change"""
        self.s2p_filter_size = value
        if self.show_s2p and self.s2p_network is not None:
            self.update_display()

    def export_current_plot(self):
        """Export current plot to image file"""
        if self.canvas.current_plot_data is None:
            QMessageBox.warning(self, "Export Error", "No plot available to export.")
            return

        # Get current request info for filename suggestion
        data_dict = self.request
        req_name = str(data_dict.get('req_name', 'unknown'))

        # Create suggested filename
        methods = []
        if self.show_gbtc:
            methods.append('gbtc')
        if self.show_pw:
            methods.append('pw')
        if self.show_s2p and self.s2p_filename:
            s2p_name = os.path.splitext(os.path.basename(self.s2p_filename))[0]
            methods.append(f's2p_{s2p_name}')
        method_suffix = '_' + '_'.join(methods) if methods else ''

        params = []
        if self.show_port1:
            params.append('port1')
        if self.show_port2:
            params.append('port2')
        param_suffix = '_' + '_'.join(params) if params else ''

        suggested_name = f"{req_name}_sparams{method_suffix}{param_suffix}_iter{self.current_iteration}.png"

        # Open file dialog
        filename, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Export S-Parameters Plot",
            suggested_name,
            "PNG Images (*.png);;PDF Files (*.pdf);;SVG Files (*.svg);;All Files (*)"
        )

        if filename:
            try:
                # Determine export method based on file extension
                ext = os.path.splitext(filename)[1].lower()

                if ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                    # Use high-quality export for raster formats
                    success = self.canvas.export_high_quality_image(filename, dpi=300)
                else:
                    # Use standard export for vector formats
                    success = self.canvas.export_image(filename)

                if success:
                    QMessageBox.information(self, "Export Successful",
                                            f"Plot exported successfully to:\n{filename}")
                else:
                    QMessageBox.critical(self, "Export Error",
                                         "Failed to export plot. Please check the filename and try again.")

            except Exception as e:
                QMessageBox.critical(self, "Export Error",
                                     f"An error occurred during export:\n{str(e)}")

    def export_hdf5_data(self):
        """Export current request data to HDF5 format"""
        data_dict = self.request

        if not data_dict:
            QMessageBox.warning(self, "Export Error", "No data available to export.")
            return

        # Generate suggested filename
        req_name = str(data_dict.get('req_name', 'unknown_request'))
        clean_name = "".join(c for c in req_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        suggested_filename = f"{clean_name}_gbtc_data.h5"

        # Export the data
        self.hdf5_exporter.export_single_request(data_dict, suggested_filename)

    def update_display(self):
        """Update the S-parameter display"""
        data_dict = self.request
        if data_dict.get('request_type', None) == 'GBTCSim':
            # Get iteration info for the title
            iteration_info = self._get_iteration_info(self.current_iteration)

            self.canvas.plot_s_parameters(
                data_dict,
                show_gbtc=self.show_gbtc,
                show_pw=self.show_pw,
                show_port1=self.show_port1,
                show_port2=self.show_port2,
                show_s2p=self.show_s2p,
                s2p_network=self.s2p_network,
                s2p_filename=self.s2p_filename,
                s2p_filter_size=self.s2p_filter_size,
                iteration=self.current_iteration,
                iteration_info=iteration_info
            )
        else:
            # Clear canvas if no valid data
            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available for plotting\nLoad an S2P file or check GBTC simulation data',
                    ha='center', va='center', transform=ax.transAxes, fontsize=16)
            self.canvas.draw()

    def refresh_iteration_controls(self):
        """Refresh iteration controls when data changes"""
        self.max_iterations = self._get_max_iterations()
        self.iteration_spinbox.setMaximum(max(0, self.max_iterations - 1))
        self.iteration_info_label.setText(f"/ {self.max_iterations - 1}")

        # Reset to first iteration if current iteration is out of bounds
        if self.current_iteration >= self.max_iterations:
            self.current_iteration = 0
            self.iteration_spinbox.setValue(self.current_iteration)
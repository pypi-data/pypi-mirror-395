import numpy as np
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox,
                               QPushButton, QGridLayout, QGroupBox, QSizePolicy, QFileDialog, QMessageBox, QDialog,
                               QDoubleSpinBox, QProgressDialog, QCheckBox)
from PySide6.QtCore import Qt, Signal
import matplotlib
from matplotlib import colors
from scipy.signal import find_peaks
from qosm.gui.objects import HDF5Exporter

matplotlib.use('Agg')  # Force Agg backend before any other matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os


class FarFieldCanvas(FigureCanvas):
    """Integrated matplotlib canvas for displaying far field patterns"""

    def __init__(self, parent=None):
        self.figure = Figure(figsize=(10, 6))
        super().__init__(self.figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # Axes for display (will be recreated based on plot type)
        self.axes = None
        self.current_plot_type = 'cartesian'  # 'cartesian' or 'polar'

        # Store current plot data for export
        self.current_plot_data = None
        self.current_plot_info = None

    def find_beamwidth_3db(self, theta_deg, gain_db):
        """
        Find the -3dB beamwidth and return the angles

        Returns:
        beamwidth: float, -3dB beamwidth in degrees
        angles_3db: tuple, (left_angle, right_angle) at -3dB points
        """
        if len(gain_db) == 0:
            return None, (None, None)

        # Find maximum gain
        max_gain = np.max(gain_db)
        target_level = max_gain - 3.0  # -3dB point

        # Find main beam center (maximum point)
        max_idx = np.argmax(gain_db)
        max_angle = theta_deg[max_idx]

        # Find -3dB points on both sides of the main beam
        left_angle = None
        right_angle = None

        # Search left side
        for i in range(max_idx, -1, -1):
            if gain_db[i] <= target_level:
                if i < len(gain_db) - 1:
                    # Linear interpolation between points
                    t = (target_level - gain_db[i]) / (gain_db[i + 1] - gain_db[i])
                    left_angle = theta_deg[i] + t * (theta_deg[i + 1] - theta_deg[i])
                else:
                    left_angle = theta_deg[i]
                break

        # Search right side
        for i in range(max_idx, len(gain_db)):
            if gain_db[i] <= target_level:
                if i > 0:
                    # Linear interpolation between points
                    t = (target_level - gain_db[i - 1]) / (gain_db[i] - gain_db[i - 1])
                    right_angle = theta_deg[i - 1] + t * (theta_deg[i] - theta_deg[i - 1])
                else:
                    right_angle = theta_deg[i]
                break

        # Calculate beamwidth
        if left_angle is not None and right_angle is not None:
            beamwidth = abs(right_angle - left_angle)
        else:
            beamwidth = None

        return beamwidth, (left_angle, right_angle)

    def find_first_sidelobe_level(self, theta_deg, gain_db):
        """
        Find the first sidelobe level

        Returns:
        sidelobe_level: float, first sidelobe level in dB
        sidelobe_angle: float, angle of first sidelobe in degrees
        """
        if len(gain_db) < 5:  # Need minimum points
            return None, None

        # Find main beam peak
        max_idx = np.argmax(gain_db)
        max_gain = gain_db[max_idx]

        # Define minimum separation from main beam (in terms of array indices)
        min_separation = max(3, len(gain_db) // 20)  # At least 3 points away

        # Find peaks in the pattern
        peaks, properties = find_peaks(gain_db, height=max_gain - 50, distance=min_separation)

        if len(peaks) == 0:
            return None, None

        # Remove the main peak
        peaks = peaks[peaks != max_idx]

        if len(peaks) == 0:
            return None, None

        # Find the highest sidelobe
        sidelobe_gains = gain_db[peaks]
        highest_sidelobe_idx = np.argmax(sidelobe_gains)
        sidelobe_peak_idx = peaks[highest_sidelobe_idx]

        sidelobe_level = gain_db[sidelobe_peak_idx]
        sidelobe_angle = theta_deg[sidelobe_peak_idx]

        return sidelobe_level, sidelobe_angle

    def plot_far_field_pattern(self, pattern_data, data_dict, display_mode='normalized', iteration=0,
                               plot_type='cartesian'):
        """
        Display the far field pattern

        Args:
            pattern_data: Dictionary with 'UdB', 'GdB', 'theta_deg', 'phi_deg'
            data_dict: Data dictionary
            display_mode: 'normalized' or 'absolute'
            iteration: Iteration number
            plot_type: 'cartesian' or 'polar'
        """
        if pattern_data is None:
            return

        # Clear figure and create appropriate axes
        self.figure.clear()
        self.current_plot_type = plot_type

        if plot_type == 'polar':
            self.axes = self.figure.add_subplot(111, projection='polar')
        else:
            self.axes = self.figure.add_subplot(111)

        # Extract data
        theta_deg = pattern_data['theta_deg']
        phi_deg = pattern_data['phi_deg']
        normalized_gain_db = pattern_data['UdB']
        absolute_gain_db = pattern_data['GdB']

        # Choose data based on display mode
        if display_mode == 'normalized':
            gain_db = normalized_gain_db
            ylabel = 'Normalized Gain (dB)'
            title_suffix = 'Normalized Gain'
        else:  # absolute
            gain_db = normalized_gain_db + absolute_gain_db  # Add absolute gain
            ylabel = 'Absolute Gain (dB)'
            title_suffix = 'Absolute Gain'

        # Find and calculate -3dB beamwidth
        beamwidth, angles_3db = self.find_beamwidth_3db(theta_deg, gain_db)

        # Find and mark first sidelobe
        sidelobe_level, sidelobe_angle = self.find_first_sidelobe_level(theta_deg, gain_db)

        if plot_type == 'polar':
            self._plot_polar_pattern(theta_deg, gain_db, beamwidth, angles_3db,
                                     sidelobe_level, sidelobe_angle, ylabel)
        else:
            self._plot_cartesian_pattern(theta_deg, gain_db, beamwidth, angles_3db,
                                         sidelobe_level, sidelobe_angle, ylabel)

        # Get request information for title
        req_name = data_dict.get('req_name', 'Unknown')
        horn_name = data_dict.get('horn_name', 'Unknown')

        # Get sweep information for title
        sweep_values = data_dict.get('sweep_values', [])
        sweep_attribute = data_dict.get('sweep_attribute', '')

        if iteration < len(sweep_values):
            sweep_info = f"\n{sweep_attribute} = {sweep_values[iteration]}"
        else:
            sweep_info = ""

        title = f'{req_name} - {title_suffix} (φ={phi_deg}°, Horn: {horn_name}){sweep_info}'
        self.axes.set_title(title)

        # Add information text box (position depends on plot type)
        info_text = self.create_info_text(pattern_data, display_mode, beamwidth,
                                          angles_3db, sidelobe_level, sidelobe_angle)

        if plot_type == 'polar':
            # Position info box for polar plot
            self.axes.text(0.02, 0.98, info_text, transform=self.figure.transFigure,
                           verticalalignment='top', horizontalalignment='left',
                           bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.8),
                           fontsize=9, fontfamily='monospace')
        else:
            # Position info box for cartesian plot
            self.axes.text(0.02, 0.98, info_text, transform=self.axes.transAxes,
                           verticalalignment='top', horizontalalignment='left',
                           bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.8),
                           fontsize=9, fontfamily='monospace')

        # Store current plot data for export
        self.current_plot_data = {
            'theta_deg': theta_deg,
            'gain_db': gain_db,
            'phi_deg': phi_deg,
            'display_mode': display_mode,
            'plot_type': plot_type,
            'iteration': iteration,
            'beamwidth': beamwidth,
            'angles_3db': angles_3db,
            'sidelobe_level': sidelobe_level,
            'sidelobe_angle': sidelobe_angle,
            'absolute_gain_db': absolute_gain_db,
            'title': title
        }

        # Update canvas
        self.draw()

    def _plot_cartesian_pattern(self, theta_deg, gain_db, beamwidth, angles_3db,
                                sidelobe_level, sidelobe_angle, ylabel):
        """Plot pattern in cartesian coordinates"""
        # Plot the pattern
        self.axes.plot(theta_deg, gain_db, 'b-', linewidth=2, label='Gain Pattern')

        # Find and display -3dB beamwidth
        if beamwidth is not None and angles_3db[0] is not None and angles_3db[1] is not None:
            max_gain = np.max(gain_db)
            level_3db = max_gain - 3.0

            # Plot -3dB line
            self.axes.axhline(y=level_3db, color='r', linestyle='--', alpha=0.7, label='-3dB Level')

            # Mark -3dB points
            self.axes.plot([angles_3db[0], angles_3db[1]], [level_3db, level_3db],
                           'ro', markersize=6)

            # Add vertical lines at -3dB points
            self.axes.axvline(x=angles_3db[0], color='r', linestyle=':', alpha=0.5)
            self.axes.axvline(x=angles_3db[1], color='r', linestyle=':', alpha=0.5)

        # Mark first sidelobe
        if sidelobe_level is not None and sidelobe_angle is not None:
            self.axes.plot(sidelobe_angle, sidelobe_level, 'go', markersize=8,
                           label=f'First Sidelobe')

        # Grid and labels
        self.axes.grid(True, alpha=0.3)
        self.axes.set_xlabel('Theta (degrees)')
        self.axes.set_ylabel(ylabel)
        self.axes.legend(loc='upper right')

    def _plot_polar_pattern(self, theta_deg, gain_db, beamwidth, angles_3db,
                            sidelobe_level, sidelobe_angle, ylabel):
        """Plot pattern in polar coordinates (oriented north)"""
        # Convert theta range (typically -90° to +90°) to polar coordinates (0° to 360°)
        # In antenna coordinates: theta=0 is boresight (north), negative theta is left, positive is right

        # For polar plot, we need to map theta to proper angular coordinates
        # theta=0° -> 0° (north), theta=+90° -> 90° (east), theta=-90° -> 270° (west)
        theta_polar = np.where(theta_deg >= 0, theta_deg, 360 + theta_deg)
        theta_plot = np.deg2rad(theta_polar)

        # Normalize gain for polar plot (shift to positive values for radius)
        min_gain = np.min(gain_db)
        max_gain = np.max(gain_db)

        # Shift gain to positive values for radius representation
        if min_gain < 0:
            radius_offset = abs(min_gain) + 5  # Add 5 dB margin
            gain_radius = gain_db + radius_offset
        else:
            radius_offset = 0
            gain_radius = gain_db

        # Plot the main pattern
        self.axes.plot(theta_plot, gain_radius, 'b-', linewidth=2, label='Gain Pattern')

        # Configure polar plot
        self.axes.set_theta_zero_location('N')  # 0° at north
        self.axes.set_theta_direction(-1)  # Clockwise direction

        # Set theta labels to show actual antenna angles
        # Create labels that make sense for the antenna coordinate system
        theta_ticks = np.arange(0, 360, 30)
        theta_tick_labels = []
        for t in theta_ticks:
            if t <= 180:
                # Convert 0-180 to antenna coordinates (0 to +180)
                antenna_angle = t
            else:
                # Convert 180-360 to antenna coordinates (0 to -180)
                antenna_angle = t - 360
            theta_tick_labels.append(f'{int(antenna_angle)}°')

        self.axes.set_thetagrids(theta_ticks, theta_tick_labels)

        # Set radial labels to show gain values
        if radius_offset > 0:
            # Create custom radial ticks that show actual dB values
            r_ticks = np.linspace(0, np.max(gain_radius), 6)
            r_tick_labels = [f'{int(r - radius_offset)}' for r in r_ticks]
            self.axes.set_rgrids(r_ticks, r_tick_labels)
            self.axes.set_ylabel(f'{ylabel} (dB)', labelpad=30)
        else:
            self.axes.set_ylabel(f'{ylabel} (dB)', labelpad=30)

        # Mark -3dB points
        if beamwidth is not None and angles_3db[0] is not None and angles_3db[1] is not None:
            level_3db = max_gain - 3.0
            level_3db_radius = level_3db + radius_offset if radius_offset > 0 else level_3db

            # Convert -3dB angles to polar coordinates
            angle_3db_0_polar = angles_3db[0] if angles_3db[0] >= 0 else 360 + angles_3db[0]
            angle_3db_1_polar = angles_3db[1] if angles_3db[1] >= 0 else 360 + angles_3db[1]

            angle_3db_0_plot = np.deg2rad(angle_3db_0_polar)
            angle_3db_1_plot = np.deg2rad(angle_3db_1_polar)

            # Plot -3dB circle
            theta_circle = np.linspace(0, 2 * np.pi, 100)
            r_circle = np.full_like(theta_circle, level_3db_radius)
            self.axes.plot(theta_circle, r_circle, 'r--', alpha=0.7, label='-3dB Level')

            # Mark -3dB points
            self.axes.plot([angle_3db_0_plot, angle_3db_1_plot],
                           [level_3db_radius, level_3db_radius], 'ro', markersize=6)

        # Mark first sidelobe
        if sidelobe_level is not None and sidelobe_angle is not None:
            sidelobe_radius = sidelobe_level + radius_offset if radius_offset > 0 else sidelobe_level
            sidelobe_angle_polar = sidelobe_angle if sidelobe_angle >= 0 else 360 + sidelobe_angle
            sidelobe_angle_plot = np.deg2rad(sidelobe_angle_polar)
            self.axes.plot(sidelobe_angle_plot, sidelobe_radius, 'go', markersize=8,
                           label='First Sidelobe')

        # Add grid
        self.axes.grid(True, alpha=0.3)
        self.axes.legend(loc='upper left', bbox_to_anchor=(0.1, 1.0))

    def create_info_text(self, pattern_data, display_mode, beamwidth, angles_3db,
                         sidelobe_level, sidelobe_angle):
        """Create information text for the plot"""
        info_lines = []

        # Cut-plane angle
        info_lines.append(f"Cut-plane: φ = {pattern_data['phi_deg']:.1f}°")

        # Maximum gain (for absolute mode)
        if display_mode == 'absolute':
            max_gain = pattern_data['GdB'] + np.max(pattern_data['UdB'])
            info_lines.append(f"Max Gain: {max_gain:.1f} dB")

        # -3dB beamwidth
        if beamwidth is not None:
            info_lines.append(f"-3dB BW: {beamwidth:.1f}°")
            if angles_3db[0] is not None and angles_3db[1] is not None:
                info_lines.append(f"  ({angles_3db[0]:.1f}° to {angles_3db[1]:.1f}°)")
        else:
            info_lines.append("-3dB BW: N/A")

        # First sidelobe level
        if sidelobe_level is not None and sidelobe_angle is not None:
            max_gain_current = np.max(pattern_data['UdB'])
            if display_mode == 'absolute':
                max_gain_current += pattern_data['GdB']
            sidelobe_relative = sidelobe_level - max_gain_current
            info_lines.append(f"1st Sidelobe: {sidelobe_relative:.1f} dB")
            info_lines.append(f"  @ {sidelobe_angle:.1f}°")
        else:
            info_lines.append("1st Sidelobe: N/A")

        return '\n'.join(info_lines)

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

    def export_high_quality_image(self, filename, figsize=(12, 8), dpi=300):
        """Export high-quality standalone image"""
        if self.current_plot_data is None:
            raise ValueError("No plot data available for export")

        try:
            # Create new figure for export
            export_fig = Figure(figsize=figsize)
            data = self.current_plot_data

            # Create appropriate axes based on plot type
            if data['plot_type'] == 'polar':
                export_ax = export_fig.add_subplot(111, projection='polar')

                # Recreate polar plot with correct coordinate transformation
                theta_deg = data['theta_deg']
                gain_db = data['gain_db']

                # Convert theta range to polar coordinates (handle negative angles)
                theta_polar = np.where(theta_deg >= 0, theta_deg, 360 + theta_deg)
                theta_plot = np.deg2rad(theta_polar)

                # Handle gain offset for polar display
                min_gain = np.min(gain_db)
                if min_gain < 0:
                    radius_offset = abs(min_gain) + 5
                    gain_radius = gain_db + radius_offset
                else:
                    radius_offset = 0
                    gain_radius = gain_db

                # Plot main pattern
                export_ax.plot(theta_plot, gain_radius, 'b-', linewidth=2, label='Gain Pattern')

                # Configure polar plot
                export_ax.set_theta_zero_location('N')
                export_ax.set_theta_direction(-1)

                # Set proper theta labels for antenna coordinates
                theta_ticks = np.arange(0, 360, 30)
                theta_tick_labels = []
                for t in theta_ticks:
                    if t <= 180:
                        antenna_angle = t
                    else:
                        antenna_angle = t - 360
                    theta_tick_labels.append(f'{int(antenna_angle)}°')
                export_ax.set_thetagrids(theta_ticks, theta_tick_labels)

                # Add -3dB markers if available
                if data['beamwidth'] is not None and data['angles_3db'][0] is not None:
                    max_gain = np.max(gain_db)
                    level_3db = max_gain - 3.0
                    level_3db_radius = level_3db + radius_offset if radius_offset > 0 else level_3db

                    # Convert -3dB angles with proper coordinate transformation
                    angle_3db_0_polar = data['angles_3db'][0] if data['angles_3db'][0] >= 0 else 360 + \
                                                                                                 data['angles_3db'][0]
                    angle_3db_1_polar = data['angles_3db'][1] if data['angles_3db'][1] >= 0 else 360 + \
                                                                                                 data['angles_3db'][1]

                    angle_3db_0_plot = np.deg2rad(angle_3db_0_polar)
                    angle_3db_1_plot = np.deg2rad(angle_3db_1_polar)

                    theta_circle = np.linspace(0, 2 * np.pi, 100)
                    r_circle = np.full_like(theta_circle, level_3db_radius)
                    export_ax.plot(theta_circle, r_circle, 'r--', alpha=0.7, label='-3dB Level')
                    export_ax.plot([angle_3db_0_plot, angle_3db_1_plot],
                                   [level_3db_radius, level_3db_radius], 'ro', markersize=6)

                # Add sidelobe marker if available
                if data['sidelobe_level'] is not None:
                    sidelobe_radius = data['sidelobe_level'] + radius_offset if radius_offset > 0 else data[
                        'sidelobe_level']
                    sidelobe_angle_polar = data['sidelobe_angle'] if data['sidelobe_angle'] >= 0 else 360 + data[
                        'sidelobe_angle']
                    sidelobe_angle_plot = np.deg2rad(sidelobe_angle_polar)
                    export_ax.plot(sidelobe_angle_plot, sidelobe_radius, 'go', markersize=8,
                                   label='First Sidelobe')

                export_ax.grid(True, alpha=0.3)
                export_ax.legend(loc='upper left', bbox_to_anchor=(0.1, 1.0))

                if data['display_mode'] == 'normalized':
                    export_ax.set_ylabel('Normalized Gain (dB)', labelpad=30)
                else:
                    export_ax.set_ylabel('Absolute Gain (dB)', labelpad=30)

            else:
                # Cartesian plot
                export_ax = export_fig.add_subplot(111)

                # Plot main pattern
                export_ax.plot(data['theta_deg'], data['gain_db'], 'b-', linewidth=2, label='Gain Pattern')

                # Add -3dB markers if available
                if data['beamwidth'] is not None and data['angles_3db'][0] is not None:
                    max_gain = np.max(data['gain_db'])
                    level_3db = max_gain - 3.0
                    export_ax.axhline(y=level_3db, color='r', linestyle='--', alpha=0.7, label='-3dB Level')
                    export_ax.plot([data['angles_3db'][0], data['angles_3db'][1]], [level_3db, level_3db],
                                   'ro', markersize=6, label='-3dB Points')
                    export_ax.axvline(x=data['angles_3db'][0], color='r', linestyle=':', alpha=0.5)
                    export_ax.axvline(x=data['angles_3db'][1], color='r', linestyle=':', alpha=0.5)

                # Add sidelobe marker if available
                if data['sidelobe_level'] is not None:
                    export_ax.plot(data['sidelobe_angle'], data['sidelobe_level'], 'go', markersize=8,
                                   label='First Sidelobe')

                # Formatting
                export_ax.grid(True, alpha=0.3)
                export_ax.set_xlabel('Theta (degrees)')

                if data['display_mode'] == 'normalized':
                    export_ax.set_ylabel('Normalized Gain (dB)')
                else:
                    export_ax.set_ylabel('Absolute Gain (dB)')

                export_ax.legend(loc='upper right')

            export_ax.set_title(data['title'])

            # Save
            export_fig.savefig(filename, dpi=dpi, bbox_inches='tight')
            return True

        except Exception as e:
            print(f"Error saving high-quality image: {e}")
            return False


class FarFieldViewer(QWidget):
    """Main widget for visualizing Far Field results"""

    # Signal emitted when a new view is requested
    new_view_requested = Signal(dict)

    def __init__(self, available_requests, selected_request=None, view_id=1, parent=None):
        super().__init__(parent)
        self.available_requests = available_requests  # Dict of {request_id: data_dict}
        self.view_id = view_id
        self.current_iteration = 0
        self.display_mode = 'normalized'  # 'normalized' or 'absolute'
        self.plot_type = 'cartesian'  # 'cartesian' or 'polar'

        # Set initial selected request
        if selected_request and selected_request in available_requests:
            self.current_request_id = selected_request
        elif available_requests:
            self.current_request_id = list(available_requests.keys())[0]
        else:
            self.current_request_id = None

        self.setup_ui()
        self.update_display()

    @property
    def current_data_dict(self):
        """Get current data dictionary"""
        if self.current_request_id and self.current_request_id in self.available_requests:
            return self.available_requests[self.current_request_id]
        return {}

    def setup_ui(self):
        """User interface setup"""
        layout = QVBoxLayout(self)

        # Request selection
        request_group = QGroupBox("Request Selection")
        request_layout = QGridLayout(request_group)

        request_layout.addWidget(QLabel("Request:"), 0, 0)
        self.request_combo = QComboBox()
        self.request_combo.setMinimumWidth(200)

        # Populate combo box with available far field requests
        for request_id, data_dict in self.available_requests.items():
            if data_dict.get('request_type') == 'FarField':
                display_name = data_dict['req_name']
                self.request_combo.addItem(display_name, request_id)

        # Set current selection
        if self.current_request_id:
            index = self.request_combo.findData(self.current_request_id)
            if index >= 0:
                self.request_combo.setCurrentIndex(index)

        self.request_combo.currentIndexChanged.connect(self.on_request_changed)
        request_layout.addWidget(self.request_combo, 0, 1)

        # Horn name (read-only info)
        request_layout.addWidget(QLabel("Horn:"), 1, 0)
        self.horn_label = QLabel("N/A")
        request_layout.addWidget(self.horn_label, 1, 1)

        # Cut-plane angle (read-only info)
        request_layout.addWidget(QLabel("Cut-plane:"), 2, 0)
        self.cutplane_label = QLabel("N/A")
        request_layout.addWidget(self.cutplane_label, 2, 1)

        layout.addWidget(request_group)

        # Display controls
        controls_group = QGroupBox("Display Controls")
        controls_layout = QHBoxLayout(controls_group)

        # Iteration selection
        controls_layout.addWidget(QLabel("Iteration:"))
        self.iteration_spinbox = QSpinBox()
        self.iteration_spinbox.valueChanged.connect(self.on_iteration_changed)
        controls_layout.addWidget(self.iteration_spinbox)

        self.iteration_max_label = QLabel("/ 0")
        controls_layout.addWidget(self.iteration_max_label)

        # Spacing
        controls_layout.addStretch()

        # Display mode (normalized vs absolute gain)
        controls_layout.addWidget(QLabel("Display:"))
        self.display_combo = QComboBox()
        self.display_combo.addItem('Normalized Gain', 'normalized')
        self.display_combo.addItem('Absolute Gain', 'absolute')
        self.display_combo.currentIndexChanged.connect(self.on_display_mode_changed)
        controls_layout.addWidget(self.display_combo)

        # Plot type (cartesian vs polar)
        controls_layout.addWidget(QLabel("Plot:"))
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItem('Cartesian', 'cartesian')
        self.plot_type_combo.addItem('Polar', 'polar')
        self.plot_type_combo.currentIndexChanged.connect(self.on_plot_type_changed)
        controls_layout.addWidget(self.plot_type_combo)

        # Spacing
        controls_layout.addStretch()

        # Export button
        self.export_button = QPushButton("Export Image")
        self.export_button.setToolTip("Export current plot as image")
        self.export_button.clicked.connect(self.export_current_plot)
        controls_layout.addWidget(self.export_button)

        # Export HDF5 button
        self.export_hdf5_button = QPushButton("Export HDF5")
        self.export_hdf5_button.setToolTip("Export current request data to HDF5 format")
        self.export_hdf5_button.clicked.connect(self.export_hdf5_data)
        controls_layout.addWidget(self.export_hdf5_button)

        layout.addWidget(controls_group)

        # Canvas for display
        self.canvas = FarFieldCanvas(self)
        layout.addWidget(self.canvas)

        # Initialize HDF5 exporter
        self.hdf5_exporter = HDF5Exporter(self)

        # Update controls with current data
        self.update_controls()

    def update_controls(self):
        """Update controls based on current request data"""
        data_dict = self.current_data_dict

        # Update horn label
        horn_name = str(data_dict.get('horn_name', 'N/A'))
        self.horn_label.setText(horn_name)

        # Update cut-plane label
        grid_info = data_dict.get('grid', {})
        phi = grid_info.get('phi', 'N/A')
        if phi != 'N/A':
            self.cutplane_label.setText(f"φ = {phi}°")
        else:
            self.cutplane_label.setText("N/A")

        # Update iteration controls
        data_array = data_dict.get('data', [])
        max_iterations = len(data_array) - 1 if data_array else 0

        self.iteration_spinbox.setMaximum(max(0, max_iterations))
        self.iteration_spinbox.setMinimum(0)
        self.iteration_spinbox.setValue(0)
        self.iteration_max_label.setText(f"/ {max_iterations}")

        # Reset iteration counter
        self.current_iteration = 0

    def on_request_changed(self, index):
        """Callback for request selection change"""
        request_id = self.request_combo.itemData(index)
        if request_id != self.current_request_id:
            self.current_request_id = request_id
            self.update_controls()
            self.update_display()

    def on_iteration_changed(self, value):
        """Callback for iteration change"""
        self.current_iteration = value
        self.update_display()

    def on_display_mode_changed(self, index):
        """Callback for display mode change"""
        self.display_mode = self.display_combo.itemData(index)
        self.update_display()

    def on_plot_type_changed(self, index):
        """Callback for plot type change"""
        self.plot_type = self.plot_type_combo.itemData(index)
        self.update_display()

    def export_current_plot(self):
        """Export current plot to image file"""
        if self.canvas.current_plot_data is None:
            QMessageBox.warning(self, "Export Error", "No plot available to export.")
            return

        # Get current request info for filename suggestion
        data_dict = self.current_data_dict
        req_name = str(data_dict.get('req_name', 'unknown'))

        # Create suggested filename
        plot_suffix = "_cart" if self.plot_type == 'cartesian' else "_polar"
        mode_suffix = "_norm" if self.display_mode == 'normalized' else "_abs"
        suggested_name = f"{req_name}_iter{self.current_iteration}_farfield{plot_suffix}{mode_suffix}.png"

        # Open file dialog
        filename, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Export Far Field Plot",
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
        data_dict = self.current_data_dict

        if not data_dict:
            QMessageBox.warning(self, "Export Error", "No data available to export.")
            return

        # Generate suggested filename
        req_name = str(data_dict.get('req_name', 'unknown_request'))
        clean_name = "".join(c for c in req_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        suggested_filename = f"{clean_name}_farfield_data.h5"

        # Export the data
        self.hdf5_exporter.export_single_request(data_dict, suggested_filename)

    def update_display(self):
        """Update the far field pattern display"""
        data_dict = self.current_data_dict
        data_array = data_dict.get('data', [])

        if data_array and self.current_iteration < len(data_array):
            current_pattern_data = data_array[self.current_iteration]
            if current_pattern_data is not None:
                self.canvas.plot_far_field_pattern(
                    current_pattern_data,
                    data_dict,
                    self.display_mode,
                    self.current_iteration,
                    self.plot_type
                )
import numpy as np
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox,
                               QPushButton, QGridLayout, QGroupBox, QSizePolicy, QFileDialog, QMessageBox, QDialog,
                               QDoubleSpinBox, QProgressDialog, QCheckBox)
from PySide6.QtCore import Qt, Signal
import matplotlib
from matplotlib import colors
from qosm.gui.dialogs import GifExportDialog

from qosm import Grid, PlaneType
from qosm.gui.objects import HDF5Exporter

matplotlib.use('Agg')  # Force Agg backend before any other matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os


class NearFieldCanvas(FigureCanvas):
    """Integrated matplotlib canvas for displaying field maps"""

    def __init__(self, parent=None):
        self.figure = Figure(figsize=(8, 6))
        super().__init__(self.figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # Axes for display
        self.axes = self.figure.add_subplot(111)
        self.colorbar = None

        # Store current plot data for export
        self.current_plot_data = None
        self.current_plot_info = None

    def plot_field_map(self, field_data, data_dict, display_mode='magnitude_all', iteration=0, use_db=False,
                       db_min=-50.0, show_hpbw=True, show_contours=True):
        """
        Display the field map as 2D pcolormesh or 1D line plot

        Args:
            field_data: Field data for current iteration
            data_dict: Data dictionary
            display_mode: 'magnitude' or 'phase'
            iteration: Iteration number
            use_db: Convert magnitude to dB scale
            db_min: Minimum dB value for clipping
            show_hpbw: Show half power markers and HPBW calculation
            show_contours: Show contour lines for 2D plots
        """

        if field_data is None:
            return

        # Remove old colorbar if it exists
        if self.colorbar:
            self.colorbar.remove()
            self.colorbar = None

        self.axes.clear()

        grid_info = data_dict.get('grid', {})
        req_field = data_dict.get('req_field', {})
        req_name = data_dict.get('req_name', {})

        # Extract grid parameters
        n_value = grid_info['n']
        grid = Grid(u_range=grid_info['u_range'], v_range=grid_info['v_range'], n=grid_info['n'], plane=PlaneType.XY)

        # Calculate magnitude or phase with component selection
        if display_mode.startswith('magnitude'):
            if display_mode == 'magnitude_all':
                plot_data = np.sqrt(np.sum(np.abs(field_data) ** 2, axis=1))
                title_suffix = f"Magnitude ${req_field}$"
            elif display_mode == 'magnitude_x':
                plot_data = np.abs(field_data[:, 0])
                title_suffix = f"Magnitude ${req_field}_x$"
            elif display_mode == 'magnitude_y':
                plot_data = np.abs(field_data[:, 1])
                title_suffix = f"Magnitude ${req_field}_y$"
            elif display_mode == 'magnitude_z':
                plot_data = np.abs(field_data[:, 2])
                title_suffix = f"Magnitude ${req_field}_z$"
            else:  # fallback to original magnitude
                return

            # Store original linear data for HPBW calculation
            original_plot_data = plot_data.copy()

            # Convert to dB if requested
            if use_db:
                # Normalize to maximum value and convert to dB
                max_val = np.max(plot_data)
                if max_val > 0:
                    plot_data_normalized = plot_data / max_val
                    plot_data = 20 * np.log10(plot_data_normalized + 1e-15)
                    # Clip to minimum dB value
                    plot_data = np.maximum(plot_data, db_min)
                else:
                    plot_data = np.full_like(plot_data, db_min)
                unit = "dB"
            else:
                unit = "V/m"

            colormap_colors = [
                [0.000, 0.008, 0.560],  # -50dB: [0, 0.8, 56]
                [0.000, 0.165, 0.584],  # -48dB: [0, 16.5, 58.4]
                [0.000, 0.333, 0.667],  # -46dB: [0, 33.3, 66.7]
                [0.000, 0.494, 0.749],  # -44dB: [0, 49.4, 74.9]
                [0.000, 0.651, 0.827],  # -42dB: [0, 65.1, 82.7]
                [0.000, 0.812, 0.906],  # -40dB: [0, 81.2, 90.6]
                [0.000, 0.976, 0.988],  # -38dB: [0, 97.6, 98.8]
                [0.000, 1.000, 0.863],  # -36dB: [0, 100, 86.3]
                [0.000, 1.000, 0.702],  # -34dB: [0, 100, 70.2]
                [0.000, 1.000, 0.537],  # -32dB: [0, 100, 53.7]
                [0.000, 1.000, 0.376],  # -30dB: [0, 100, 37.6]
                [0.000, 1.000, 0.216],  # -28dB: [0, 100, 21.6]
                [0.000, 1.000, 0.055],  # -26dB: [0, 100, 5.5]
                [0.110, 1.000, 0.000],  # -24dB: [11, 100, 0]
                [0.271, 1.000, 0.000],  # -22dB: [27.1, 100, 0]
                [0.427, 1.000, 0.000],  # -20dB: [42.7, 100, 0]
                [0.596, 1.000, 0.000],  # -18dB: [59.6, 100, 0]
                [0.757, 1.000, 0.000],  # -16dB: [75.7, 100, 0]
                [0.914, 1.000, 0.000],  # -14dB: [91.4, 100, 0]
                [1.000, 0.925, 0.000],  # -12dB: [100, 92.5, 0]
                [1.000, 0.757, 0.000],  # -10dB: [100, 75.7, 0]
                [1.000, 0.600, 0.000],  # -08dB: [100, 60, 0]
                [1.000, 0.439, 0.000],  # -06dB: [100, 43.9, 0]
                [1.000, 0.275, 0.000],  # -04dB: [100, 27.5, 0]
                [1.000, 0.114, 0.000],  # -02dB: [100, 11.4, 0]
                [1.000, 0.000, 0.000],  # 0dB: [100, 0, 0]
            ]
            cmap = colors.LinearSegmentedColormap.from_list(
                'extracted_gradient_smooth', colormap_colors, N=256
            )

        elif display_mode.startswith('phase'):
            if display_mode == 'phase_x':
                plot_data = np.angle(field_data[:, 0], deg=True)
                title_suffix = f"Phase ${req_field}_x$"
            elif display_mode == 'phase_y':
                plot_data = np.angle(field_data[:, 1], deg=True)
                title_suffix = f"Phase ${req_field}_y$"
            elif display_mode == 'phase_z':
                plot_data = np.angle(field_data[:, 2], deg=True)
                title_suffix = f"Phase ${req_field}_z$)"
            else:  # fallback to original phase
                return

            cmap = 'hsv'
            unit = "°"
            original_plot_data = None  # No HPBW for phase plots
        else:
            return

        # Reshape plot data to grid
        plot_data = plot_data.reshape(grid.shape)
        if original_plot_data is not None:
            original_plot_data = original_plot_data.reshape(grid.shape)

        # Check if one dimension is 1 (essentially 1D data)
        is_1d = grid.shape[0] == 1 or grid.shape[1] == 1

        # Variables for HPBW calculation
        hpbw_info = ""
        half_power_positions = []

        if is_1d:
            # 1D plot case
            if grid.shape[0] == 1:
                # Single row, varying columns (U direction)
                if grid.u.ndim == 2:
                    x_data = grid.u[0, :] * 1e3  # First (and only) row
                else:
                    x_data = grid.u * 1e3  # Already 1D
                y_data = plot_data[0, :]  # First (and only) row
                x_label = 'U [mm]'

                # Use original data for HPBW calculation if available
                if original_plot_data is not None:
                    original_y_data = original_plot_data[0, :]
                else:
                    original_y_data = None
            else:
                # Single column, varying rows (V direction)
                if grid.v.ndim == 2:
                    x_data = grid.v[:, 0] * 1e3  # First (and only) column
                else:
                    x_data = grid.v * 1e3  # Already 1D
                y_data = plot_data[:, 0]  # First (and only) column
                x_label = 'V [mm]'

                # Use original data for HPBW calculation if available
                if original_plot_data is not None:
                    original_y_data = original_plot_data[:, 0]
                else:
                    original_y_data = None

            # Create line plot
            line_color = 'blue' if display_mode.startswith('magnitude') else 'red'
            self.axes.plot(x_data, y_data, color=line_color, linewidth=2, marker='o', markersize=3)

            # Calculate and display HPBW for magnitude plots
            if show_hpbw and display_mode.startswith('magnitude') and original_y_data is not None:
                # Find maximum value and half power level
                max_val = np.max(original_y_data)
                half_power_level = max_val / np.sqrt(2)  # -3dB point

                # Convert half power level to display units
                if use_db:
                    half_power_display = -3.0  # -3dB
                    half_power_label = "-3dB"
                else:
                    half_power_display = half_power_level
                    half_power_label = f"{half_power_level:.3f} V/m"

                # Find crossings with half power level
                crossings = []
                for i in range(len(original_y_data) - 1):
                    if ((original_y_data[i] <= half_power_level <= original_y_data[i + 1]) or
                            (original_y_data[i] >= half_power_level >= original_y_data[i + 1])):
                        # Linear interpolation to find exact crossing point
                        if original_y_data[i + 1] != original_y_data[i]:
                            alpha = (half_power_level - original_y_data[i]) / (
                                        original_y_data[i + 1] - original_y_data[i])
                            x_crossing = x_data[i] + alpha * (x_data[i + 1] - x_data[i])
                            crossings.append(x_crossing)

                # Draw half power line
                self.axes.axhline(y=half_power_display, color='red', linestyle='--', alpha=0.7,
                                  label=f'Half Power ({half_power_label})')

                # Mark crossing points
                for x_cross in crossings:
                    self.axes.axvline(x=x_cross, color='red', linestyle=':', alpha=0.7)
                    self.axes.plot(x_cross, half_power_display, 'ro', markersize=6)
                    half_power_positions.append(x_cross)

                # Calculate HPBW if we have exactly 2 crossings
                if len(crossings) == 2:
                    hpbw = abs(crossings[1] - crossings[0])
                    hpbw_info = f"\nHPBW = {hpbw:.3f} mm"

                    # Add annotation - position arrow correctly for both dB and linear scales
                    mid_x = (crossings[0] + crossings[1]) / 2
                    y_range = np.max(y_data) - np.min(y_data)

                    self.axes.annotate(f'HPBW = {hpbw:.3f} mm',
                                       xy=(mid_x, half_power_display),
                                       xytext=(mid_x, half_power_display - 0.05*y_range),
                                       ha='center', fontsize=10, color='red')

                elif len(crossings) > 2:
                    # Multiple crossings - calculate beamwidths between consecutive pairs
                    beamwidths = []
                    for i in range(0, len(crossings), 2):
                        if i + 1 < len(crossings):
                            bw = abs(crossings[i + 1] - crossings[i])
                            beamwidths.append(bw)

                    if beamwidths:
                        hpbw_info = f"\nHPBWs = {[f'{bw:.3f}' for bw in beamwidths]} mm"

                # Add legend
                self.axes.legend(loc='best', fontsize=9)

            # Labels and formatting
            self.axes.set_xlabel(x_label)
            self.axes.set_ylabel(f'{title_suffix} [{unit}]')
            self.axes.grid(True, alpha=0.3)

            # No colorbar for 1D plots
            self.colorbar = None

        else:
            # 2D plot case
            im = self.axes.pcolormesh(grid.u, grid.v, plot_data, cmap=cmap, shading='auto')

            # Add colorbar
            self.colorbar = self.figure.colorbar(im, ax=self.axes)
            self.colorbar.set_label(f'{title_suffix} [{unit}]')

            # For 2D plots, add contour lines if enabled
            if show_contours and show_hpbw and display_mode.startswith('magnitude') and original_plot_data is not None:
                max_val = np.max(original_plot_data)
                half_power_level = max_val / np.sqrt(2)

                # Add contour line at half power level
                contour_color = 'white' if use_db else 'red'
                contour = self.axes.contour(grid.u, grid.v, original_plot_data,
                                            levels=[half_power_level], colors=contour_color,
                                            linestyles='--', linewidths=2, alpha=0.8)
                self.axes.clabel(contour, inline=True, fontsize=9, fmt='-3dB')

            # Labels
            self.axes.set_xlabel('U')
            self.axes.set_ylabel('V')
            self.axes.grid(True, alpha=0.3)

            # Set equal aspect ratio for 2D field maps
            self.axes.set_aspect('equal', adjustable='box')

        # Get sweep information for title
        sweep_values = data_dict.get('sweep_values', [])
        sweep_attribute = data_dict.get('sweep_attribute', '')

        if iteration < len(sweep_values):
            sweep_info = f"\n{sweep_attribute} = {sweep_values[iteration]}"
        else:
            sweep_info = ""

        # Add HPBW info to title
        full_title = f'{req_name} - {title_suffix}{sweep_info}{hpbw_info}'
        self.axes.set_title(full_title)

        # Store current plot data for export
        self.current_plot_data = {
            'U': grid.u,
            'V': grid.v,
            'plot_data': plot_data,
            'cmap': cmap if not is_1d else None,
            'title_suffix': title_suffix,
            'unit': unit,
            'iteration': iteration,
            'n_value': n_value,
            'use_db': use_db,
            'db_min': db_min,
            'display_mode': display_mode,
            'sweep_info': sweep_info,
            'is_1d': is_1d,
            'x_data': x_data if is_1d else None,
            'y_data': y_data if is_1d else None,
            'x_label': x_label if is_1d else None,
            'hpbw_info': hpbw_info,
            'half_power_positions': half_power_positions,
            'show_hpbw': show_hpbw,
            'show_contours': show_contours
        }

        # Update canvas
        self.draw()

    def export_image(self, filename, dpi=300, bbox_inches='tight'):
        """
        Export current plot to image file

        Args:
            filename: Output filename with extension
            dpi: Resolution in dots per inch
            bbox_inches: Bounding box option ('tight' or None)
        """
        if self.current_plot_data is None:
            raise ValueError("No plot data available for export")

        try:
            self.figure.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    def export_high_quality_image(self, filename, figsize=(10, 8), dpi=300):
        """
        Export high-quality standalone image with better formatting

        Args:
            filename: Output filename with extension
            figsize: Figure size in inches (width, height)
            dpi: Resolution in dots per inch
        """
        if self.current_plot_data is None:
            raise ValueError("No plot data available for export")

        try:
            # Store original figure properties
            original_size = self.figure.get_size_inches()
            original_dpi = self.figure.get_dpi()

            # Temporarily set the desired size and DPI for export
            self.figure.set_size_inches(figsize)
            self.figure.set_dpi(dpi)

            # Save the current figure directly
            self.figure.savefig(filename, dpi=dpi, bbox_inches='tight',
                                facecolor='white', edgecolor='none')

            # Restore original properties
            self.figure.set_size_inches(original_size)
            self.figure.set_dpi(original_dpi)

            # Refresh the canvas to restore the display properly
            self.draw()

            return True

        except Exception as e:
            print(f"Error saving high-quality image: {e}")
            # Try to restore original settings even if export failed
            try:
                self.figure.set_size_inches(original_size)
                self.figure.set_dpi(original_dpi)
                self.draw()
            except:
                pass
            return False

    def export_gif_animation(self, filename, all_field_data, grid_info, display_mode='magnitude_all',
                             duration_per_frame=0.5, figsize=(10, 8), dpi=100, use_db=False, db_min=-50.0,
                             show_annotations=False, show_contours=True):
        """
        Export animated GIF with all iterations using the existing viewer rendering system

        Args:
            filename: Output filename with .gif extension
            all_field_data: List of field data for all iterations
            grid_info: Grid information (u_range, v_range, n)
            display_mode: 'magnitude_all', 'magnitude_x', etc.
            duration_per_frame: Duration per frame in seconds
            figsize: Figure size in inches (width, height)
            dpi: Resolution in dots per inch
            use_db: Convert magnitude to dB scale
            db_min: Minimum dB value for clipping
            show_annotations: Show HPBW annotations (uses existing viewer settings)
            show_contours: Show contour lines for 2D plots
        """
        try:
            from PIL import Image
            import io
            from qosm import Grid, PlaneType

            # Store current viewer state to restore later
            original_display_mode = self.parent().display_mode if hasattr(self.parent(),
                                                                          'display_mode') else display_mode
            original_use_db = self.parent().use_db if hasattr(self.parent(), 'use_db') else use_db
            original_db_min = self.parent().db_min if hasattr(self.parent(), 'db_min') else db_min
            original_show_contours = self.parent().show_contours if hasattr(self.parent(),
                                                                            'show_contours') else show_contours
            original_iteration = self.parent().current_iteration if hasattr(self.parent(), 'current_iteration') else 0
            original_figsize = self.figure.get_size_inches()
            original_dpi = self.figure.get_dpi()

            viewer = self.parent()
            data_dict = viewer.current_data_dict

            # Calculate global range across all iterations for consistent scaling
            grid = Grid(u_range=grid_info['u_range'], v_range=grid_info['v_range'],
                        n=grid_info['n'], plane=PlaneType.XY)

            global_min = float('inf')
            global_max = float('-inf')
            is_1d = grid.shape[0] == 1 or grid.shape[1] == 1

            for field_data in all_field_data:
                if field_data is None:
                    continue

                # Calculate plot data based on display mode
                if display_mode.startswith('magnitude'):
                    if display_mode == 'magnitude_all':
                        plot_data = np.sqrt(np.sum(np.abs(field_data) ** 2, axis=1))
                    elif display_mode == 'magnitude_x':
                        plot_data = np.abs(field_data[:, 0])
                    elif display_mode == 'magnitude_y':
                        plot_data = np.abs(field_data[:, 1])
                    elif display_mode == 'magnitude_z':
                        plot_data = np.abs(field_data[:, 2])
                    else:
                        continue

                    # Convert to dB if requested (same as in plotting function)
                    if use_db:
                        max_val = np.max(plot_data)
                        if max_val > 0:
                            plot_data_normalized = plot_data / max_val
                            plot_data = 20 * np.log10(plot_data_normalized + 1e-15)
                            plot_data = np.maximum(plot_data, db_min)
                        else:
                            plot_data = np.full_like(plot_data, db_min)

                elif display_mode.startswith('phase'):
                    if display_mode == 'phase_x':
                        plot_data = np.angle(field_data[:, 0], deg=True)
                    elif display_mode == 'phase_y':
                        plot_data = np.angle(field_data[:, 1], deg=True)
                    elif display_mode == 'phase_z':
                        plot_data = np.angle(field_data[:, 2], deg=True)
                    else:
                        continue
                else:
                    continue

                # Track global range
                global_min = min(global_min, np.min(plot_data))
                global_max = max(global_max, np.max(plot_data))

            # Temporarily set export settings
            viewer.display_mode = display_mode
            viewer.use_db = use_db
            viewer.db_min = db_min
            viewer.show_contours = show_contours and show_annotations  # Use annotations flag for contours too

            # Set figure size for export and store layout parameters
            self.figure.set_size_inches(figsize)
            self.figure.set_dpi(dpi)

            # Create a consistent layout by plotting the first frame and storing layout info
            if all_field_data and all_field_data[0] is not None:
                viewer.current_iteration = 0
                viewer.update_display()

                # For 2D plots, store the initial subplot position to maintain consistency
                if not is_1d:
                    # Get the initial axes position
                    initial_axes_pos = self.axes.get_position()

                    # Force a consistent colorbar width/position
                    if hasattr(self, 'colorbar') and self.colorbar is not None:
                        initial_cbar_pos = self.colorbar.ax.get_position()

            # Collect frames by iterating through all iterations
            frames = []

            for iteration in range(len(all_field_data)):
                # Update iteration and refresh display
                viewer.current_iteration = iteration
                viewer.update_display()

                # Apply consistent scaling and layout
                if is_1d:
                    # For 1D plots, set y-axis limits
                    self.axes.set_ylim(global_min, global_max)
                else:
                    # For 2D plots, ensure consistent scaling and layout
                    images = self.axes.get_images()
                    if images:
                        # Set consistent color limits
                        images[0].set_clim(vmin=global_min, vmax=global_max)

                    # Ensure consistent axes position
                    if 'initial_axes_pos' in locals():
                        self.axes.set_position(initial_axes_pos)

                    # Ensure consistent colorbar position and size
                    if hasattr(self, 'colorbar') and self.colorbar is not None:
                        if 'initial_cbar_pos' in locals():
                            self.colorbar.ax.set_position(initial_cbar_pos)

                        # Update colorbar with consistent limits via the mappable
                        self.colorbar.mappable.set_clim(vmin=global_min, vmax=global_max)

                        # Ensure colorbar ticks are consistent
                        if display_mode.startswith('phase'):
                            # For phase plots, use consistent phase range
                            self.colorbar.set_ticks([-180, -90, 0, 90, 180])
                        else:
                            # For magnitude plots, update the colorbar range
                            self.colorbar.update_normal(self.colorbar.mappable)

                # Force tight layout to be consistent
                self.figure.tight_layout()

                # Redraw to apply all changes
                self.draw()

                # Ensure the canvas is fully updated before capturing
                self.figure.canvas.flush_events()

                # Capture current frame with consistent settings
                buf = io.BytesIO()
                self.figure.savefig(buf, format='png', dpi=dpi, bbox_inches='tight',
                                    facecolor='white', edgecolor='none',
                                    pad_inches=0.1)  # Consistent padding
                buf.seek(0)
                frame = Image.open(buf)

                # Ensure all frames have the same size by cropping/padding if necessary
                if not frames:
                    # Store the size of the first frame as reference
                    reference_size = frame.size
                else:
                    # Resize subsequent frames to match the first frame
                    if frame.size != reference_size:
                        frame = frame.resize(reference_size, Image.Resampling.LANCZOS)

                frames.append(frame.copy())
                buf.close()

            # Restore original viewer state
            viewer.display_mode = original_display_mode
            viewer.use_db = original_use_db
            viewer.db_min = original_db_min
            viewer.show_contours = original_show_contours
            viewer.current_iteration = original_iteration
            self.figure.set_size_inches(original_figsize)
            self.figure.set_dpi(original_dpi)

            # Restore original display
            viewer.update_display()

            # Save as GIF with consistent frame sizes
            if frames:
                duration_ms = int(duration_per_frame * 1000)

                # Ensure all frames are exactly the same size
                if len(set(frame.size for frame in frames)) > 1:
                    print(f"Warning: Frame sizes vary. Normalizing to {reference_size}")
                    frames = [frame.resize(reference_size, Image.Resampling.LANCZOS)
                              if frame.size != reference_size else frame for frame in frames]

                frames[0].save(
                    filename,
                    save_all=True,
                    append_images=frames[1:],
                    duration=duration_ms,
                    loop=0,
                    optimize=True
                )

            return True

        except Exception as e:
            print(f"Error creating animated GIF: {e}")
            import traceback
            traceback.print_exc()

            # Try to restore original state even if export failed
            try:
                if 'viewer' in locals():
                    viewer.display_mode = original_display_mode
                    viewer.use_db = original_use_db
                    viewer.db_min = original_db_min
                    viewer.show_contours = original_show_contours
                    viewer.current_iteration = original_iteration
                    viewer.update_display()
                if 'original_figsize' in locals():
                    self.figure.set_size_inches(original_figsize)
                if 'original_dpi' in locals():
                    self.figure.set_dpi(original_dpi)
            except:
                pass

            return False


class NearFieldViewer(QWidget):
    """Main widget for visualizing Near Field results"""

    # Signal emitted when a new view is requested
    new_view_requested = Signal(dict)

    def __init__(self, available_requests, selected_request=None, view_id=1, parent=None):
        super().__init__(parent)
        self.available_requests = available_requests  # Dict of {request_id: data_dict}
        self.view_id = view_id
        self.current_iteration = 0
        self.display_mode = 'magnitude_all'
        self.use_db = False
        self.db_min = -50.0
        self.show_contours = True  # New attribute for contour control

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

        # Populate combo box with available requests
        for request_id, data_dict in self.available_requests.items():
            display_name = data_dict['req_name']
            self.request_combo.addItem(display_name, request_id)

        # Set current selection
        if self.current_request_id:
            index = self.request_combo.findData(self.current_request_id)
            if index >= 0:
                self.request_combo.setCurrentIndex(index)

        self.request_combo.currentIndexChanged.connect(self.on_request_changed)
        request_layout.addWidget(self.request_combo, 0, 1)

        # Domain UUID (read-only info)
        request_layout.addWidget(QLabel("Domain:"), 1, 0)
        self.domain_label = QLabel("N/A")
        request_layout.addWidget(self.domain_label, 1, 1)

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

        # Display mode
        controls_layout.addWidget(QLabel("Display:"))
        self.display_combo = QComboBox()
        self.display_combo.addItem('Magnitude', 'magnitude_all')
        self.display_combo.addItem('Mag X', 'magnitude_x')
        self.display_combo.addItem('Mag Y', 'magnitude_y')
        self.display_combo.addItem('Mag Z', 'magnitude_z')
        self.display_combo.addItem('Phase X', 'phase_x')
        self.display_combo.addItem('Phase Y', 'phase_y')
        self.display_combo.addItem('Phase Z', 'phase_z')
        self.display_combo.currentIndexChanged.connect(self.on_display_mode_changed)
        controls_layout.addWidget(self.display_combo)

        # dB checkbox and minimum setting
        self.db_checkbox = QCheckBox("dB")
        self.db_checkbox.setToolTip("Convert magnitude to normalized dB scale")
        self.db_checkbox.toggled.connect(self.on_db_toggled)
        controls_layout.addWidget(self.db_checkbox)

        # dB minimum value
        controls_layout.addWidget(QLabel("Min:"))
        self.db_min_spinbox = QDoubleSpinBox()
        self.db_min_spinbox.setRange(-200, 0)
        self.db_min_spinbox.setValue(-50)
        self.db_min_spinbox.setSuffix(" dB")
        self.db_min_spinbox.setToolTip("Minimum dB value (values below will be clipped)")
        self.db_min_spinbox.valueChanged.connect(self.on_db_min_changed)
        self.db_min_spinbox.setEnabled(False)  # Initially disabled
        controls_layout.addWidget(self.db_min_spinbox)

        # Spacing
        controls_layout.addStretch()

        # Contour checkbox
        self.contour_checkbox = QCheckBox("Contours")
        self.contour_checkbox.setChecked(True)  # Default to enabled
        self.contour_checkbox.setToolTip("Show contour lines at half-power level for 2D magnitude plots")
        self.contour_checkbox.toggled.connect(self.on_contour_toggled)
        controls_layout.addWidget(self.contour_checkbox)

        # Spacing
        controls_layout.addStretch()

        # Export button
        self.export_button = QPushButton("Export Image")
        self.export_button.setToolTip("Export current plot as image")
        self.export_button.clicked.connect(self.export_current_plot)
        controls_layout.addWidget(self.export_button)

        # Export GIF button
        self.export_gif_button = QPushButton("Export GIF")
        self.export_gif_button.setToolTip("Export animated GIF of all iterations")
        self.export_gif_button.clicked.connect(self.export_gif_animation)
        controls_layout.addWidget(self.export_gif_button)

        # NOUVEAU: Export HDF5 button
        self.export_hdf5_button = QPushButton("Export HDF5")
        self.export_hdf5_button.setToolTip("Export current request data to HDF5 format")
        self.export_hdf5_button.clicked.connect(self.export_hdf5_data)
        controls_layout.addWidget(self.export_hdf5_button)

        layout.addWidget(controls_group)

        # Canvas for display
        self.canvas = NearFieldCanvas(self)
        layout.addWidget(self.canvas)

        # Initialize HDF5 exporter
        self.hdf5_exporter = HDF5Exporter(self)

        # Update controls with current data
        self.update_controls()

    def update_controls(self):
        """Update controls based on current request data"""
        data_dict = self.current_data_dict

        # Update domain label
        domain_name = str(data_dict.get('domain_name', 'N/A'))
        self.domain_label.setText(domain_name)

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

    def on_db_toggled(self, checked):
        """Callback for dB checkbox toggle"""
        self.use_db = checked
        self.db_min_spinbox.setEnabled(checked)
        self.update_display()

    def on_db_min_changed(self, value):
        """Callback for dB minimum value change"""
        self.db_min = value
        if self.use_db:
            self.update_display()

    def on_contour_toggled(self, checked):
        """Callback for contour checkbox toggle"""
        self.show_contours = checked
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
        mode_short = self.display_mode.replace('magnitude_', 'mag_').replace('phase_', 'ph_')
        db_suffix = "_dB" if self.use_db and self.display_mode.startswith('magnitude') else ""
        suggested_name = (f"{req_name}_iter{self.current_iteration}_"
                          f"{mode_short}{db_suffix}.png")

        # Open file dialog
        filename, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Export Near Field Plot",
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
        suggested_filename = f"{clean_name}_request_data.h5"

        # Export the data
        self.hdf5_exporter.export_single_request(data_dict, suggested_filename)

    def export_gif_animation(self):
        """Export animated GIF of all iterations"""
        data_dict = self.current_data_dict
        data_array = data_dict.get('data', [])

        if not data_array or len(data_array) < 2:
            QMessageBox.warning(self, "Export Error",
                                "Need at least 2 iterations to create an animation.")
            return

        # Show configuration dialog
        dialog = GifExportDialog(self.use_db, self.db_min, self)
        if dialog.exec() != QDialog.Accepted:
            return

        settings = dialog.get_settings()

        # Get filename for GIF
        req_uuid = str(data_dict.get('req_uuid', 'unknown'))
        if len(req_uuid) > 10:
            req_uuid = req_uuid[:10]

        db_suffix = "_dB" if settings['use_db'] and settings['display_mode'].startswith('magnitude') else ""
        annotations_suffix = "_annotated" if settings.get('show_annotations', False) else ""
        suggested_name = f"nearfield_animation_{req_uuid}_{settings['display_mode']}{db_suffix}{annotations_suffix}.gif"

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Animated GIF",
            suggested_name,
            "GIF Files (*.gif)"
        )

        if filename:
            # Create progress dialog
            progress = QProgressDialog("Creating animated GIF...", "Cancel", 0, 0, self)
            progress.setWindowTitle("Exporting GIF")
            progress.setWindowModality(Qt.WindowModal)
            progress.setCancelButton(None)  # Remove cancel button
            progress.setMinimumDuration(0)  # Show immediately
            progress.show()

            # Process events to show the dialog
            QApplication.processEvents()

            success = False
            error_message = ""

            try:
                # Export the GIF using the canvas method (which now uses the viewer)
                grid_info = data_dict.get('grid', {})
                success = self.canvas.export_gif_animation(
                    filename,
                    data_array,
                    grid_info,
                    display_mode=settings['display_mode'],
                    duration_per_frame=settings['duration_per_frame'],
                    figsize=settings.get('figsize', (10, 8)),
                    dpi=settings['dpi'],
                    use_db=settings['use_db'],
                    db_min=settings['db_min'],
                    show_annotations=settings.get('show_annotations', False),
                    show_contours=settings.get('show_contours', True)
                )

            except Exception as e:
                error_message = str(e)
                success = False

            # Close progress dialog
            progress.close()
            progress.deleteLater()

            # Process events to ensure dialog is closed
            QApplication.processEvents()

            # Show result
            if success:
                QMessageBox.information(self, "Export Successful",
                                        f"Animated GIF exported successfully to:\n{filename}")
            else:
                if error_message:
                    QMessageBox.critical(self, "Export Error",
                                         f"An error occurred during GIF export:\n{error_message}")
                else:
                    QMessageBox.critical(self, "Export Error",
                                         "Failed to export animated GIF. Please try again.")

    def create_new_view(self):
        """Emit signal to create a new view"""
        # Pass the current request data for the new view
        self.new_view_requested.emit(self.current_data_dict)

    def update_display(self):
        """Update the field map display"""
        data_dict = self.current_data_dict
        req_field = data_dict.get('req_field', [])
        data_array = data_dict.get('data', [])

        if data_array and self.current_iteration < len(data_array):
            current_field_data = data_array[self.current_iteration]

            # Check if data is 1D before plotting
            grid_info = data_dict.get('grid', {})
            if grid_info:
                from qosm import Grid, PlaneType
                grid = Grid(u_range=grid_info['u_range'], v_range=grid_info['v_range'],
                            n=grid_info['n'], plane=PlaneType.XY)
                is_1d = grid.shape[0] == 1 or grid.shape[1] == 1
            else:
                is_1d = False

            # Show/hide contours checkbox based on data dimensionality
            self.contour_checkbox.setVisible(not is_1d)

            self.canvas.plot_field_map(
                current_field_data,
                data_dict,
                self.display_mode,
                self.current_iteration,
                self.use_db,
                self.db_min,
                show_hpbw=True,
                show_contours=self.show_contours and not is_1d  # Disable contours for 1D
            )
        else:
            # If no data, hide contours checkbox
            self.contour_checkbox.setVisible(False)
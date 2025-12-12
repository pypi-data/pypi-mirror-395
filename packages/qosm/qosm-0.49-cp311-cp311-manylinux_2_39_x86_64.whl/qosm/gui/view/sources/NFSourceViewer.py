from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from matplotlib import colors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import sqrt, sum, abs, linspace, conj

from qosm.gui.managers.SimulationManager import resample_field


class NFSourceViewDialog(QDialog):
    def __init__(self, src_data, parent=None):
        super().__init__(parent)
        self.src_data = src_data

        self.setWindowTitle("E and H Field Display")
        self.setGeometry(100, 100, 1100, 900)

        # Main layout
        main_layout = QVBoxLayout()

        # Title
        title_label = QLabel("Electromagnetic Field Visualization")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)

        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 11))
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)
        self.plot_fields()

    def plot_fields(self):
        # Clear figure
        self.figure.clear()

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

        # Get grid info
        grid_info = self.src_data['grid_info']
        x_range = grid_info['x_range']
        y_range = grid_info['y_range']

        lambda_0 = 299792458. / (self.src_data['frequency_GHz'] * 1e9)
        sampling_step = self.src_data['sampling_step_lambda'] * lambda_0
        grid_info = self.src_data['grid_info']
        r_pts_init = self.src_data['points']
        new_width = self.src_data['max_width_lambda'] * lambda_0
        new_height = self.src_data['max_height_lambda'] * lambda_0

        e_init = self.src_data['e_field']
        h_init = conj(self.src_data['h_field'])

        e, r_pts, grid = resample_field(e_init, grid_info, r_pts_init, new_width, new_height, sampling_step)
        h, _, _ = resample_field(h_init, grid_info, r_pts_init, new_width, new_height, sampling_step)

        u, v, shape = grid

        # Create initial coordinate arrays
        x = linspace(x_range[0], x_range[1], x_range[2], endpoint=True)
        y = linspace(y_range[0], y_range[1], y_range[2], endpoint=True)

        # Create subplots
        ax1 = self.figure.add_subplot(221)
        ax2 = self.figure.add_subplot(222)
        ax3 = self.figure.add_subplot(223)
        ax4 = self.figure.add_subplot(224)

        def plot_field(field, ax, field_label, u, v):
            magnitude = sqrt(abs(sum(field.reshape((v.shape[0], u.shape[0], 3)) ** 2, axis=2)))

            im = ax.pcolormesh(u, v, magnitude, shading='auto', cmap=cmap)
            ax.set_title(f'{field_label} Field Magnitude')
            ax.set_xlabel('u')
            ax.set_ylabel('v')
            ax.set_aspect('equal')
            cbar = self.figure.colorbar(im, ax=ax)
            cbar.set_label(f'|{field_label}|')

        # Plot E field magnitude
        plot_field(e_init, ax1, '$E_0$', x, y)
        plot_field(h_init, ax2, '$H_0$', x, y)
        plot_field(e, ax3, '$E_s$', u, v)
        plot_field(h, ax4, '$H_s$', u, v)

        # Adjust layout
        self.figure.tight_layout()

        # Refresh canvas
        self.canvas.draw()

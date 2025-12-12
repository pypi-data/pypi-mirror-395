import sys
import os
import glob
import numpy as np
from scipy.interpolate import interp1d
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from skimage import measure
import argparse

try:
    import saclay_format as saclay_parser
except ImportError:
    import saclay_parser


def set_axes_equal(ax, nx, ny, nz, dx, dy, dz):
    x_range = (nx - 1) * dx
    y_range = (ny - 1) * dy
    z_range = (nz - 1) * dz

    x_middle = x_range / 2
    y_middle = y_range / 2
    z_middle = z_range / 2

    plot_radius = 0.5 * max(x_range, y_range, z_range)

    ax.set_xlim([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim([z_middle - plot_radius, z_middle + plot_radius])


class ContourViewer(QWidget):
    def __init__(self,  header_file, field_name):
        super().__init__()
        self.data = saclay_parser.read( header_file)
        prefix = self.data['metadata'].get('prefix', 'Unknown')
        self.setWindowTitle(f"3D Contour Viewer - {prefix} ({field_name})")

        self.layout = QVBoxLayout(self)

        if field_name not in self.data:
            raise ValueError(f"Field '{field_name}' not found in header variables.")
        self.rho = self.data[field_name]
        self.nx, self.ny, self.nz, self.n_frames = self.rho.shape
        self.dx = self.data['metadata'].get('dx', 1.0)
        self.dy = self.data['metadata'].get('dy', 1.0)
        self.dz = self.data['metadata'].get('dz', 1.0)

        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_box_aspect([1., 1., 1.])
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

        self.fig1d, self.ax1d = plt.subplots(figsize=(8, 3))
        self.canvas1d = FigureCanvas(self.fig1d)
        self.layout.addWidget(self.canvas1d)

        self.D_values = []

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.n_frames - 1)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.update_plot)
        self.layout.addWidget(self.slider)

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.elev = 20
        self.azim = -60

        self.update_plot(0)

    def update_plot(self, index):
        self.elev = self.ax.elev
        self.azim = self.ax.azim

        rho = self.rho[:, :, :, index]
        self.label.setText(f"Frame {index+1}/{self.n_frames}")

        x = np.linspace(0, self.dx * (self.nx - 1), self.nx)
        y = np.linspace(0, self.dy * (self.ny - 1), self.ny)
        z = np.linspace(0, self.dz * (self.nz - 1), self.nz)

        vmin, vmax = np.min(rho), np.max(rho)
        level = 0.08
        if not (vmin <= level <= vmax):
            level = (vmin + vmax) / 2

        verts, faces, _, _ = measure.marching_cubes(rho, level=level)
        verts[:, 0] = verts[:, 0] * (x[1] - x[0])
        verts[:, 1] = verts[:, 1] * (y[1] - y[0])
        verts[:, 2] = verts[:, 2] * (z[1] - z[0])

        self.ax.cla()
        self.ax.plot_trisurf(
            verts[:, 0], verts[:, 1], verts[:, 2],
            triangles=faces,
            cmap='plasma',
            lw=0.2,
            alpha=0.6,
            antialiased=True
        )
        set_axes_equal(self.ax, self.nx, self.ny, self.nz, self.dx, self.dy, self.dz)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.view_init(elev=self.elev, azim=self.azim)
        self.canvas.draw()

        mid_x = self.nx // 2
        mid_y = self.ny // 2
        rho_z = rho[mid_x, mid_y, :]
        self.ax1d.cla()
        self.ax1d.plot(z, rho_z, color='blue', lw=1.5)
        self.ax1d.set_xlabel("z (fm)")
        self.ax1d.set_ylabel(r"$\rho \; (\mathrm{fm}^{-3})$")
        self.ax1d.set_title(f"f(z) at x={mid_x}, y={mid_y}")
        self.ax1d.grid(True)
        self.canvas1d.draw()

        f_interp = interp1d(z, rho_z, kind='linear', fill_value="extrapolate")
        z_fine = np.arange(z[0], z[-1], 0.05)
        rho_fine = f_interp(z_fine)

        mask = (z_fine >= 12) & (z_fine <= 25)
        z_region = z_fine[mask]
        rho_region = rho_fine[mask]

        crossings = []
        for i in range(len(z_region) - 1):
            if (rho_region[i] - 0.08) * (rho_region[i+1] - 0.08) < 0:
                z_cross = z_region[i] + (0.08 - rho_region[i]) * (z_region[i+1] - z_region[i]) / (rho_region[i+1] - rho_region[i])
                crossings.append(z_cross)

        if len(crossings) == 2:
            D = abs(crossings[1] - crossings[0])
            if len(self.D_values) <= index:
                self.D_values.extend([np.nan] * (index - len(self.D_values) + 1))
            self.D_values[index] = D

            valid_frames = np.array([
                (i + 1, val)
                for i, val in enumerate(self.D_values)
                if not np.isnan(val)
            ])
            np.savetxt(
                "D_vs_frame.dat",
                valid_frames,
                fmt="%-8d %.6f",
                header="Frame    D (fm)"
            )



def main():
    arg_parser = argparse.ArgumentParser(description="3D Contour Viewer with 1D profile and D measurement")
    arg_parser.add_argument(
        "input",
        help="Input file (.yaml/.yml or .h5/.hdf5)"
    )
    arg_parser.add_argument("--field", "-f", type=str, default=None, help="Field to visualize")
    args = arg_parser.parse_args()

    header_file = args.input

    # Read using the new unified read function
    data_all = saclay_parser.read(header_file)

    if args.field is None:
        if "rho_n" in data_all and "rho_p" in data_all:
            rho_t = data_all["rho_n"] + data_all["rho_p"]

            dx = data_all['metadata'].get('dx', 1.0)
            dy = data_all['metadata'].get('dy', 1.0)
            dz = data_all['metadata'].get('dz', 1.0)
            cell_volume = dx * dy * dz

            integrated_density = [np.sum(rho_t[:, :, :, i]) * cell_volume for i in range(rho_t.shape[3])]
            print("\nIntegrated total density per frame:")
            for i, val in enumerate(integrated_density, start=1):
                print(f" Frame {i}: {val:.6f}")

            class ContourViewerTotal(ContourViewer):
                def __init__(self, header_file, field_name):
                    super().__init__( header_file, "rho_n")
                    self.rho = rho_t
                    self.nx, self.ny, self.nz, self.n_frames = self.rho.shape
                    prefix = self.data['metadata'].get('prefix', 'Unknown')
                    self.setWindowTitle(f"3D Contour Viewer - {prefix} (rho_t)")

            ViewerClass = ContourViewerTotal
            field_to_use = "rho_t"
        else:
            ViewerClass = ContourViewer
            field_to_use = "rho_n"
    else:
        ViewerClass = ContourViewer
        field_to_use = args.field

    app = QApplication(sys.argv)
    window = ViewerClass( header_file, field_to_use)
    window.resize(900, 900)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

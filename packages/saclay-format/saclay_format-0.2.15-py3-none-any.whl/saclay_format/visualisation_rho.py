import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
from skimage import measure
from mpl_toolkits.mplot3d import Axes3D


try:
    import saclay_format as saclay_parser
except ImportError:
    import saclay_parser



def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "input",
        help="Input file (.yaml/.yml or .h5/.hdf5)"
    )
    args = arg_parser.parse_args()

    # Read using the new unified read function
    data = saclay_parser.read(args.input)
 


    print("File read:", args.input)
    print("Keys in data:", list(data))

    nx, ny, nz = data["metadata"]["nx"], data["metadata"]["ny"], data["metadata"]["nz"]
    fields = data["metadata"]["field"]

    rho_n_exists = any(var["name"] == "rho_n" for var in fields)

    if not rho_n_exists:
        print("rho_n not found in metadata fields.")
        exit(0)

    rho_n = data["rho_n"]
    n_frames = data["metadata"].get('frame', 1)
    if n_frames > 1:
        rho_n = rho_n[:, :, :, 0]  # <-- (nx, ny, nz, n_frames)

    # 1D slice along x at center y,z
    x = np.arange(nx)
    rho_slice_1d = rho_n[:, ny // 2, nz // 2]  # <-- updated order


    plt.figure()
    plt.plot(x, rho_slice_1d, marker="o")
    plt.xlabel("x")
    plt.ylabel("rho_n at y=ny//2, z=nz//2")
    plt.title("1D slice: rho_n(x) at center (y,z)")
    plt.grid(True)

    # 2D slice at fixed z = nz//2
    rho_slice_2d = rho_n[:, :, nz // 2]  # <-- updated order
    dx = data["metadata"].get("dx", 1.0)
    dy = data["metadata"].get("dy", 1.0)
    aspect_ratio = dx / dy

    plt.figure()
    plt.imshow(
        rho_slice_2d.T,  # <-- transpose so x→horizontal, y→vertical
        origin="lower",
        extent=[0, nx * dx, 0, ny * dy],
        aspect=aspect_ratio,
    )
    plt.xlabel("x [fm]")
    plt.ylabel("y [fm]")
    plt.title("2D slice: rho_n(x, y) at z=nz//2")
    plt.colorbar(label="rho_n")
    plt.tight_layout()

    # Interpolated 2D slice
    zoom_factor = 4
    rho_interp = zoom(rho_slice_2d, zoom=zoom_factor, order=3)

    plt.figure()
    plt.imshow(
        rho_interp.T,  # <-- transpose for consistency
        origin="lower",
        extent=[0, nx * dx, 0, ny * dy],
        aspect=aspect_ratio,
    )
    plt.xlabel("x [fm]")
    plt.ylabel("y [fm]")
    plt.title("Interpolated 2D slice: rho_n(x, y) at z=nz//2")
    plt.colorbar(label="rho_n")
    plt.tight_layout()

    # 3D voxel plot (thresholded)
    threshold = 0.5 * np.max(rho_n)
    mask = rho_n > threshold

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.voxels(mask, facecolors="blue", edgecolor="k", alpha=0.3)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(f"3D view of rho_n (density > {threshold:.2e})")
    plt.tight_layout()

    # 3D isosurface
    verts, faces, normals, values = measure.marching_cubes(rho_n, level=threshold)
    dx = data["metadata"].get("dx", 1.0)
    dy = data["metadata"].get("dy", 1.0)
    dz = data["metadata"].get("dz", 1.0)

    verts[:, 0] *= dx  # x
    verts[:, 1] *= dy  # y
    verts[:, 2] *= dz  # z

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_trisurf(
        verts[:, 0],
        verts[:, 1],
        faces,
        verts[:, 2],
        cmap="plasma",
        lw=0,
        alpha=1,
        edgecolor="none",
    )
    ax.set_xlabel("X [fm]")
    ax.set_ylabel("Y [fm]")
    ax.set_zlabel("Z [fm]")
    ax.set_title(f"Isosurface at level={threshold:.3f}")
    plt.tight_layout()

    # Interpolated isosurface
    zoom_factor = 3
    rho_n_interp = zoom(rho_n, zoom=zoom_factor, order=3)
    threshold = 0.5 * np.max(rho_n_interp)

    verts, faces, normals, values = measure.marching_cubes(rho_n_interp, level=threshold)
    dx /= zoom_factor
    dy /= zoom_factor
    dz /= zoom_factor

    verts[:, 0] *= dx
    verts[:, 1] *= dy
    verts[:, 2] *= dz

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_trisurf(
        verts[:, 0],
        verts[:, 1],
        faces,
        verts[:, 2],
        cmap="plasma",
        lw=0,
        alpha=1,
        edgecolor="none",
    )
    ax.set_xlabel("X [fm]")
    ax.set_ylabel("Y [fm]")
    ax.set_zlabel("Z [fm]")
    ax.set_title(f"Smooth Isosurface at level={threshold:.3f}")
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()

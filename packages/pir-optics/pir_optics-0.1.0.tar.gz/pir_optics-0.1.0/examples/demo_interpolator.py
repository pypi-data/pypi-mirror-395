# To run:
# uv run examples/demo_interpolator.py
#
import time
import numpy as np
import matplotlib.pyplot as plt
from pir_optics import PixelIrradianceModel

def main():
    start_time = time.perf_counter()
    model = PixelIrradianceModel(
        wavelength=0.365,
        NA_image=0.10,
        mirror_pitch=7.6,
        img_pixel_pitch=27.0,
        pixel_fill=0.80,
        nx=1024,
        dx=0.1,
        auto_compute=True,
        use_cache=False,
    )
    end_time = time.perf_counter()
    print(f"Elapsed time: {(end_time - start_time)*1000:.2f} ms")

    # Scalar sample at the center
    v0 = model[0.0, 0.0]
    print("I(0,0) =", v0)

    # 1D sampling along horizontal line y=0
    half_extent = 100
    x = np.linspace(-half_extent, half_extent, 400)
    y = np.zeros_like(x)
    v1 = model[x, y]

    plt.figure()
    plt.plot(x, v1)
    plt.xlabel("x (µm)")
    plt.ylabel("I(x, 0)")
    plt.title("1D Interpolated Centerline (NA=0.10, λ=0.365 µm)")
    plt.grid(True)

    # 2D sampling on a grid
    X, Y = np.meshgrid(
        np.linspace(-half_extent, half_extent, 200),
        np.linspace(-half_extent, half_extent, 200),
        indexing="xy"
    )
    V = model[X, Y]

    plt.figure()
    plt.imshow(
        V,
        extent=[X.min(), X.max(), Y.min(), Y.max()],
        origin="lower",
        cmap="gray",
        vmax=1.0,
        vmin=0.0,
    )
    plt.colorbar(label="Irradiance")
    plt.xlabel("x (µm)")
    plt.ylabel("y (µm)")
    plt.title("2D Interpolated Irradiance (single pixel)")

    plt.show()

if __name__ == "__main__":
    main()

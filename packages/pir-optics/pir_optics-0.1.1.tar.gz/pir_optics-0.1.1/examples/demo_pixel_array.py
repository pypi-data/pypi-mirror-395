import time
import numpy as np
import matplotlib.pyplot as plt

from pir_optics import PixelIrradianceModel, PixelArrayModel

def example_pixel_array():
    # --- Create single-pixel PIR model ---
    start_time = time.perf_counter()
    pir = PixelIrradianceModel(
        wavelength=0.365,
        NA_image=0.10,
        mirror_pitch=7.6,
        img_pixel_pitch=27.0,
        pixel_fill=0.80,
        nx=1024,
        dx=0.1,
        auto_compute=True,   # compute PSF + single-pixel spot
        use_cache=False,
    )
    end_time = time.perf_counter()
    print(f"PIR calculation elapsed time: {(end_time - start_time)*1000:.2f} ms")

    # --- Create PixelArray ---
    start_time = time.perf_counter()
    pa = PixelArrayModel(
        PIR=pir,
        n_pixels_x=5,
        n_pixels_y=5,
        nx=1024,
        dx=0.2,
    )
    end_time = time.perf_counter()
    print(f"Pixel array calculation elapsed time: {(end_time - start_time)*1000:.2f} ms")
    
    # --- Display result ---
    pa.plot_irradiance_2d()
    pa.plot_centerline()
    plt.show()

if __name__ == "__main__":
    example_pixel_array()

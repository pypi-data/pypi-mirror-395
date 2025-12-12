import marimo

__generated_with = "0.18.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import time
    from pathlib import Path
    import matplotlib.pyplot as plt
    from pir_optics import PixelIrradianceModel, PixelArrayModel
    return PixelArrayModel, PixelIrradianceModel, mo, plt, time


@app.cell
def _(mo):
    # parameters
    wavelength = mo.ui.number(start=0.2, stop=1.0, step=0.005, value=0.365)
    NA = mo.ui.number(start=0.01, stop=0.5, step=0.01, value=0.10)
    mirror_pitch = mo.ui.number(start=2.0, stop=20.0, step=0.1, value=7.6)
    img_pixel_pitch = mo.ui.number(start=5.0, stop=100.0, step=0.1, value=27.0)
    pixel_fill = mo.ui.number(start=0.1, stop=1.0, step=0.01, value=0.80)

    # grid controls
    nx_ctrl = mo.ui.number(start=128, stop=4096, step=1, value=512)
    dx_ctrl = mo.ui.number(start=0.05, stop=1.0, step=0.01, value=0.10)
    return (
        NA,
        dx_ctrl,
        img_pixel_pitch,
        mirror_pitch,
        nx_ctrl,
        pixel_fill,
        wavelength,
    )


@app.cell
def _(
    NA,
    dx_ctrl,
    img_pixel_pitch,
    mirror_pitch,
    mo,
    nx_ctrl,
    pixel_fill,
    wavelength,
):
    grid_size = (nx_ctrl.value - 1) * dx_ctrl.value
    grid_size_display = mo.md(f"{grid_size:.1f}")

    indent_size = 6

    controls = mo.vstack(
        [
            mo.md("### Parameters"),
            mo.hstack([mo.md(f"{indent_size * '&nbsp;'}Wavelength (µm)"), wavelength]),
            mo.hstack([mo.md(f"{indent_size * '&nbsp;'}NA (image side)"), NA]),
            mo.hstack([mo.md(f"{indent_size * '&nbsp;'}Mirror pitch (µm)"), mirror_pitch]),
            mo.hstack([mo.md(f"{indent_size * '&nbsp;'}Image pixel pitch (µm)"), img_pixel_pitch]),
            mo.hstack([mo.md(f"{indent_size * '&nbsp;'}Pixel fill factor"), pixel_fill]),
            mo.md("### Grid settings"),
            mo.hstack([mo.md(f"{indent_size * '&nbsp;'}nx (samples per axis)"), nx_ctrl]),
            mo.hstack([mo.md(f"{indent_size * '&nbsp;'}dx (µm per sample)"), dx_ctrl]),
            mo.hstack([mo.md(f"{indent_size * '&nbsp;'}grid size (µm)"), grid_size_display]),
        ]
    )
    return controls, indent_size


@app.cell
def _(
    NA,
    PixelIrradianceModel,
    controls,
    dx_ctrl,
    img_pixel_pitch,
    indent_size,
    mirror_pitch,
    mo,
    nx_ctrl,
    pixel_fill,
    plt,
    time,
    wavelength,
):
    nx = int(nx_ctrl.value)
    dx = dx_ctrl.value
    pitch = img_pixel_pitch.value

    t0 = time.perf_counter()
    model = PixelIrradianceModel(
        wavelength=wavelength.value,
        NA_image=NA.value,
        mirror_pitch=mirror_pitch.value,
        img_pixel_pitch=pitch,
        pixel_fill=pixel_fill.value,
        nx=nx,
        dx=dx,
        auto_compute=True,
        use_cache=False,
    )
    elapsed = time.perf_counter() - t0


    # --- 2D irradiance plot ---
    fig2d, ax2d = plt.subplots(figsize=(6, 5))
    im = ax2d.imshow(
        model.I,
        extent=[model.x[0], model.x[-1], model.y[0], model.y[-1]],
        origin="lower",
        cmap="gray",
    )
    ax2d.set_xlabel("x (µm)")
    ax2d.set_ylabel("y (µm)")
    ax2d.set_title("Single-pixel irradiance (normalized)")
    fig2d.colorbar(im, ax=ax2d, label="Normalized I")

    # --- 2D PSF ---
    fig_psf, ax_psf = plt.subplots(figsize=(6, 5))
    im_psf = ax_psf.imshow(
        model.psf,
        extent=[model.x[0], model.x[-1], model.y[0], model.y[-1]],
        origin="lower",
        cmap="gray",
    )
    ax_psf.set_xlabel("x (µm)")
    ax_psf.set_ylabel("y (µm)")
    ax_psf.set_title("PSF (normalized)")
    fig_psf.colorbar(im_psf, ax=ax_psf, label="Normalized PSF")

    # --- centerline irradiance ---
    fig1d, ax1d = plt.subplots(figsize=(6, 3))
    ax1d.plot(model.x, model.I[model.ny // 2, :], "k")
    ax1d.plot(model.x, model.ideal_pixel[model.ny // 2, :], "r", linestyle="--")
    ax1d.set_xlabel("x (µm)")
    ax1d.set_ylabel("Normalized irradiance")
    ax1d.set_title("Center-line: irradiance")
    ax1d.set_ylim(-0.05, 1.05)

    # --- centerline PSF ---
    fig1d_psf, ax1d_psf = plt.subplots(figsize=(6, 3))
    ax1d_psf.plot(model.x, model.psf[model.ny // 2, :], "k")
    ax1d_psf.set_xlabel("x (µm)")
    ax1d_psf.set_ylabel("Normalized PSF")
    ax1d_psf.set_title("Center-line: PSF")
    ax1d_psf.set_ylim(-0.05, 1.05)

    # --- layout: controls on top, plots below ---
    top_row = mo.vstack([
        controls,
        mo.md("### Diagnostics"),
        mo.md(f"{indent_size * '&nbsp;'}Computation time: {elapsed*1000:.3f} ms"),
        mo.md(f"{indent_size * '&nbsp;'}Max normalized edge irradiance: {model.max_edge_I:.3e}"),
    ])

    two_d_row = mo.hstack([fig2d, fig_psf])
    centerline_row = mo.hstack([fig1d, fig1d_psf])

    PIR_layout = mo.vstack([
        top_row,
        mo.md("### 2D plots"),
        two_d_row,
        mo.md("### Center-line plots"),
        centerline_row,
    ])
    return PIR_layout, model


@app.cell
def _(mo):
    # Pixel array size
    N_pixels_x = mo.ui.number(
        start=1,
        stop=10,
        step=1,
        value=3,
    )
    M_pixels_y = mo.ui.number(
        start=1,
        stop=10,
        step=1,
        value=3,
    )
    # grid controls
    nx_pixel_array_grid_ctrl = mo.ui.number(
        start=128,
        stop=4096,
        step=1,
        value=512,
    )
    dx_pixel_array_grid_ctrl = mo.ui.number(
        start=0.05,
        stop=1.0,
        step=0.01,
        value=0.25,
    )
    return (
        M_pixels_y,
        N_pixels_x,
        dx_pixel_array_grid_ctrl,
        nx_pixel_array_grid_ctrl,
    )


@app.cell
def _(
    M_pixels_y,
    N_pixels_x,
    dx_pixel_array_grid_ctrl,
    mo,
    nx_pixel_array_grid_ctrl,
):
    grid_size_pixel_array = (nx_pixel_array_grid_ctrl.value - 1) * dx_pixel_array_grid_ctrl.value
    grid_size_pixel_array_display = mo.md(f"{grid_size_pixel_array:.1f}")

    indent_size_pixel_array = 6

    pixel_array_controls = mo.vstack(
        [
            mo.md("### Pixel array size"),
            mo.hstack(
                [
                    mo.md(f"{indent_size_pixel_array * '&nbsp;'}N pixels (x)"),
                    N_pixels_x,
                ]
            ),
            mo.hstack(
                [
                    mo.md(f"{indent_size_pixel_array * '&nbsp;'}M pixels (y)"),
                    M_pixels_y,
                ]
            ),
            mo.md("### Pixel array grid settings"),
            mo.hstack(
                [
                    mo.md(f"{indent_size_pixel_array * '&nbsp;'}nx (samples per axis)"),
                    nx_pixel_array_grid_ctrl,
                ]
            ),
            mo.hstack(
                [
                    mo.md(f"{indent_size_pixel_array * '&nbsp;'}dx (µm per sample)"),
                    dx_pixel_array_grid_ctrl,
                ]
            ),
            mo.hstack(
                [
                    mo.md(f"{indent_size_pixel_array * '&nbsp;'}grid size (µm)"),
                    grid_size_pixel_array_display,
                ]
            ),
        ]
    )
    return (pixel_array_controls,)


@app.cell
def _(
    M_pixels_y,
    N_pixels_x,
    PixelArrayModel,
    dx_pixel_array_grid_ctrl,
    indent_size,
    mo,
    model,
    nx_pixel_array_grid_ctrl,
    pixel_array_controls,
    plt,
    time,
):
    N = int(N_pixels_x.value)
    M = int(M_pixels_y.value)
    nx_pixel_array_grid = int(nx_pixel_array_grid_ctrl.value)

    t1 = time.perf_counter()
    pa_model = PixelArrayModel(
        PIR=model,
        n_pixels_x=N,
        n_pixels_y=M,
        use_image_pixel_pitch=True,
        nx=nx_pixel_array_grid,
        dx=dx_pixel_array_grid_ctrl.value,
    )
    elapsed1 = time.perf_counter() - t1

    # --- 2D irradiance plot ---
    fig2d_px_array, ax2d_px_array = plt.subplots(figsize=(6, 5))
    im_px_array = ax2d_px_array.imshow(
        pa_model.I,
        extent=[pa_model.x[0], pa_model.x[-1], pa_model.y[0], pa_model.y[-1]],
        origin="lower",
        cmap="gray",
    )
    ax2d_px_array.set_xlabel("x (µm)")
    ax2d_px_array.set_ylabel("y (µm)")
    ax2d_px_array.set_title("Single-pixel irradiance (normalized)")
    fig2d_px_array.colorbar(im_px_array, ax=ax2d_px_array, label="Normalized I")

    # --- centerline irradiance ---
    fig1d_px_array, ax1d_px_array = plt.subplots(figsize=(6, 3))
    ax1d_px_array.plot(pa_model.x, pa_model.I[pa_model.ny // 2, :], "k")
    ax1d_px_array.plot(pa_model.x, pa_model.ideal_pixel_array[pa_model.ny // 2, :], "r", linestyle=":")
    ax1d_px_array.set_xlabel("x (µm)")
    ax1d_px_array.set_ylabel("Normalized irradiance")
    ax1d_px_array.set_title("Center-line: irradiance")
    ax1d_px_array.set_ylim(-0.05, None);

    px_array_layout = mo.vstack(
        [
            # mo.md("### Predicted pixel array irradiance"),
            pixel_array_controls,
            mo.md("### Diagnostics"),
            mo.md(f"{indent_size * '&nbsp;'}Computation time: {elapsed1*1000:.3f} ms"),
            mo.vstack([fig2d_px_array, fig1d_px_array]),
        ]
    )
    return (px_array_layout,)


@app.cell
def _(mo):
    from importlib.resources import files
    import pir_optics

    def load_markdown_file():
        """Load markdown file and return as marimo markdown object."""
        content = files(pir_optics).joinpath("docs/PIR_theory_summary.md").read_text()
        return mo.md(content)

    return (load_markdown_file,)


@app.cell
def _(PIR_layout, load_markdown_file, mo, px_array_layout):


    tabs = mo.ui.tabs(
        {
            "PIR Theory": load_markdown_file(),
            "Pixel Impulse Response": PIR_layout,
            "Pixel Array Irradiance": px_array_layout,
        }
    )

    tabs
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

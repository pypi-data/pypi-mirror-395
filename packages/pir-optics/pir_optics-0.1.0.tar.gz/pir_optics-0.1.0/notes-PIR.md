# Purpose

Predict pixel impulse response for given DLP 3D printer optical system parameters. See `PIR_theory_summary.md` for overview, theory, and big-picture implementation details.

# Next

- Save data to npz file with button so it can be analyzed and plotted later? How reasonable is it to use an npz file to fully encapsulate a set of parameters and their result? Or is there a better way?
- Save figures to image files with button?
- Save settings to YAML configuration file?
- ~~App heading at top of page?~~
- Turn into app that can be run in browser (from Github Pages?)
- Put on PyPI?

# Log

## Wed, 12/3/95

### License

Add [BSD 3-Clause Clear License](https://choosealicense.com/licenses/bsd-3-clause-clear/).

### README

Add README.md.

## Tue, 12/2/95

### Refine PIR theory document

- Edit `PIR_theory_summary.md` so that:
    - All LaTex equations render correctly.
    - Clearer Section 1 Purpose.
- Put file in `src/pir_optics/doc` and change read code accordingly so it will be compatible with runing with Pyodide/WASM too.

### Set up as Marimo app with Github Pages

See [ChatGPT discussion](https://chatgpt.com/share/692b5ced-9fb4-800e-a290-eeb07df8d229). Should appear at `https://gregnordin.github.io/pixel_impulse_response_calc/`

Spent hours trying to track down problems. See ChatGPT discussion referenced above. Looks like a marimo bug so no resolution for now.

## Sat, 11/29/25

### Refine marimo notebook UI

- Clean up UI.
- Show ideal pixel linescan with PIR linescan.
- Show normalized irradiance max value on boundary of 2D grid.
- Show 2D grid physical size.

### Start making a 2-tab app for arrays of pixels

See [Marimo app structure](https://chatgpt.com/share/692b5ced-9fb4-800e-a290-eeb07df8d229). Start modifying `notebooks/pixel_spot_app.py` marimo notebook by adding a tab interface with the first tab being my original single-page app and a placeholder image for the 2nd page (i.e., 2nd tab).

### Create pixel array using PIR

See `src/pir_optics/pixel_array.py:PixelArrayModel`.

- Create example code to demonstrate arrays: `examples/demo_pixel_array.py`.
- Add `.plot_irradiance_2d()` and `.plot_centerline()` methods to `PixelArrayModel`.
- Add dotted red line for ideal pixel array center line plot.

### Finish making 2-tab app for arrays of pixels

Use `PixelArrayModel` to finish 2nd tab. Explore different arrangements of grids and PIR parameters. **Rename** to `notebooks/PIR_and_pixel_array.py`. 

```bash
# Run editable notebook
uv run marimo edit notebooks/PIR_and_pixel_array.py
# Run as app
uv run marimo run notebooks/PIR_and_pixel_array.py
```

Lessons:

- **If PIR grid size is too small and the max value on its edges is too large, will get artifact of strange banding in pixel array image**

Add display of `PIR_theory_summary.md` in 3rd tab.

## Thu, 11/27/25

### Reconstitute ChatGPT chat

The chat thread I was using finally choked as it got too big ([Irradiance distribution analysis](https://chatgpt.com/share/691e574e-ed30-800e-9d1d-997b1b67ae19)). Learn how to reconsititute it--see [Upload project as ZIP](https://chatgpt.com/share/692887d6-3d98-800e-9dcf-33754179e013)--which involves creating a **theory summary message** and a ~~**code summary message**~~ `PIR.zip` file.

Create zip file with project directory structure:

```bash
cd ..
rm PIR.zip
zip -r PIR.zip PIR \
  -x "*/.git/*" \
  -x "*/.venv/*" \
  -x "*/__pycache__/*" \
  -x "*.pyc" \
  -x "try1.py" \
  -x "notes-PIR.md" \
  -x "examples/demo_pixel_array_superposition.py" \
  -x "*.DS_Store"
cd PIR
```

#### Theory summary message

See `PIR_theory_summary.md`.

How to use this in future chats (NOTE: I need to explicitly ignore this notes file! &rarr; do not include it in the ZIP file.)

> - This entire block is your theory summary message.
> - In a new chat, you can paste this first so I have the physics/model context.
> - Then you can either:
>     - Re-upload the same ZIP as your “code context” for the current state, or
>     - Paste specific code snippets you want to modify.
>
> You don’t *have* to maintain a separate “code summary” text file if managing the actual project ZIP is easier. The ZIP effectively *is* your code snapshot; a short textual “code structure” summary can help you, but it’s optional from my side as long as you can upload the project when needed.

### Add `[x,y]` access to `PixelIrradianceModel` interpolator

See `src/pir_model/pixel_irradiance.py:PixelIrradianceModel.__get_item__` and `examples/demo_interpolator.py`. Investigate interpolated values outside of xy data range & find they go to zero as expected.

## Wed, 11/26/25

### `PixelIrradianceModel`

- Change `_make_filename` to include all independent parameters so `.npz` filename is unique to a specific case.

- Change `examples/demo_pixel_spot.py` so it calculates and prints the elapsed time to run `PixelIrradianceModel`. For the results below, the runs after the first one take less time because `use_cache=True` so `compute` is just loading an `.npz` file.

    - Results: `nx=512, dx=0.1`: **4.24 ms, 2.11 ms, 2.30 ms**
    - Results: `nx=800, dx=0.1`: **28.70 ms, 3.91 ms, 4.16 ms**
    - Results: `nx=1024, dx=0.1`: **54.98 ms, 9.53 ms, 6.03 ms**
    - Results: `nx=1500, dx=0.1`: **98.89 ms, 10.71 ms, 11.22 ms**

- Change marimo `notebooks/pixel_spot_app.py` to have `nx` and `dx` as inputs and display elapsed time to run `PixelIrradianceModel`.

    `uv run examples/demo_pixel_spot.py`

- Find a problem with how I was running the marimo notebook with `uv` where it was stuck on an old version of my project. This is how it should be run now after fixing `pyproject.toml`:

    `uv run marimo edit notebooks/pixel_spot_app.py`

## Fri, 11/22/25

- Play with xy range for different pixel sizes. Settle on 2 ranges: 0.1 &mu;m sampling for pixel sizes <= 40 &mu;m and 0.2 &mu;m sampling for larger pixel sizes.

#### Superposition to get 5x5 pixel array

`examples/demo_pixel_array_superposition.py`

**Problems:**

- Change PSF to 0.05 and see all of the artifacts. **These need fixed**



## Thu, 11/20/25

- Generalize code to handle user-defined values for wavelength, NA, image pixel pitch, micromirror array pixel pitch, and pixel fill factor.
- Create function to analyze numerical aperture and print relevant values.
- Put code into a class in `src/pir_optics/pixel_irradiance.py`.
- Add marimo notebook example in `notebooks`.



PIR for [Asiga Max X27, 27 um pixel pitch](https://www.asiga.com/max-x/) ([Asiga Ultra](https://www.asiga.com/ultra/) is 32 um pixel pitch):

- DMD: [DLP651NE 0.65-Inch 1080p Digital Micromirror Device](https://www.ti.com/lit/ds/symlink/dlp651ne.pdf)
- [ChatGPT Irradiance Distribution Analysis](https://chatgpt.com/share/691e574e-ed30-800e-9d1d-997b1b67ae19)



Develop PIR for HR3.3u

- Jupyter notebook: `/Users/nordin/Documents/Projects/photopolymerization/development/2024-07-09_v0.2/2024-07-17_pixel_profile_from_images.ipynb`
- PIR image data: `/Users/nordin/Documents/Projects/photopolymerization/development/2024-07-09_v0.2/PIR_3_15_21-LED_powersetting_150`


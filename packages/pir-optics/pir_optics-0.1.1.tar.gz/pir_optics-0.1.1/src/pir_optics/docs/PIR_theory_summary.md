## Pixel Impulse Response — Theory Summary

### 1. Purpose

The Pixel Impulse Response (PIR) computes the **irradiance distribution in the image plane produced by a single “on” pixel** of a DMD-based projection system, taking into account:

- Diffraction from a **circular, diffraction-limited pupil**
- **Incoherent** imaging
- Finite **pixel size and fill factor**
- System geometry defined by DMD pixel pitch and image pixel pitch

The result is a 2D irradiance map $I(x,y)$ in the image plane for a single pixel, which constitutes the optical system PIR. **The image plane irradiance for any arbitrary set of "on" pixels can be predicted by simply summing the PIR of each pixel centered on that pixel's position in the image plane.**

------

### 2. Optical Geometry & Parameters

Image-side parameters (all lengths in microns):

- `wavelength` $\lambda$
- `NA_image` (image-side numerical aperture)
- `mirror_pitch` $p_\text{mir}$: DMD pixel pitch
- `img_pixel_pitch` $p_\text{img}$: pixel pitch at the image plane
- `pixel_fill` $f \in (0,1]$: 2D fill factor (fractional area)

Derived quantities:

- **Magnification**: &nbsp; $M = \frac{p_\text{img}}{p_\text{mir}}$
- **Image-side pixel width** (effective illuminated square in image plane): &nbsp; $w_\text{pix} = p_\text{img}\sqrt{f}$. This is the side length of a square region in the image plane representing one “on” pixel, assuming the same fill factor on object and image sides and a pixel-centered mapping.

The model works entirely in **image-plane coordinates** $(x,y)$, measured in microns.

------

### 3. Mathematical Model

The system is modeled as an **incoherent, shift-invariant** imaging system:

- Object: uniform square pixel
- Point spread function (PSF): Airy intensity pattern for a circular pupil
- Image: convolution of object intensity with PSF

#### 3.1 Image-plane grid

A square, uniformly sampled image-plane grid is used:

- Number of points: `nx × ny`, with `ny = nx`
- Sampling: `dx = dy` (microns)

Coordinates:

$$
 x_i = (i - N/2),dx,\quad
 y_j = (j - N/2),dy,\quad i,j = 0,\dots,N-1
$$

$$
 X, Y = \text{meshgrid}(x, y, \text{indexing='xy'}),\quad
 R = \sqrt{X^2 + Y^2}
$$

This grid is the evaluation domain for both PSF and pixel object.

#### 3.2 Incoherent PSF (Airy pattern)

For a circular, diffraction-limited pupil, the **coherent** amplitude PSF (up to a phase) is proportional to:

$$
 a(r) \propto \frac{2 J_1(z)}{z},\quad
 z = \alpha r,
$$

 where

- $J_1$: Bessel function of the first kind (order 1)
- $k_0 = \frac{2\pi}{\lambda}$
- $\alpha = k_0,\text{NA}*\text{image} = \frac{2\pi}{\lambda},\text{NA}*\text{image}$
- $r = \sqrt{x^2 + y^2}$

The **incoherent** PSF is the intensity:

$$
 h(r) = \left|\frac{2J_1(z)}{z}\right|^2
$$

In the implementation:

- $z = \alpha R$
- For $z \neq 0$: $\text{psf}(R) = \left(\frac{2J_1(z)}{z}\right)^2$
  
- For $z = 0$: limit is **1**, so psf is explicitly set to 1 at the center to avoid (0/0).

The PSF is normalized so total energy is 1:

$$
 \sum_{i,j}\text{psf}_{ij},dx,dy = 1
$$

The result is stored as `self.psf`.

Useful scale (not directly needed for the computation but used in diagnostics):

$$
 \Delta x_\text{Rayleigh,img} \approx 0.61 \frac{\lambda}{\text{NA}_\text{image}}
$$

------

#### 3.3 Pixel object (single “on” pixel)

The pixel is modeled as a **uniform square** in the image plane:

$$
 \text{obj}(x,y) =
 \begin{cases}
 1, & |x| \le \frac{w_\text{pix}}{2},\quad |y| \le \frac{w_\text{pix}}{2}\
 0, & \text{otherwise}
 \end{cases}
$$

Implemented as:

```python
obj = ((|X| <= w_pix/2) & (|Y| <= w_pix/2)).astype(float)
```

This is the image-plane representation of one “on” pixel with the given fill factor.

------

#### 3.4 Incoherent imaging: convolution

The image intensity from a single pixel is the **convolution** of the pixel object with the PSF:

$$
 I(x,y) = (\text{obj} * \text{psf})(x,y)
$$

Numerically, this is implemented with FFT-based convolution:

1. Shift `obj` and `psf` so that their centers align with the FFT convention using `ifftshift`.
2. Compute FFTs: &nbsp; $\mathcal{F}{\text{obj}} \cdot \mathcal{F}{\text{psf}}$
3. Inverse FFT: &nbsp; $I = \mathcal{F}^{-1}\left(\mathcal{F}{\text{obj}}\cdot\mathcal{F}{\text{psf}}\right)$
4. Shift back with `fftshift` so the origin (pixel center) is in the center of the array.
5. Take the real part (imaginary components are numerical noise).
6. Normalize:  &nbsp; $I \leftarrow I / \max(I)$ &nbsp; so that the peak irradiance is 1.

This gives a **dimensionless irradiance map** `self.I` which captures the shape of the single-pixel spot, not its absolute power scaling. We call this the system's **Pixel Impulse Response (PIR)**.

------

### 4. Sampling / NA Diagnostics

The model computes a few diagnostic quantities to help understand the regime:

- Image-plane Rayleigh resolution: &nbsp; $\Delta x_\text{img} = 0.61 \frac{\lambda}{\text{NA}_\text{image}}$
- Ratio of image pixel pitch to Rayleigh resolution: &nbsp; $\text{ratio} = \frac{p_\text{img}}{\Delta x_\text{img}}$. 
     This indicates whether the **pixel is much larger than the diffraction blur** (ratio ≫ 1) or comparable to it (ratio ≈ 1).
- Minimum NA needed to resolve the image pixel pitch: &nbsp; $\text{NA}_{\text{min}} = 0.61 \frac{\lambda}{p_{\text{img}}}$
- Object-side NA: &nbsp; $\text{NA}_\text{obj} = \frac{\text{NA}_\text{image}}{M}$
  
     and corresponding object-side Rayleigh resolution: &nbsp; $\Delta x_\text{obj} = 0.61 \frac{\lambda}{\text{NA}_\text{obj}}$

These are printed as text for quick interpretation of the regime (e.g., “pixel much larger than diffraction spot”).

------

### 5. DMD Grating / Order Check (Sanity)

Treating the DMD as a 1D grating of period $d = p_\text{mir}$:

- First-order diffraction angle: &nbsp; $\theta_1 = \arcsin\left(\min(1, \lambda / d)\right)$
- Lens semi-angle defined by NA: &nbsp; $\theta_\text{lens} = \arcsin(\min(1, \text{NA}_\text{image}))$

Comparing $\theta_1$ and $\theta_\text{lens}$ gives a rough sense of which DMD orders could fall into the pupil, depending on the off-axis design. This is **diagnostic only**; the current PIR model itself uses the **zero-order Airy PSF** and does not explicitly model off-axis order selection.

------

### 6. Accessing the Irradiance

The model provides:

- 2D irradiance array `I(x,y)` on the regular grid.
- Convenience plotting:
    - `plot_irradiance_2d()` — 2D grayscale map of the spot.
    - `plot_centerline()` — 1D line profile along the central horizontal line.
- An interpolator `irradiance(x,y)` built with `RegularGridInterpolator` for continuous evaluation in microns within the grid extent. This is also available by indexing an instance of `PixelIrradianceModel` as `pir[x,y]`, which is effectively a shorthand for `pir.irradiance(x,y)`.

------

### 7. Key Assumptions & Limitations

- Scalar diffraction; polarization ignored.
- Perfectly incoherent illumination (image = convolution of object intensity with PSF).
- Diffraction-limited, aberration-free circular pupil.
- Single pixel modeled as a **perfectly uniform square** of width $w_\text{pix} = p_\text{img}\sqrt{f}$.
- No temporal or spectral bandwidth (single wavelength).
- No explicit modeling of off-axis DMD orders in the PSF; order effects only appear via the printed diagnostics.

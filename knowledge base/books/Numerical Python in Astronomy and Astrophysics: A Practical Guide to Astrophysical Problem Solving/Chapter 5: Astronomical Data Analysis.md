我来将这份PDF文档（第5章）的内容转换为Markdown格式：

```markdown
# Chapter 5: Astronomical Data Analysis

**Abstract:** Astronomy and astrophysics are highly data-driven research fields: Hypotheses are built upon existing data, models are used to make predictions and discrepancies between theory and observation drive scientific progress, forcing us to either modify existing models or come up with new solutions. In this chapter, we discuss techniques for analysing a variety of data, ranging from individual stellar spectra and light curves to large surveys, such as GAIA. Naturally, file input and output are an important prerequisite for data processing. We conclude with a brief introduction to convolutional neural networks and their application to image data and spectra.

---

## 5.1 Spectral Analysis

In Chap. 3, we discussed how stars can be classified by spectral properties. Modern spectrographs can produce spectra with high wavelength resolution, which allows for the detailed analysis of absorption lines. As an example, the online material for this book includes an optical spectrum of the star ζ Persei taken with the Ultraviolet and Visual Echelle Spectrograph (UVES) of ESO.

The spectrum is stored in the **FITS file format**, which can be considered a de-facto standard for astronomical data. In contrast to plain text (ASCII) based formats, FITS files are binary, which reduces the operational overhead during read and write processes. Furthermore, every FITS file contains a header with a detailed description of the data and its format. This information is called **metadata**.

Thanks to the Astropy library, FITS files can be accessed with just a few lines of code. Tools for handling FITS files are provided by the module `astropy.io.fits`:

```python
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

file = "data_files/ADP.2014-10-29T09_42_08.747.fits"
fits_data = fits.open(file)
```

This code prompts the metadata of the file:

```
Filename: ADP.2014-10-29T09_42_08.747.fits
No.    Name      Ver    Type         Cards   Dimensions   Format
0      PRIMARY   1      PrimaryHDU   788     ()           
1      SPECTRUM  1      BinTableHDU  71      1R x 6C      [134944D, 134944E, ...]
```

The second HDU contains the full spectrum, which is tabulated in six columns. For a more detailed description:

```python
print(fits_data[1].columns)
```

Output:
```
ColDefs(
    name = 'WAVE'; format = '134944D'; unit = 'Angstrom'
    name = 'FLUX_REDUCED'; format = '134944E'; unit = 'adu'
    name = 'ERR_REDUCED'; format = '134944E'; unit = 'adu'
    name = 'BGFLUX_REDUCED'; format = '134944E'; unit = 'adu'
    name = 'FLUX'; format = '134944E'; unit = '10^-16 erg/cm^2/s/Angstrom'
    name = 'ERR'; format = '134944E'; unit = '10^-16 erg/cm^2/s/Angstrom'
)
```

We are interested in columns 0 and 4 (wavelength and flux). Extract the data:

```python
scidata = fits_data[1].data
fits_data.close()

wavelength = scidata[0][0]
flux = scidata[0][4]

# Normalize and convert units
norm = np.max(flux)
flux = flux / norm
wavelength = wavelength / 10  # Angstrom to nm

# Plot
%matplotlib inline
plt.plot(wavelength, flux, linestyle='-', color='navy')
plt.xlabel("$\lambda$/nm")
plt.ylabel("Flux / ADU")
plt.xlim(587, 590)
```

![Helium and sodium absorption lines in spectrum of ζ Persei](figure_5_1.png)

**Figure 5.1:** Helium and sodium absorption lines in spectrum of ζ Persei

The plot shows the spectrum of ζ Persei in the wavelength range from 587 to 590 nm. Since ζ Persei is a B-type supergiant with an effective temperature of 20800 K, helium absorption lines such as the broad line at 587.6 nm can be seen. However, the two narrow lines at 589.0 and 589.6 nm originate from **sodium in the interstellar medium (ISM)**. These lines were discovered in spectroscopic binary stars by Mary L. Heger in 1919.

### Exercises

**5.1** Investigate the spectrum of ζ Persei in the wavelength range from 480 to 660 nm. Use `plt.axvline()` to mark the Balmer absorption lines Hα and Hβ at wavelengths 656.3 and 486.1 nm, respectively. Identify the absorption lines of He I at wavelengths 471.3, 492.1, 501.6, 504.7, 587.6, and 667.8 nm.

**5.2** Devise an algorithm to estimate the **full width at half-maximum (FWHM)**, $\lambda_{1/2}$, of the helium and sodium absorption lines. Assuming thermal Doppler broadening:

$$\lambda_{1/2} = \frac{2\lambda}{c}\sqrt{\frac{2kT\log 2}{m}}$$

where $k$ is the Boltzmann constant, $c$ the speed of light, and $m$ the mass of the atoms. Which temperatures are implied and what do your results suggest about the origin of the sodium lines?

---

## 5.2 Transit Light Curves

The last three decades have seen a dramatic revolution in our understanding of planetary systems. As of fall 2020, about 4,300 confirmed exoplanets in more than 3,000 stellar systems have been found. The majority has been detected via **planetary transits** or periodic variations of a star's radial velocity.

When the orbital plane of an exoplanet happens to be nearly aligned with the line of sight from Earth, the exoplanet passes between us and its hosting star, causing it to block a fraction of the light:

$$\frac{\Delta F}{F} = \left(\frac{R_P}{R_S}\right)^2$$

For a Jovian planet orbiting a solar-like star, $R_P/R_S \approx 0.1$, implying that only 1% of the star's light will be blocked.

### TrES-2b Light Curve Analysis

The ASCII file `tres2_data.dat` contains three columns: modified Julian date (MJD), relative flux, and flux error.

```python
import numpy as np

data = np.loadtxt("tres2_data.dat")

mjd = data[:, 0]
flux = data[:, 1]
err = data[:, 2]

# Plot with error bars
import matplotlib.pyplot as plt
%matplotlib inline

plt.errorbar(mjd, flux, yerr=err, ecolor='steelblue',
             linestyle='none', marker='o', color='navy')
plt.xlabel("MJD")
plt.ylabel("Flux / ADU")
```

![Light curve of a transit of TrES-2b](figure_5_4.png)

**Figure 5.4:** Light curve of a transit of TrES-2b observed from Hamburg on July 6th, 2013

Estimate ingress and egress times:

```python
T1 = 5.645e4 + 0.445  # ingress
T4 = 5.645e4 + 0.520  # egress

# Calculate normalization from out-of-transit data
norm1 = np.mean(flux[mjd < T1])      # before transit
norm2 = np.mean(flux[mjd > T4])      # after transit
norm = 0.5 * (norm1 + norm2)

print(f"Flux normalization factor: {norm:.3f}")

# Normalize
flux /= norm
err /= norm
```

**Moving average smoothing:**

```python
# Width and offset of sample window
offset = 7
width = 2 * offset + 1  # N = 15

# Compute moving average
flux_smoothed = np.ones(flux.size - width + 1)
for i, val in enumerate(flux_smoothed):
    flux_smoothed[i] = np.sum(flux[i:i+width]) / width

flux_min = np.min(flux_smoothed)
print(f"Minimum flux: {flux_min:.3f}")
```

Plot the smoothed light curve:

```python
plt.errorbar(mjd, flux, yerr=err, ecolor='steelblue',
             linestyle='none', marker='o', color='navy', zorder=1)
plt.xlim(np.min(mjd), np.max(mjd))
plt.xlabel("MJD")
plt.ylabel("rel. flux")

# Smoothed flux
plt.plot(mjd[offset:-offset], flux_smoothed,
         lw=2, color='orange', zorder=2)

# Mark ingress, egress, and minimum flux
plt.axvline(T1, color='crimson', lw=1, linestyle=':')
plt.axvline(T4, color='crimson', lw=1, linestyle=':')
plt.axhline(flux_min, lw=1, linestyle='--', color='black')

plt.savefig("tres2_lightcurve_smooth.pdf")
```

![Smoothed light curve](figure_5_5.png)

**Figure 5.5:** Smoothed light curve computed from the data points

The result, $\Delta F/F \approx 1 - 0.985 = 0.015$, allows us to calculate the star-planet radius ratio: $R_P/R_S \approx 0.12$.

### Planet Radius from Transit Parameters

Assuming the orbital plane is aligned with the line of sight:

$$\sin\left(\frac{\pi T_{\text{trans}}}{P}\right) = \frac{R_S + R_P}{a}$$

For small angles, the approximate relation for the planet radius is:

$$R_P \simeq a \frac{\pi T_{\text{trans}}}{P}\left(1 + \sqrt{\frac{F}{\Delta F}}\right)^{-1}$$

The semi-major axis from Kepler's third law:

$$\frac{a}{1\text{ AU}} = \left(\frac{M_S}{M_\odot}\right)^{1/3}\left(\frac{P}{365.25\text{ d}}\right)^{2/3}$$

For TrES-2b: $M_S = 0.98 M_\odot$, $a = 0.0355$ AU, yielding $R_P \approx 0.8 R_{\text{Jup}}$ (improved model gives $R_P \approx 1.27 R_{\text{Jup}}$).

### Exercises

**5.3** Write a Python function that performs the computation for given start/end times of the transit and window width. 
- (a) Vary tuning parameters and analyze sensitivity of $\Delta F/F$.
- (b) Devise a criterion to exclude extreme outliers.

**5.4** Improved transit model with inclination:
$$R_P = a\sqrt{1 - \sin i \cos\left(\frac{2\pi T_{\text{trans}}}{P}\right)}\left(1 + \sqrt{\frac{F}{\Delta F}}\right)^{-1}$$

For TrES-2: $i = 83.6°$. Apply the improved model to compute $R_P$.

---

## 5.3 Survey Data Sets

### GAIA Mission Data

The GAIA mission has measured basic properties of more than a billion stars. Data can be accessed via the GAIA archive using **ADQL** (Astronomical Data Query Language), which extends SQL.

Example query:
```sql
SELECT l, b, parallax, parallax_over_error, radial_velocity, phot_g_mean_mag 
FROM gaiadr2.gaia_source 
WHERE phot_g_mean_mag < 12 
  AND ABS(radial_velocity) > 0 
  AND parallax >= 1.0 
  AND parallax_over_error >= 10
```

This selects ~1.4 million objects. Download in CSV format (~130 MB).

### Loading and Analyzing GAIA Data

```python
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("gaia_12mag_1kpc-result.csv",
                  dtype='float64', usecols=(0, 1, 2, 4),
                  delimiter=',', skiprows=1)

print(data.shape)  # (1386484, 4)
```

**Distance distribution:**

```python
# Distance from parallax (parallax in mas -> distance in kpc)
d = 1.0 / data[:, 2]

fig = plt.figure(figsize=(6, 4), dpi=300)
plt.hist(d, 100)
plt.xlabel('$d$ / kpc')
plt.ylabel('$N$')
plt.savefig('d_histogram.png')
```

![Distribution of distances](figure_5_7.png)

**Figure 5.7:** Distribution of distances in a sample of 1.4 million stars

**Radial velocity distribution:**

```python
bin_width = 2.5  # in km/s
rv_lim = 140
bins = np.arange(-rv_lim, rv_lim + bin_width, bin_width)

fig = plt.figure(figsize=(6, 4), dpi=300)
rv_histogram = plt.hist(data[:, 3], bins=bins)
plt.xlabel('radial velocity / km/s')
plt.ylabel('N')
plt.savefig('rv_histogram.png')
```

### Gaussian Fit to Velocity Distribution

The radial velocity distribution appears Gaussian:

$$y(x) = y_0 \exp\left(-\frac{(x-x_0)^2}{2\sigma^2}\right)$$

```python
# Bin centers
x = bins[:-1] + bin_width / 2
y = rv_histogram[0]

import scipy.optimize as opt

def gaussian(x, y0, x0, sigma_sqr):
    return y0 * np.exp(-(x - x0)**2 / (2 * sigma_sqr))

params, params_covariance = opt.curve_fit(gaussian, x, y)
print("Parameters best-fit:", params)

# Plot fit
y_gauss = gaussian(x, params[0], params[1], params[2])
plt.hist(data[:, 3], bins=bins)
plt.plot(x, y_gauss, color='red')
```

![Radial velocity distribution and Gaussian fit](figure_5_9.png)

**Figure 5.9:** Radial velocity distribution and best-fit Gaussian (red line)

### Kolmogorov-Smirnov Test

```python
from scipy.stats import ks_2samp

ks_2samp(y, y_gauss)
```

Result: `KstestResult(statistic=0.295, pvalue=0.0001)`

The very small p-value (~0.01%) indicates that the distribution shows systematic deviations from a pure Gaussian.

### Spatial Distribution of Radial Velocities

```python
rv = data[:, 3]
redshift, blueshift = data[rv > 0], data[rv <= 0]

print("Redshifted stars:", len(redshift))
print("Blueshifted stars:", len(blueshift))

# Scatter plot
fig = plt.figure(figsize=(10, 10*60/360+1), dpi=300)
ax = fig.add_subplot(111)

step = 10  # Plot every 10th star

plt.scatter(blueshift[::step, 0], blueshift[::step, 1],
            s=1, marker='.', color='blue', alpha=0.1)
plt.scatter(redshift[::step, 0], redshift[::step, 1],
            s=1, marker='.', color='red', alpha=0.1)

plt.xlabel('longitude [deg]')
plt.ylabel('lat. [deg]')
plt.xlim(0, 360)
plt.ylim(-30, 30)
ax.set_aspect('equal')
```

![Distribution of blue- and redshifted stars](figure_5_10.png)

**Figure 5.10:** Distribution of blue- and redshifted stars in the $l$-$b$-plane

### Exercises

**5.5** Compute mean values and standard deviations of radial velocity for 5° bins of galactic longitude. Interpret trends assuming a flat galactic rotation curve.

**5.6** **Oort's formula:** For $d \ll R_0 \approx 8.5$ kpc:
$$\frac{v_r}{d} = A \sin(2l)$$
where $A = 14.8$ km s⁻¹ kpc⁻¹.

- (a) Create scatter plot of $v_{rad}/d$ vs. $l$ for stars closer than $0.05R_0$.
- (b) Fit Oort's formula and determine best-fit value of $A$.

---

## 5.4 Image Processing

Online access to images from space telescopes is provided by the **Barbara A. Mikulski Archive for Space Telescopes (MAST)** of NASA, including Hubble Space Telescope (HST) data.

### M51 Whirlpool Galaxy

Download images from three filters:
- Blue (435 nm): `h_m51_b_s20_drz_sci.fits`
- Green/Visual (555 nm): `h_m51_v_s20_drz_sci.fits`  
- Red/Hα (658 nm): `h_m51_h_s20_drz_sci.fits`

```python
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Load red channel
m51r_file = "h_m51_h_s20_drz_sci.fits"
m51r = fits.open(m51r_file)
print(m51r.info())
m51r_data = m51r[0].data
m51r.close()

# Histogram of image data
plt.hist(m51r_data.flatten(), log=True, bins=100)
plt.xlabel('Signal')
plt.ylabel('N')
```

![Distribution of values in M51 red-channel image](figure_5_11.png)

**Figure 5.11:** Distribution of values in the M51 red-channel image

Display monochromatic image:

```python
plt.imshow(m51r_data, cmap='gray')
plt.clim(0, 0.1)
plt.colorbar()
```

![Monochromatic image of M51](figure_5_12.png)

**Figure 5.12:** Monochromatic image of M51 in the red (Hα) channel

### Creating RGB Composite Image

```python
# Load all channels
m51g_file = "h_m51_v_s20_drz_sci.fits"
m51g = fits.open(m51g_file)
m51g_data = m51g[0].data
m51g.close()

m51b_file = "h_m51_b_s20_drz_sci.fits"
m51b = fits.open(m51b_file)
m51b_data = m51b[0].data
m51b.close()

# Create RGB array
alpha = 0.15  # brightness factor

m51rgb = np.zeros([2150, 3050, 3])

m51rgb[:, :, 0] = m51r_data.transpose() / np.mean(m51r_data)
m51rgb[:, :, 1] = m51g_data.transpose() / np.mean(m51g_data)
m51rgb[:, :, 2] = m51b_data.transpose() / np.mean(m51b_data)

m51rgb *= 255 * alpha

# Clip at 255
m51rgb = np.where(m51rgb > 255, 255, m51rgb)

# Convert to image
from PIL import Image

img = Image.fromarray(m51rgb.astype(np.uint8))
img.show()
img.save("m51_rgb.png")
```

![RGB image of M51](figure_5_13.png)

**Figure 5.13:** RGB image of M51 composed from HST image data from three different filters

### Exercise

**5.7** Experiment with the fudge factor `alpha` and the normalization of image data. How does it affect the resulting image of M51?

---

## 5.5 Machine Learning

Neural networks are algorithms that can be trained by presenting data to them. The training process enables the network to find features, correlations, structures, etc. when confronted with new data.

**Convolutional Neural Networks (CNNs):**
- Input layer: pixel values
- Convolutional layers: apply convolution filters (small windows sliding through image)
- Pooling layers: downsampling
- Fully connected dense layers: classification
- Output layer: class probabilities

Modern APIs such as **TensorFlow** and **Keras** make setting up neural networks straightforward.

### 5.5.1 Image Classification: Galaxy Morphology

Goal: Classify galaxies as elliptical, spiral, or irregular using the EFIGI catalogue.

```python
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as image
import tensorflow as tf
from tensorflow import keras

# Load data file list
data = open("data_files/galaxies/efigi.dat", "r")

names = []
types = []

for line in data:
    fields = line.split(" ")
    names.append(fields[0])
    types.append(fields[1])

nData = len(names)
imgSize = 64  # Resize to 64x64

# Load and preprocess images
galaxies = np.zeros((nData, imgSize, imgSize, 3))
labels = np.zeros(nData, dtype='int')

for i in range(nData):
    img = image.open("data_files/galaxies/png/" + str(names[i]) + ".png")
    imgResized = img.resize(size=(imgSize, imgSize))
    galaxies[i, :, :, :] = np.array(imgResized) / 255
    labels[i] = types[i]
```

**Split into training, validation, and test sets:**

```python
import random

# 70% training, 15% validation, 15% test
size = labels.size
sample = random.sample([n for n in range(size)], int(0.3 * size))

otherLabels = labels[sample]
otherGalaxies = galaxies[sample, :, :, :]
trainLabels = np.delete(labels, sample)
trainGalaxies = np.delete(galaxies, sample, axis=0)

# Split remainder into validation and test
size = otherLabels.size
subsample = random.sample([n for n in range(size)], int(size / 2))

valdLabels = otherLabels[subsample]
valdGalaxies = otherGalaxies[subsample, :, :, :]
testLabels = np.delete(otherLabels, subsample)
testGalaxies = np.delete(otherGalaxies, subsample, axis=0)
```

**Create CNN:**

```python
galNet = keras.Sequential([
    keras.layers.Conv2D(96, (8, 8), activation='relu',
                        input_shape=(imgSize, imgSize, 3)),
    keras.layers.MaxPooling2D(pool_size=(4, 4)),
    keras.layers.Flatten(),
    keras.layers.Dense(30, activation='relu'),
    keras.layers.Dense(3, activation='softmax')
])

galNet.summary()
```

**Compile and train:**

```python
galNet.compile(optimizer='adam',
               loss='sparse_categorical_crossentropy',
               metrics=['accuracy'])

results = galNet.fit(trainGalaxies, trainLabels, epochs=40,
                     validation_data=(valdGalaxies, valdLabels))
```

**Plot training history:**

```python
plt.figure(figsize=(6, 4), dpi=100)
plt.plot(results.history['loss'], color='green', label='training')
plt.plot(results.history['val_loss'], color='red', label='validation')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
```

![Loss curves showing overfitting](figure_5_15_top.png)

**Figure 5.15 (top):** Loss curves showing overfitting with 96 feature maps

**Improved network with dropout:**

```python
galNet = keras.Sequential([
    keras.layers.Conv2D(32, (8, 8), activation='relu',
                        input_shape=(imgSize, imgSize, 3)),
    keras.layers.MaxPooling2D(pool_size=(4, 4)),
    keras.layers.Flatten(),
    keras.layers.Dropout(0.3),  # Randomly deactivate 30% of neurons
    keras.layers.Dense(24, activation='relu'),
    keras.layers.Dense(3, activation='softmax')
])
```

![Loss curves with dropout](figure_5_15_bottom.png)

**Figure 5.15 (bottom):** Loss curves with reduced overfitting using 32 feature maps and dropout layer

**Evaluate on test set:**

```python
loss, acc = galNet.evaluate(testGalaxies, testLabels)
# Result: ~86% accuracy
```

**Predict on new image:**

```python
img = image.open("data_files/galaxies/NGC_1232.jpg")
imgResized = img.resize(size=(imgSize, imgSize))
imgArr = np.array(imgResized) / 255
imgArrExp = np.expand_dims(imgArr, axis=0)

pred = galNet.predict(imgArrExp)

label = ["elliptical", "spiral", "irregular"]
for i, p in enumerate(pred.flatten()):
    print(f"{label[i]:10s} {p:.4e}")

# Output: spiral ~99.6% probability
```

### 5.5.2 Spectral Classification: Stellar Temperatures

Goal: Derive effective temperature from stellar spectrum using ~80,000 synthetic spectra with noise.

```python
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from os import listdir
from os.path import isfile, join

path = "specnet/training"
specnames = [f for f in listdir(path) if isfile(join(path, f))]

n_spectra = len(specnames)
print("Total number of training spectra:", n_spectra)
# Output: 79200

# Extract temperatures from filenames
temp = np.zeros(n_spectra, dtype='int')
for i, spec in enumerate(specnames):
    temp[i] = int(spec[0:4])

temp_class = sorted(list(set(temp)))
n_labels = len(temp_class)
print("Temperature classes:", temp_class)
# [4000, 4200, 4400, 4600, 4800, 5000, 5200, 5400, 5600, 5800, 6000]
```

**Load and reshape spectra:**

```python
n_channels = 20
channel_length = int(spec_size / n_channels)  # 425

labels = np.zeros(n_spectra, dtype='int')
spectra = np.zeros((n_spectra, channel_length, n_channels), dtype='float64')

for i in range(n_spectra):
    labels[i] = temp_class.index(temp[i])
    spectrum_file = join(path, specnames[i])
    spec_arr = np.load(spectrum_file)
    flux = spec_arr["arr_0"][:, 1]
    flux_2d = np.reshape(flux, (-1, n_channels))
    spectra[i, :, :] = flux_2d
```

**Create 1D CNN:**

```python
specNet = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(24, 4, activation='relu',
                           input_shape=(channel_length, n_channels)),
    tf.keras.layers.Conv1D(120, 10, activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(n_labels, activation='softmax'),
])

specNet.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

specNet.fit(spectra, labels, epochs=4)
```

Training reaches ~100% accuracy in 4 epochs.

**Test on solar spectrum:**

```python
spectrum_file = "data_files/sun_spec.npz"
spec_arr = np.load(spectrum_file)
flux = spec_arr["arr_0"][:, 1]
flux_2d = np.reshape(flux, (-1, n_channels))

guess = specNet.predict(np.expand_dims(flux_2d, axis=0))

for i in range(n_labels):
    print(f"{temp_class[i]:4d}K {100*guess[0,i]:6.2f}%")

# Output: 5800K ~98.8% (Sun's actual T_eff = 5780K)
```

**Save and load model:**

```python
# Save
specNet.save('data_files/specnet_model.tf', save_format='tf')

# Load later
specNet = keras.models.load_model('data_files/specnet_model.tf')
```

### Exercises

**5.8** Improve `galNet` by varying network parameters, using larger image size, or adding convolutional layers. Test on web-found galaxy images.

**5.9** Use spectral classes (Morgan-Keenan system) instead of temperatures. Train network to identify classes. Investigate sensitivity on filter parameters. Use GPU if available:

```python
with tf.device('/gpu:0'):
    specNet.fit(spectra, labels, epochs=4)
```

---

## Summary Tables

**Table 5.1:** Spectral classes and effective temperatures of G- and K-type main sequence stars

| Class | T_eff [K] |
|-------|-----------|
| G0    | 5980      |
| G2    | 5800      |
| G5    | 5620      |
| G9    | 5370      |
| K0    | 5230      |
| K1    | 5080      |
| K3    | 4810      |
| K4    | 4640      |
| K5    | 4350      |
| K7    | 4150      |

---

This chapter covered:
- **FITS file I/O** with `astropy.io.fits`
- **Spectral analysis**: absorption lines, Doppler broadening
- **Light curve analysis**: exoplanet transits, moving averages
- **Survey data**: GAIA archive, ADQL queries, histograms, Gaussian fitting, K-S test
- **Image processing**: RGB composition from multi-filter data
- **Machine learning**: CNNs for galaxy classification (2D) and stellar temperature estimation (1D spectra)
```
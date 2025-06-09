import os
import numpy as np
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

# Define base path
base_path = r"C:\Define Your Base Path"

# Define filenames
bands = {
    "blue": "Blue_Band.tif",
    "green": "Green_Band.tif",
    "red": "Red_Band.tif",
    "re": "RedEdge_Band.tif",
    "nir": "NearInfrared_Band.tif"
}

# Load bands
def load_band(filepath):
    with rasterio.open(filepath) as src:
        return src.read(1), src.profile

blue, profile = load_band(os.path.join(base_path, bands["blue"]))
green, _ = load_band(os.path.join(base_path, bands["green"]))
red, _ = load_band(os.path.join(base_path, bands["red"]))
re, _ = load_band(os.path.join(base_path, bands["re"]))
nir, _ = load_band(os.path.join(base_path, bands["nir"]))

# Compute NDVI
ndvi = (nir - red) / (nir + red)
ndvi[np.isinf(ndvi)] = np.nan

# Threshold
ndvi_threshold = 0.8 # Adjust the threshold based on NDVI of your area
vegetation_mask = ndvi > ndvi_threshold
soil_mask = ndvi <= ndvi_threshold

# Apply mask function
def apply_mask(band, mask):
    result = np.where(mask, band, np.nan)
    return result

# Vegetation bands
blue_veg = apply_mask(blue, vegetation_mask)
green_veg = apply_mask(green, vegetation_mask)
red_veg = apply_mask(red, vegetation_mask)
re_veg = apply_mask(re, vegetation_mask)
nir_veg = apply_mask(nir, vegetation_mask)

# Soil bands
blue_soil = apply_mask(blue, soil_mask)
green_soil = apply_mask(green, soil_mask)
red_soil = apply_mask(red, soil_mask)
re_soil = apply_mask(re, soil_mask)
nir_soil = apply_mask(nir, soil_mask)

# Save rasters
def save_raster(output_path, data, base_profile):
    base_profile.update(dtype=rasterio.float32, nodata=np.nan)
    with rasterio.open(output_path, 'w', **base_profile) as dst:
        dst.write(data.astype(np.float32), 1)

save_raster(os.path.join(base_path, "blue_vegetation.tif"), blue_veg, profile)
save_raster(os.path.join(base_path, "green_vegetation.tif"), green_veg, profile)
save_raster(os.path.join(base_path, "red_vegetation.tif"), red_veg, profile)
save_raster(os.path.join(base_path, "rededge_vegetation.tif"), re_veg, profile)
save_raster(os.path.join(base_path, "nir_vegetation.tif"), nir_veg, profile)

save_raster(os.path.join(base_path, "blue_soil.tif"), blue_soil, profile)
save_raster(os.path.join(base_path, "green_soil.tif"), green_soil, profile)
save_raster(os.path.join(base_path, "red_soil.tif"), red_soil, profile)
save_raster(os.path.join(base_path, "rededge_soil.tif"), re_soil, profile)
save_raster(os.path.join(base_path, "nir_soil.tif"), nir_soil, profile)

# Plotting
fig, axs = plt.subplots(4, 3, figsize=(14, 12))
axs = axs.flatten()

axs[0].set_title("NDVI Map")
show(ndvi, ax=axs[0], cmap='RdYlGn')

axs[1].set_title("Blue Band (Vegetation)")
show(blue_veg, ax=axs[1], cmap='Blues')

axs[2].set_title("Blue Band (Soil)")
show(blue_soil, ax=axs[2], cmap='Blues')

axs[3].set_title("Green Band (Vegetation)")
show(green_veg, ax=axs[3], cmap='Greens')

axs[4].set_title("Green Band (Soil)")
show(green_soil, ax=axs[4], cmap='Greens')

axs[5].set_title("Red Band (Vegetation)")
show(red_veg, ax=axs[5], cmap='Reds')

axs[6].set_title("Red Band (Soil)")
show(red_soil, ax=axs[6], cmap='Reds')

axs[7].set_title("Red-edge Band (Vegetation)")
show(re_veg, ax=axs[7], cmap='PuRd')

axs[8].set_title("Red-edge Band (Soil)")
show(re_soil, ax=axs[8], cmap='PuRd')

axs[9].set_title("NIR Band (Vegetation)")
show(nir_veg, ax=axs[9], cmap='inferno')

axs[10].set_title("NIR Band (Soil)")
show(nir_soil, ax=axs[10], cmap='inferno')

for ax in axs[11:]:
    ax.axis('off')

plt.tight_layout()
plt.show()

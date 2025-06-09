# Vegetation_and_Soil_Mask

Vegetation and Soil Mask Separation

Description:

This Python script is designed specifically for processing multispectral drone imagery. It reads five spectral bands (Blue, Green, Red, Red-edge, and NIR), computes the Normalized Difference Vegetation Index (NDVI), and separates the scene into vegetation and soil zones using a user-defined NDVI threshold (default = 0.8). The script then masks each band to isolate vegetation-only and soil-only reflectance, saves them as new GeoTIFF files, and provides a clear set of visual plots for interpretation. It enables targeted analysis of crop and soil reflectance patterns directly from drone-acquired raster data.


Author: Sathish Raymond Emmanuel

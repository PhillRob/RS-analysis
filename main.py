# This is a sample Python script.
#import arcsilib
#import arc

import rasterio
from xml.dom import minidom
from xml.etree.ElementTree import parse
import numpy
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

dir = "/Users/philipp/Dropbox (BPLA)/03_Planning/NDVI-Studies-Riyadh/02_Drawings/CAD/"
image_file = "/Users/philipp/Dropbox (BPLA)/03_Planning/NDVI-Studies-Riyadh/02_Drawings/GIS/2021/WorldView 2021 8BAnds/21MAY13073945-S2AS-RCRC-8Bands.TIF"
image_file = "/Users/philipp/Dropbox (BPLA)/03_Planning/NDVI-Studies-Riyadh/02_Drawings/GIS/2021/WorldView 2021 8BAnds/Clipped-DQ-21MAY13074013-S2AS-RCRC-8Bands.TIF"

from rasterio.plot import show
# Load red and NIR bands - note all PlanetScope 4-band images have band order BGRN
with rasterio.open(image_file) as src:
    band_red = src.read(5)

with rasterio.open(image_file) as src:
    band_nir = src.read(7)

with rasterio.open(image_file) as src:
        band_nir2 = src.read(8)

show(band_red)

xmldoc = minidom.parse("/Users/philipp/Dropbox (BPLA)/03_Planning/NDVI-Studies-Riyadh/02_Drawings/GIS/2021/WorldView 2021 8BAnds/21MAY13073945-S2AS-RCRC-8Bands.XML")
nodes = xmldoc.getElementsByTagName("IMD")


document = parse('/Users/philipp/Dropbox (BPLA)/03_Planning/NDVI-Studies-Riyadh/02_Drawings/GIS/2021/WorldView 2021 8BAnds/21MAY13073945-S2AS-RCRC-8Bands.XML')
IMD = document.find('IMD')

bandC_F = IMD.find('BAND_C').findtext('ABSCALFACTOR')
bandB_F = IMD.find('BAND_B').findtext('ABSCALFACTOR')
bandG_F = IMD.find('BAND_G').findtext('ABSCALFACTOR')
bandY_F = IMD.find('BAND_Y').findtext('ABSCALFACTOR')
bandR_F = IMD.find('BAND_R').findtext('ABSCALFACTOR')
bandRE_F = IMD.find('BAND_RE').findtext('ABSCALFACTOR')
bandN_F = IMD.find('BAND_N').findtext('ABSCALFACTOR')
bandN2_F = IMD.find('BAND_N2').findtext('ABSCALFACTOR')

bandC_E = IMD.find('BAND_C').findtext('EFFECTIVEBANDWIDTH')
bandB_E = IMD.find('BAND_B').findtext('EFFECTIVEBANDWIDTH')
bandG_E = IMD.find('BAND_G').findtext('EFFECTIVEBANDWIDTH')
bandY_E = IMD.find('BAND_Y').findtext('EFFECTIVEBANDWIDTH')
bandR_E = IMD.find('BAND_R').findtext('EFFECTIVEBANDWIDTH')
bandRE_E = IMD.find('BAND_RE').findtext('EFFECTIVEBANDWIDTH')
bandN_E = IMD.find('BAND_N').findtext('EFFECTIVEBANDWIDTH')
bandN2_E = IMD.find('BAND_N2').findtext('EFFECTIVEBANDWIDTH')

gain = 0.964
offset = -3.021

# Multiply by corresponding coefficients
band_red_c = gain * band_red * (float(bandR_E) / float(bandR_E)) +(offset)
band_nir_c = gain * band_nir * (float(bandN_E)/float(bandN_E)) +(offset)
band_nir2_c = gain * band_nir2 * (float(bandN2_E)/float(bandN2_E)) +(offset)

# Allow division by zero
numpy.seterr(divide='ignore', invalid='ignore')

# Calculate NDVI
ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir.astype(float) + band_red.astype(float))
show(ndvi)

ndvin2 = (band_nir2.astype(float) - band_red.astype(float)) / (band_nir2.astype(float) + band_red.astype(float))
show(ndvin2)

#NDVI with autmoscorr
ndvi_c = (band_nir_c.astype(float) - band_red_c.astype(float)) / (band_nir_c.astype(float) + band_red_c.astype(float))
show(ndvi_c)

ndvin2_c = (band_nir2_c.astype(float) - band_red_c.astype(float)) / (band_nir2_c.astype(float) + band_red_c.astype(float))
show(ndvin2_c)



# Set spatial characteristics of the output object to mirror the input
kwargs = src.meta
kwargs.update(
    dtype=rasterio.float32,
    count = 1)

# Create the file
with rasterio.open('ndvi.tif', 'w', **kwargs) as dst:
        dst.write_band(1, ndvi.astype(rasterio.float32))

# Create the file
with rasterio.open('ndvin2_c.tif', 'w', **kwargs) as dst:
        dst.write_band(1, ndvin2_c.astype(rasterio.float32))

# Create the file
with rasterio.open('ndvin2.tif', 'w', **kwargs) as dst:
        dst.write_band(1, ndvin2.astype(rasterio.float32))

# Create the file
with rasterio.open('ndvi_c.tif', 'w', **kwargs) as dst:
        dst.write_band(1, ndvi_c.astype(rasterio.float32))




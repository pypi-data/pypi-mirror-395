# import cartopy.crs
# import cartopy
import rasterio.crs
import cmocean
import rectifiedgrid as rg
import os
from gisdata import GOOD_DATA
from matplotlib import pyplot as plt
from affine import Affine
# import cartopy.crs as ccrs
import pyepsg
import rioxarray
import xarray
from shapely.geometry import Point, LineString
import numpy as np
from scipy import ndimage
from rectifiedgrid.demo import get_demo_data
import matplotlib.colors as colors

# test 3D
da_path = "/home/menegon/menegon/ISMAR/projects/PORTODIMARE/cea_rer/downloaded/rer_project_area/rer_project_area.shp"
da = rg.read_vector(da_path, res=0.002, fillvalue=np.nan)

da3_path = "/home/menegon/menegon/ISMAR/projects/PORTODIMARE/cea_rer/downloaded/biological_conservation_zone_reprojected/biological_conservation_zone.shp"
da3 = rg.read_vector(da3_path, grid=da)
da3.rg.plotmap()
plt.show()

da3_3035 = da3.rio.reproject("epsg:3035")
da3_3035.shape
surface = (rg.read_raster("test/data/GEBCO2021_ita/GEBCO2021_ita.nc")
           .rio.write_crs("epsg:4326")
           )
surface.values = surface.values.astype(float)
surface.rio.set_nodata(np.nan, inplace=True)
divnorm = colors.TwoSlopeNorm(vmin=-4000, vcenter=0, vmax=2500)

top_surface = surface.copy()
top_surface.values = np.abs(top_surface.values)
da3_3035_z = da3_3035.rg.to_3d(bottom_surface=surface, top_surface=top_surface, resolution_z=3, mode="full", bottom_layer=10)
da3_3035_z.sel(y=2.38e+06, method="nearest").plot()
plt.show()

da3_3035_z = da3_3035.rg.to_3d(bottom_surface=surface, top=0, mode="middle")
da3_3035_z.sel(y=2.38e+06, method="nearest").plot()
plt.show()

da3_3035_z.to_netcdf('/tmp/a.nc')

#%%

vector_path = os.path.join(GOOD_DATA, "vector/san_andres_y_providencia_highway.shp")
da = rg.read_vector(vector_path, 0.001, fillvalue=0)
da.plot()
plt.show()
bounds = da.rio.bounds()
line = LineString([Point(bounds[0], bounds[1]), Point(bounds[2], bounds[3])])
features = zip([line], [10])
da_r = rg.rasterize_features(da, features)
da_r.plot()
plt.show()
da_add = da + da_r
da_add.plot()
plt.show()

da.attrs, da.encoding, da.rio.crs, da.rio.nodata
da_add.attrs, da_add.encoding, da_add.rio.crs, da_add.rio.nodata

da_add.rg.plotmap()
plt.show()

da_path = "/home/menegon/menegon/ISMAR/projects/PORTODIMARE/cea_rer/downloaded/rer_project_area/rer_project_area.shp"
da = rg.read_vector(da_path, res=0.002, fillvalue=np.nan)
bounds = da.rio.bounds()
buffer = 15000
da.rg.plotmap(zoomlevel=7, extent_buffer=buffer)
plt.show()

da2_path = "/home/menegon/menegon/ISMAR/projects/PORTODIMARE/cea_rer/downloaded/otb_evf_reprojected/otb_evf.shp"
da2 = rg.read_vector(da2_path, grid=da, column="swept_km")

da2.rg.plotmap(zoomlevel=7, extent_buffer=buffer, legend=True)
plt.show()

da3_path = "/home/menegon/menegon/ISMAR/projects/PORTODIMARE/cea_rer/downloaded/biological_conservation_zone_reprojected/biological_conservation_zone.shp"
da3 = rg.read_vector(da3_path, grid=da)
da3.rg.plotmap()
plt.show()

((da3).rg.gaussian_conv(0.03)*100).rg.logrescale().plot()
plt.show()

da3.rg.crop(value=np.nan).rg.plotmap()
plt.show()
da3.rio.crs

da3_3035 = da3.rio.reproject("epsg:3035")
da3_3035.shape
surface = (rg.read_raster("test/data/GEBCO2021_ita/GEBCO2021_ita.nc")
           .rio.write_crs("epsg:4326")
           )
surface.values = surface.values.astype(float)
surface.rio.set_nodata(np.nan, inplace=True)
divnorm = colors.TwoSlopeNorm(vmin=-4000, vcenter=0, vmax=2500)
surface.plot.surface(cmap=cmocean.cm.topo, norm=divnorm, xincrease=True)
plt.show()
surface.plot(cmap=cmocean.cm.topo, norm=divnorm, xincrease=True)
plt.show()

da3_3035_z = da3_3035.rg.to_3d(surface)
da3_3035_z.rg.resolution_z
da3_3035_z.rio._x_dim
da3_3035_z.sel(z=0, method="nearest").plot()
plt.show()


grid = da3_3035.copy()
grid.values[grid.values>=0] = 1
grid.plot()
plt.show()

acq_z = da3_3035_z.copy()
acq_z.rg.resolution_z, da3_3035_z.rg.resolution_z
acq_z.sel(y=2.38e+06, method="nearest").plot()
plt.show()

conv3d = acq_z.rg.gaussian_conv([4000, 1000, 3], mode="nearest")
conv3d.sel(y=2.38e+06, method="nearest").plot()
plt.show()
conv3d.sel(z=0, method="nearest").plot()
plt.show()

#%%
float(da3)
da3_sup = da3_3035.rg.to_3d(surface, mode="surface")
da3_sup.sel(y=2.38e+06, method="nearest").plot()
plt.show()
da3_sup_conv = da3_sup.rg.gaussian_conv([4000, 1000, 40], mode="nearest")
da3_sup_conv.sel(y=2.38e+06, method="nearest").plot()
plt.show()

da3_floor = da3_3035.rg.to_3d(surface, mode="floor")
da3_floor.sel(y=2.38e+06, method="nearest").plot()
plt.show()


grid4326 = get_demo_data('line4326')
grid3035 = get_demo_data('line3035')

p = cartopy.crs.Mercator().proj4_params

grid3035.values[0, -1] = 0
grid3035.values[0, -2] = 0
grid3035.shape

grid3035.plot()
plt.show()

grid3035.rg.crop(0).plot()
plt.show()



grid3035.coords

grid3035.plot()
plt.show()


from rasterio.enums import Resampling
_r = grid4326.rio.reproject_match(grid3035,
                                  resampling=Resampling.nearest)  # grid3035.reproject(grid4326, Resampling.nearest)

grid3035
rg.read_raster('/tmp/tmpzi_cwtu1.tiff')

round(da3.min().values * 100)
da3.values.min()

da3.values.mean().round(2)

self = da3.rg
raster = self._obj.copy()
maxval = np.nanmax(raster.values)
if maxval != 0:
    raster.values[:] = (raster.values / maxval)[:]

raster.values[raster.values>0]
raster.plot()
plt.show()

np.nanmax(raster.values)
raster.values.nanmin

da3.values[da3.values<0] = 0

np.array(10) / np.abs(np.array([10, -20]))

da3.rio.resolution()

rgauss = xarray.apply_ufunc(ndimage.gaussian_filter,
                        da3.fillna(0),
                        # input_core_dims=[[]],
                        # output_core_dims=[[]],
                        kwargs=dict(sigma=10, mode="constant") #, output=da3)
                       )
rgauss.where(da>0).plot()
plt.show()

rgauss.rio.resolution()
rgauss.spatial_ref

#%%

dar.spatial_ref

raster = os.path.join(GOOD_DATA, 'raster',
                      'test_grid.tif')
r = rg.read_raster(raster)

da.spatial_ref
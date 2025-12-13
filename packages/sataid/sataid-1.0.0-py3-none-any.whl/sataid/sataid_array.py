"""
sataid_array.py
Core class for manipulating SATAID data, plotting, and exporting.
Compatible with sataid_colormaps (3 arguments).
"""

import os
import re
from datetime import datetime, timedelta
from struct import pack
from typing import Optional

import netCDF4 as nc
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Import fungsi colormap internal
# Pastikan sataid_colormaps.py sudah memiliki parameter (name, channel, units)
from .sataid_colormaps import get_custom_colormap

# ============================================================
#  TIME UTILITIES
# ============================================================

def etim_to_datetime(etim):
    """Convert SATAID time tuple (yy, yy, mm, dd, hh, mm...) to datetime."""
    try:
        tahun = int(str(etim[0]) + str(etim[1]))
        bulan = etim[2]
        hari = etim[3]
        jam = etim[4]
        menit = etim[5]

        dt = datetime(tahun, bulan, hari, jam, menit)
        if menit > 0:
            # Round up to next hour if minutes > 0
            dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        return dt
    except Exception:
        return None


# ============================================================
#  SATAIDARRAY CLASS
# ============================================================

class SataidArray:
    """
    Container for SATAID data providing .plot(), .to_geotiff(), .to_netcdf(), and .sel() methods.
    """

    ShortName = ['V1', 'V2', 'VS', 'N1', 'N2', 'N3', 'I4',
                 'WV', 'W2', 'W3', 'MI', 'O3', 'IR', 'L2', 'I2', 'CO']

    def __init__(self,
                 lats: np.ndarray,
                 lons: np.ndarray,
                 data: np.ndarray,
                 sate: tuple,
                 chan: tuple,
                 etim: tuple,
                 fint: Optional[tuple] = None,
                 asat: Optional[tuple] = None,
                 vers: Optional[tuple] = None,
                 eint: Optional[tuple] = None,
                 cord: Optional[tuple] = None,
                 eres: Optional[tuple] = None,
                 fname: Optional[str] = None,
                 units: Optional[str] = None,
                 ftim: Optional[tuple] = None):
        self.lat = lats
        self.lon = lons
        self.data = data
        self.sate = sate
        self.chan = chan
        self.etim = etim
        self.ftim = ftim
        self.fint = fint
        self.asat = asat
        self.vers = vers
        self.eint = eint
        self.cord = cord
        self.eres = eres
        self.fname = fname
        self.units = units

        # Internal metadata for lossless round-trip writing
        self._digital_data: Optional[np.ndarray] = None
        self._cal_table: Optional[np.ndarray] = None
        self._nrec: Optional[tuple] = None
        self._ncal: Optional[tuple] = None
        self._calb: Optional[tuple] = None
        self._recl: Optional[int] = None

    @property
    def satellite_name(self) -> str:
        if not self.sate: return ""
        name = b"".join(self.sate).decode(errors='replace').strip()
        return 'Himawari-9' if name == 'Himawa-9' else name

    @property
    def channel_name(self) -> str:
        if not self.chan: return ""
        raw_name = b"".join(self.chan).decode(errors='ignore')
        match = re.match(r'^[A-Za-z]+', raw_name)
        return match.group(0) if match else ''

    def description(self):
        dt = etim_to_datetime(self.etim)
        time_str = dt.strftime("%Y-%m-%d %H:%M UTC") if dt else ""
        print("=== Data Description ===")
        print(f"Time: {time_str}")
        print(f"Satellite: {self.satellite_name} | Channel: {self.channel_name}")
        print(f"Shape: {self.data.shape} | Units: {self.units}")
        print(f"Lat: {self.lat.min():.4f} to {self.lat.max():.4f}")
        print(f"Lon: {self.lon.min():.4f} to {self.lon.max():.4f}")

    def to_array(self):
        return self.lat, self.lon, self.data

    # ------------------ PLOTTING ------------------

    def _create_plot(self, cartopy=False, coastline_resolution='10m',
                     coastline_color='blue', cmap=None):
        plot_data = self.data.copy()
        
        # 1. Tentukan Default (Gray)
        norm = None
        cbar_kwargs = {}
        vmin, vmax = None, None
        default_cmap = 'gray'
        colorbar_label = f'Value ({self.units})' if self.units else 'Value'

        if self.units == 'Reflectance':
            default_cmap = 'gray'
            vmin, vmax = 0, 1.1
        elif self.units == '°C':
            default_cmap = 'gray_r'
            vmin, vmax = -80, 60
            colorbar_label = 'Brightness Temperature (°C)'

        # Colormap awal pilihan user (atau default)
        plot_cmap = cmap if cmap is not None else default_cmap

        # 2. Cek Custom Colormap via sataid_colormaps
        #    Jika user minta 'EH' tapi data bukan IR, get_custom_colormap akan return None.
        if isinstance(plot_cmap, str):
            custom_pack = get_custom_colormap(plot_cmap, self.channel_name, self.units)
            
            if custom_pack is not None:
                # Custom map valid (misal: EH pada channel IR)
                plot_cmap, norm, label_custom, cbar_custom = custom_pack
                if label_custom: colorbar_label = label_custom
                if cbar_custom: cbar_kwargs.update(cbar_custom)
                # Reset vmin/vmax karena norm menangani range
                vmin = vmax = None
            else:
                # Custom map INVALID atau nama standar Matplotlib (misal 'jet').
                # Cek apakah user memaksa minta colormap khusus IR ('EH', 'RAINBOW_IR')
                # tapi ditolak karena channel tidak cocok.
                if plot_cmap.upper() in ['EH', 'EH_IR', 'RAINBOW_IR']:
                    print(f"Warning: Colormap '{plot_cmap}' is valid only for IR/Thermal channels.")
                    print(f"         Switching to default grayscale for '{self.channel_name}'.")
                    plot_cmap = default_cmap
                    # Pastikan vmin/vmax direset ke default agar gambar tidak hitam/putih total
                    if self.units == 'Reflectance': vmin, vmax = 0, 1.1
                    elif self.units == '°C': vmin, vmax = -80, 60

        # 3. Eksekusi Plot
        dt = etim_to_datetime(self.etim)
        time_str = dt.strftime('%Y-%m-%d %H:%M UTC') if dt else ""
        title_l = f"{self.satellite_name} {self.channel_name}"
        title_r = time_str

        if cartopy:
            try:
                import cartopy.crs as ccrs
                import cartopy.feature as cfeature
            except ImportError:
                print("Error: 'cartopy' not found. Please install via: pip install cartopy")
                return None

            fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
            kw = dict(extent=(self.lon.min(), self.lon.max(), self.lat.min(), self.lat.max()),
                      origin='upper', cmap=plot_cmap, transform=ccrs.PlateCarree(), interpolation='none')
            
            if norm: kw['norm'] = norm
            else: 
                if vmin is not None: kw['vmin'] = vmin
                if vmax is not None: kw['vmax'] = vmax

            img = ax.imshow(plot_data, **kw)
            ax.coastlines(resolution=coastline_resolution, color=coastline_color, linewidth=0.8)
            ax.add_feature(cfeature.BORDERS, linewidth=0.3, edgecolor=coastline_color)
            
            # Gridlines
            gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
            gl.top_labels = False; gl.right_labels = False

            ax.set_title(title_l, loc='left', fontweight='bold', fontsize=10)
            ax.set_title(title_r, loc='right', fontweight='bold', fontsize=10)

            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="3%", pad=0.04, axes_class=plt.Axes)
            cbar = fig.colorbar(img, cax=cax, orientation='vertical', **cbar_kwargs)
            cbar.set_label(colorbar_label, size=9)
            # Invert axis only for Temp if gray_r is used (standard IR convention)
            if self.units == '°C' and 'gray_r' in str(plot_cmap): 
                cbar.ax.invert_yaxis()

        else:
            # Non-Cartopy Plot
            fig, ax = plt.subplots(figsize=(10, 6))
            kw = dict(extent=(self.lon.min(), self.lon.max(), self.lat.min(), self.lat.max()),
                      aspect='auto', cmap=plot_cmap)
            if norm: kw['norm'] = norm
            else:
                if vmin is not None: kw['vmin'] = vmin
                if vmax is not None: kw['vmax'] = vmax

            img = ax.imshow(plot_data, **kw)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="3%", pad=0.04)
            cbar = fig.colorbar(img, cax=cax, **cbar_kwargs)
            cbar.set_label(colorbar_label, size=9)
            if self.units == '°C' and 'gray_r' in str(plot_cmap):
                cbar.ax.invert_yaxis()

            ax.set_title(title_l, loc='left', fontweight='bold'); ax.set_title(title_r, loc='right', fontweight='bold')
            ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude')

        return fig

    def plot(self, cartopy=False, coastline_resolution='10m', coastline_color='blue', cmap=None):
        fig = self._create_plot(cartopy, coastline_resolution, coastline_color, cmap)
        if fig: plt.show()

    def savefig(self, output_file=None, cartopy=False, cmap=None, **kwargs):
        fig = self._create_plot(cartopy=cartopy, cmap=cmap, **kwargs)
        if fig:
            fname = output_file or (os.path.basename(self.fname) + '.png' if self.fname else 'output.png')
            print(f"Saving to {fname}")
            fig.savefig(fname, bbox_inches='tight', dpi=300)
            plt.close(fig)

    # ------------------ DATA SELECTION ------------------

    def sel(self, latitude=None, longitude=None, method='nearest'):
        # Point Selection
        if isinstance(latitude, (int, float)) and isinstance(longitude, (int, float)):
            if method == 'nearest':
                iy = np.abs(self.lat - latitude).argmin()
                ix = np.abs(self.lon - longitude).argmin()
                return self.data[iy, ix]
            elif method in ['linear', 'cubic']:
                try:
                    from scipy.interpolate import RectBivariateSpline
                    # RectBivariateSpline requires strictly increasing coords
                    lats_inv = self.lat[::-1] if self.lat[0] > self.lat[-1] else self.lat
                    data_inv = self.data[::-1, :] if self.lat[0] > self.lat[-1] else self.data
                    
                    k = 3 if method == 'cubic' else 1
                    interp = RectBivariateSpline(lats_inv, self.lon, data_inv, kx=k, ky=k)
                    return interp(latitude, longitude)[0, 0]
                except ImportError:
                    print("Error: scipy required for interpolation.")
                    return None
            else:
                raise NotImplementedError("Supported methods: 'nearest', 'linear', 'cubic'")

        # Region Selection (Slicing)
        lat_sl = slice(None); lon_sl = slice(None)
        if isinstance(latitude, slice):
            lat_sl = (self.lat >= min(latitude.start, latitude.stop)) & \
                     (self.lat <= max(latitude.start, latitude.stop))
        if isinstance(longitude, slice):
            lon_sl = (self.lon >= min(longitude.start, longitude.stop)) & \
                     (self.lon <= max(longitude.start, longitude.stop))

        sub_data = self.data[np.ix_(lat_sl, lon_sl)]
        sub_lats = self.lat[lat_sl]
        sub_lons = self.lon[lon_sl]

        new_obj = SataidArray(
            sub_lats, sub_lons, sub_data, self.sate, self.chan, self.etim,
            self.fint, self.asat, self.vers, self.eint, self.cord, self.eres,
            self.fname, self.units, self.ftim
        )
        # Crop digital data as well for round-trip safety
        if self._digital_data is not None:
            new_obj._digital_data = self._digital_data[np.ix_(lat_sl, lon_sl)]
        new_obj._cal_table = self._cal_table
        new_obj._nrec = self._nrec; new_obj._ncal = self._ncal
        new_obj._calb = self._calb; new_obj._recl = self._recl
        return new_obj

    # ------------------ EXPORT METHODS ------------------

    def to_geotiff(self, output_filename=None):
        """
        Export data to GeoTIFF format. Requires 'rasterio'.
        """
        try:
            import rasterio
            from rasterio.transform import from_bounds
        except ImportError:
            print("\nError: 'rasterio' is required for GeoTIFF export.")
            print("Install via: pip install rasterio")
            return

        if output_filename is None:
            output_filename = (os.path.basename(self.fname) + '.tif') if self.fname else 'output.tif'

        print(f"Saving data to GeoTIFF: {output_filename}")

        # Bounds: West, South, East, North
        left, right = self.lon.min(), self.lon.max()
        bottom, top = self.lat.min(), self.lat.max()
        height, width = self.data.shape
        
        # Transform: Top-Left based. 
        # Note: self.lat[0] is typically North (Top), self.lat[-1] is South (Bottom)
        # Bounds order for rasterio: (left, bottom, right, top)
        transform = from_bounds(left, bottom, right, top, width, height)

        with rasterio.open(
            output_filename,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=str(self.data.dtype),
            crs='EPSG:4326',  # WGS84
            transform=transform
        ) as dst:
            dst.write(self.data, 1)

    def to_netcdf(self, output_filename=None):
        if not output_filename:
            output_filename = (os.path.basename(self.fname) + '.nc') if self.fname else 'output.nc'
        
        print(f"Exporting to NetCDF: {output_filename}")
        
        with nc.Dataset(output_filename, 'w', format='NETCDF4') as ds:
            ds.description = f"SATAID Export - {self.channel_name}"
            ds.createDimension('lat', len(self.lat))
            ds.createDimension('lon', len(self.lon))
            
            vlat = ds.createVariable('lat', 'f4', ('lat',))
            vlat[:] = self.lat
            vlat.units = 'degrees_north'
            
            vlon = ds.createVariable('lon', 'f4', ('lon',))
            vlon[:] = self.lon
            vlon.units = 'degrees_east'
            
            vdata = ds.createVariable(self.channel_name, 'f4', ('lat', 'lon'))
            vdata[:] = self.data
            if self.units:
                vdata.units = self.units

    def to_sataid(self, output_filename=None):
        """Write back to SATAID binary format (lossless if using original counts)."""
        if not output_filename:
            output_filename = (os.path.basename(self.fname) + '.sataid') if self.fname else 'output.sataid'
            
        if self._digital_data is None:
            raise ValueError("Raw digital data missing. Cannot export to SATAID.")

        print(f"Exporting to SATAID binary: {output_filename}")
        ddata = self._digital_data.astype(np.uint16)
        ny, nx = ddata.shape
        
        # Recalculate Coordinate Header for current extent
        # Cord structure: UL, UR, LL, LR
        new_cord = [self.lat.max(), self.lon.min(), self.lat.max(), self.lon.max(),
                    self.lat.min(), self.lon.min(), self.lat.min(), self.lon.max()]
        recl = self._recl if self._recl else 288

        with open(output_filename, 'wb') as f:
            # Header writing...
            f.write(pack('I', recl))
            f.write(pack('c'*8, *self.chan)); f.write(pack('c'*8, *self.sate))
            f.write(pack('I', 0)) # skip
            ft = self.ftim if self.ftim else self.etim
            f.write(pack('I'*8, *ft)); f.write(pack('I'*8, *self.etim))
            f.write(pack('I', self._calb[0]))
            f.write(pack('I'*2, *self.fint)); f.write(pack('f'*2, *self.eres))
            f.write(pack('I'*2, nx, ny))
            f.write(pack('I'*2, *self._nrec))
            f.write(pack('f'*8, *new_cord))
            f.write(pack('I'*3, *self._ncal))
            f.write(b'\x00'*24)
            f.write(pack('f'*6, *self.asat))
            f.write(b'\x00'*32)
            f.write(pack('c'*4, *self.vers))
            f.write(pack('I', recl))

            # Calibration Table
            cal_sz = (len(self._cal_table) + 2) * 4
            f.write(pack('I', cal_sz))
            f.write(self._cal_table.astype('f4').tobytes())
            f.write(pack('I', cal_sz))

            # Data Lines (2-byte handling)
            line_bytes = nx * 2
            base = line_bytes + 8
            pad = (4 - (base % 4)) % 4
            rec_sz = base + pad
            
            for i in range(ny):
                f.write(pack('I', rec_sz))
                f.write(ddata[i, :].tobytes())
                if pad > 0: f.write(b'\x00' * pad)
                f.write(pack('I', rec_sz))
                
        print("SATAID binary written.")

    def to_xarray(self):
        try:
            import xarray as xr
        except ImportError:
            print("xarray not installed.")
            return None
        
        # xarray prefers lat south->north
        l, d = self.lat, self.data
        if l[0] > l[-1]:
            l = l[::-1]
            d = d[::-1, :]
            
        coords = {'lat': l, 'lon': self.lon}
        attrs = {'units': self.units, 'satellite': self.satellite_name}
        return xr.DataArray(d, coords=coords, dims=('lat', 'lon'), name=self.channel_name, attrs=attrs)
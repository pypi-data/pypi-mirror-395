"""
sataid_colormaps.py
Menyediakan skema warna kustom dengan validasi tipe data.
"""

import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm

# Daftar channel yang dianggap sebagai channel suhu (IR/WV)
THERMAL_CHANNELS = ['IR', 'WV', 'W2', 'W3', 'MI', 'I2', 'I4', 'CO', 'O3']

def _make_eh_colormap(units=None):
    # Definisi Level EH dalam Celcius
    levels_c = np.array([-100, -69, -62, -56, -48, -41, -34, -28, -21, -13, -7, 0, 8, 14, 21, 60], dtype=float)
    
    if units is not None and "K" in str(units):
        levels = levels_c + 273.15
        label_units = "K"
    else:
        levels = levels_c
        label_units = "°C"

    colors = ('#ffd4b8', '#ffc48d', '#ffa000', '#ff5d00', '#cd9a00', '#c5bb00', 
              '#9cd300', '#8cff00', '#00e686', '#00c091', '#43b0ff', '#4887ff', 
              '#3462b4', '#0a4882', '#000000')
    
    cmap = ListedColormap(colors, name="EH")
    norm = BoundaryNorm(levels, cmap.N)
    cbar_kwargs = {"ticks": levels, "spacing": "proportional"}
    return cmap, norm, f"Brightness Temperature ({label_units})", cbar_kwargs

def _make_rainbow_ir_colormap(units=None):
    levels_k = np.array([330, 310, 290, 270, 260, 250, 240, 235, 230, 225, 220, 215, 210, 205, 200, 195, 190, 185, 180, 175, 170], dtype=float)
    if units is not None and ("C" in str(units)):
        levels = levels_k - 273.15
        label_units = "°C"
    else:
        levels = levels_k
        label_units = "K"

    colors = ["#202020", "#404040", "#707070", "#A0A0A0", "#F5F5F5", "#00F5FF", "#40C0FF", "#0040FF", "#00FF40", "#C0FF00",
              "#FFFF00", "#FF9900", "#FF0000", "#C00000", "#603020", "#404040", "#707070", "#D0D0D0", "#B000C0", "#FFFFFF"]

    cmap = ListedColormap(colors, name="RAINBOW_IR")
    norm = BoundaryNorm(levels, cmap.N)
    cbar_kwargs = {"ticks": levels[::2], "spacing": "proportional"}
    return cmap, norm, f"Brightness Temperature ({label_units})", cbar_kwargs

# --- FUNGSI UTAMA ---
def get_custom_colormap(name: str, channel_name: str = "", units: str = None):
    """
    Mengambil colormap jika cocok dengan tipe datanya.
    """
    if not isinstance(name, str):
        return None

    key = name.upper()
    ch = channel_name.upper() if channel_name else ""
    
    # Cek apakah ini data suhu (berdasarkan nama channel atau satuan unit)
    # Channel IR biasanya mengandung string 'IR', 'WV', atau ada di list THERMAL_CHANNELS
    is_thermal = any(x in ch for x in THERMAL_CHANNELS)
    
    # Validasi tambahan lewat units (jika channel name kosong/aneh)
    if units and ('C' in units or 'K' in units):
        is_thermal = True
    if units and 'Reflectance' in units:
        is_thermal = False

    # --- EH (Strict IR Check) ---
    if key in ("EH", "EH_IR"):
        if is_thermal:
            return _make_eh_colormap(units=units)
        else:
            # Jika user minta EH tapi datanya bukan Thermal/IR, return None.
            # sataid_array.py harus menangani ini agar tidak error.
            return None

    # --- RAINBOW ---
    if key == "RAINBOW_IR":
        if is_thermal:
            return _make_rainbow_ir_colormap(units=units)
        else:
            return None

    return None
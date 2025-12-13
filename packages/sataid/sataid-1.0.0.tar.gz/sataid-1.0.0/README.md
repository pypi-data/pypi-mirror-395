# sataid

`sataid` is a small Python helper package to read, visualize, crop, and re-write
**SATAID binary files** .

It is mainly designed for operational meteorologists and satellite enthusiasts
who are familiar with JMA Himawari/SATAID workflows, but want to process the
data using Python and modern tools (NumPy, Matplotlib, Cartopy, xarray, etc.).

---

## Installation

```bash
pip install sataid

#or
pip install "sataid[full]"
# full = cartopy, rasterio, xarray, scipy

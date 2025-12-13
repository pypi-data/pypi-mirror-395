"""
sataid_reader.py
Handles reading of raw SATAID (*.Z00) files.
"""

import io
import re
from struct import unpack
import numpy as np

# Import internal Class
from .sataid_array import SataidArray

def _szdd_decompress_bytes(data: bytes) -> bytes:
    """Decompress SZDD/MS-Expand compressed data."""
    if len(data) < 14 or data[:4] != b"SZDD":
        raise ValueError("Not an SZDD file.")

    print("SZDD Compression detected. Decompressing...")
    out_len = unpack('I', data[10:14])[0]
    payload = data[14:]

    # LZSS buffer
    window = bytearray(4096)
    for i in range(4096): window[i] = 0x20
    
    pos = 4096 - 16
    out = bytearray()
    p = 0
    
    while p < len(payload):
        control = payload[p]; p += 1
        bit = 1
        while bit <= 0x80 and p < len(payload):
            if control & bit:
                if p >= len(payload): break
                ch = payload[p]; p += 1
                out.append(ch)
                window[pos] = ch
                pos = (pos + 1) & 0xFFF
            else:
                if p + 1 > len(payload): break
                matchpos = payload[p]
                matchlen = payload[p+1]
                p += 2
                matchpos |= (matchlen & 0xF0) << 4
                matchlen = (matchlen & 0x0F) + 3
                for _ in range(matchlen):
                    c = window[matchpos & 0xFFF]
                    matchpos = (matchpos + 1) & 0xFFF
                    out.append(c)
                    window[pos] = c
                    pos = (pos + 1) & 0xFFF
            bit <<= 1
            
    if out_len > 0 and len(out) >= out_len:
        out = out[:out_len]
    return bytes(out)


def read_sataid(fname):
    """
    Main entry point to read a SATAID file.
    Returns a SataidArray object.
    """
    with open(fname, 'rb') as f:
        head = f.read(4)
        f.seek(0)
        content = f.read()
    
    if head == b"SZDD":
        content = _szdd_decompress_bytes(content)
        
    fi = io.BytesIO(content)

    # --- Header Parsing ---
    recl = unpack('I', fi.read(4))[0]
    chan = unpack('c'*8, fi.read(8))
    sate = unpack('c'*8, fi.read(8))
    fi.read(4)
    ftim = unpack('I'*8, fi.read(32))
    etim = unpack('I'*8, fi.read(32))
    calb = unpack('I', fi.read(4))
    fint = unpack('I'*2, fi.read(8))
    eres = unpack('f'*2, fi.read(8))
    eint = unpack('I'*2, fi.read(8)) # nx, ny
    nrec = unpack('I'*2, fi.read(8))
    cord = unpack('f'*8, fi.read(32))
    ncal = unpack('I'*3, fi.read(12))
    fi.read(24)
    asat = unpack('f'*6, fi.read(24))
    fi.read(32)
    vers = unpack('c'*4, fi.read(4))
    fi.read(4) # end recl

    # --- Calibration Table ---
    nbyt = unpack('I', fi.read(4))[0]
    cal_len = int(nbyt/4 - 2)
    cal = np.array(unpack('f'*cal_len, fi.read(4*cal_len)))
    fi.read(4)

    # --- Digital Data ---
    nx, ny = eint
    raw_list = []
    
    if nrec[1] == 2: # 2 bytes per pixel
        for _ in range(ny):
            l_nbyt = unpack('I', fi.read(4))[0]
            line = unpack('H'*nx, fi.read(nx*2))
            raw_list.append(line)
            pad = l_nbyt - (nx*2 + 8)
            if pad > 0: fi.read(pad)
            fi.read(4)
    else:
        raise NotImplementedError("Only 2-byte SATAID supported for now.")

    raw_data = np.array(raw_list, dtype=np.uint16)

    # --- Calibration & Coords ---
    # Cord: UL(lat,lon), UR, LL, LR
    lat_ul, lon_ul = cord[0], cord[1]
    lat_ll, lon_ur = cord[4], cord[3]
    
    lats = np.linspace(lat_ul, lat_ll, ny)
    lons = np.linspace(lon_ul, lon_ur, nx)
    
    # Apply calibration
    idx = raw_data.astype(int) - 1
    idx = np.clip(idx, 0, len(cal)-1)
    data = cal[idx]

    # --- Meta & Units ---
    ch_str = b"".join(chan).decode(errors='ignore').strip()
    m = re.match(r'^[A-Za-z0-9]+', ch_str)
    short = m.group(0) if m else ''
    
    # Simple Unit Logic
    units = 'unknown'
    # List of Refl channels (approximate index logic or names)
    if any(x in short for x in ['V1', 'V2', 'VS', 'N1', 'N2', 'N3']):
        units = 'Reflectance'
    elif any(x in short for x in ['IR', 'WV', 'W2', 'W3', 'MI', 'I2', 'I4']):
        data = data - 273.15 # K to C
        units = '°C'

    obj = SataidArray(
        lats, lons, data, sate, chan, etim, fint, asat, vers, eint, cord, eres,
        fname=fname, units=units, ftim=ftim
    )
    
    # Attach raw data for exporting
    obj._digital_data = raw_data
    obj._cal_table = cal
    obj._nrec = nrec; obj._ncal = ncal
    obj._calb = calb; obj._recl = recl
    
    return obj

def read_sataid_array(fname):
    """Returns simple tuple (lat, lon, data)."""
    s = read_sataid(fname)
    return s.lat, s.lon, s.data
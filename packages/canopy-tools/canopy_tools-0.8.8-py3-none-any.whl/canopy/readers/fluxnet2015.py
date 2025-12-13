import pandas as pd
import numpy as np
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime
from canopy.readers.registry import register_reader_desc
from canopy.source_data import get_source_data

FLUXNET_FREQS = ['HH', 'HR', 'DD', 'WW', 'MM', 'YY', ]
PERIOD_FREQS = {'HH': '30min', 'HR': 'h', 'DD': 'D', 'WW': 'W', 'MM': 'M', 'YY': 'Y', }
TIMESTAMP_FORMAT = {'HH': '%Y%m%d%H%M', 'HR': '%Y%m%d%H%M', 'DD': '%Y%m%d', 'WW': '%Y%m%d', 'MM': '%Y%m', 'YY': '%Y', }

NA = -9999.0

def _read_zipped_fnet(path: Path, freq: str, subset: str, cols: list[str] | None):

    csv_file = Path(path.stem.replace(f"{subset}_", f"{subset}_{freq}_") + ".csv")

    if not freq in FLUXNET_FREQS:
        raise ValueError(f"Unrecognized frequency {freq} (must be one of {FLUXNET_FREQS}).")
    timestamp_col = 'TIMESTAMP'
    if freq in ['HH', 'HR', 'WW']:
        timestamp_col += '_START'
    timestamp_format = TIMESTAMP_FORMAT[freq]

    with ZipFile(path) as fzip:
        try:
            fzip.extract(csv_file.name)
        except KeyError:
            return None

    with open(csv_file) as f:
        csv_header = f.readline().split(',')
        csv_header = [c.strip() for c in csv_header]
        for c in ['TIMESTAMP', 'TIMESTAMP_START', 'TIMESTAMP_END']:
            try:
                csv_header.remove(c)
            except ValueError:
                pass

    if cols is None:
        cols_filtered = [timestamp_col] + csv_header
    else:
        cols = [c.strip().upper() for c in cols]
        cols_filtered = sorted(list(set(cols) & set(csv_header)))
        cols_filtered = [timestamp_col] + cols_filtered

    site_code = csv_file.name[4:10].lower()
    fnet_data = get_source_data('fluxnet2015')
    lon = fnet_data["sites"][site_code]['longitude']
    lat = fnet_data["sites"][site_code]['latitude']

    df = pd.read_csv(csv_file,
                     usecols=cols_filtered,
                     parse_dates = [timestamp_col],
                     date_format = timestamp_format)
        
    csv_file.unlink()
    df.rename(columns={timestamp_col:'time'}, inplace=True)
    df['time'] = df['time'].dt.to_period(PERIOD_FREQS[freq])
    df['lon'] = lon
    df['lat'] = lat
    df.index = pd.MultiIndex.from_frame(df[['lon', 'lat', 'time']])
    df.drop(['lon', 'lat', 'time'], axis=1, inplace=True)
    df[df == NA] = np.nan

    return df


@register_reader_desc('FLUXNET 2015')
def fluxnet2015(path: str | Path,
                grid_type: str,
                freq: str,
                subset: str = 'SUBSET',
                cols: list[str] | None = None,
                sites: list[str] | None = None):
    """
    Read a file from a .zip archive from FLUXNET2015 as downloaded from www.fluxnet.org

    Parameters
    ----------
    path : str | Path
        The path of a fluxnet.org .zip file or the path of a directory containing fluxnet.org
        .zip files. In the latter case, see 'sites' argument below.
    freq : str
        The frequency to retrieve as described in fluxnet.org:
            HH: half-hourly
            HR: hourly
            DD: daily
            WW: weekly
            MM: monthly
            YY: yearly
    subset : str
        The subset to retrieve. One of 'FULLSET' or 'SUBSET' (the default).
    cols : list[str] or None
        Colums to read (case insensitive). If None, the default, all columns are read.
    sites : list[str] or None
        A list of fluxnet site codes as in https://fluxnet.org/sites/site-list-and-pages/
        If None, all valid fluxnet sites in the path are read.
    """

    path = Path(path)

    if not path.exists():
        raise ValueError(f"Path {path} does not exist.")

    # If path is a file, attempt to read that file
    if path.is_file():
        df = _read_zipped_fnet(path, freq, subset, cols)
    # If path is a directory, load all files in directory, or all files that are in "sites"
    else:
        dframes = []
        if sites is None:
            files = path.glob("*FLUXNET2015*.zip")
            for file in files:
                dframes.append(_read_zipped_fnet(file, freq, subset, cols))
        else:
            match = set()
            for site_code in sites:
                for file in path.glob(f"FLX_*FLUXNET2015*{subset}*.zip"):
                    if site_code.lower() in file.name.lower():
                        dframes.append(_read_zipped_fnet(file, freq, subset, cols))
                        match.add(site_code)
                        break
            if len(dframes) == 0:
                raise ValueError(f"No matching files for 'sites' list in {path}.")
            no_match = set(sites) ^ match
            if len(no_match) > 0:
                print("WARNING: no matching files for the following sites:")
                print('\n'.join(no_match))
        try:
            df = pd.concat(dframes)
        except ValueError:
            df = None

    if df is None:
        raise ValueError("No matching data found.")

    if not df.index.is_monotonic_increasing:
        df.sort_index(inplace=True)

    return df


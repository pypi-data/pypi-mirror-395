# NYC School Data
# Copyright (C) 2025. Matthew X. Curinga
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU AFFERO GENERAL PUBLIC LICENSE (the "License") as
# published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the License for more details.
#
# You should have received a copy of the License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================
import pandas as pd
import geopandas as gpd
import os
import requests
import appdirs
import json
import warnings
from pathlib import Path

def local_path(url):
    """Get the local path for storing cached files from a url."""
    root =  appdirs.user_data_dir("mixi-maps", "mixi")
    dirs = url.split("/")
    path = os.path.join(root, *dirs[2:])
    return path


def read_file(url, gdf=False):
    """Read a file from url or local cache."""
    filename = local_path(url)
    local = os.path.exists(filename)

    path = filename if local else url
    data = None
    if path.endswith(".parquet"):
        data =  gpd.read_parquet(path)
    elif path.endswith(".geojson"):
        data =  gpd.read_file(path)
    elif path.endswith(".csv"):
        data =  pd.read_csv(path)
    elif path.endswith(".feather"):
        data = gpd.read_feather(path) if gdf else pd.read_feather(path)
    elif path.endswith(".json"):
        if local:
            with open(path, "r") as f:
                data = json.load(f)
        else:
            response = requests.get(path)
            response.raise_for_status()
            data = response.json()
    else:
        if not local:
            download_file(url, filename)
        with open(path, "r") as f:
            data =  f.read()

    if not local:
        write_cache(data, filename)

    return data

def clear_cache(fn):
    path = local_path(fn)
    path = os.path.join(path, fn)
    if os.path.exists(path):
        os.remove(path)


def write_cache(df, path):
    """Write a data file to the user local cache."""
    # create the directory if it doesn't exist
    dir = os.path.dirname(path)
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)

        ext = Path(path).suffix.lower().lstrip(".")
        if ext == "geojson":
            df.to_file(path, driver="GeoJSON")
        elif ext == "csv":
            df.to_csv(path, index=False)
        elif ext == "feather":
            df.to_feather(path)
        elif ext == "json":
            with open(path, "w") as f:
                json.dump(df, f)
        elif ext == "parquet":
            df.to_parquet(path, index=False)
        else:
            with open(path, "w") as f:
                f.write(df)
    except Exception as e:
        warnings.warn("Failed to write cache file:\n" + path)
        warnings.warn(str(e))

def download_file(url, local_filename):
    """Optimize file download using requests library."""
    Path(local_filename).parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

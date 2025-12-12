
# Spio

## Description

Spio is a Python package that provides functionalities for reading and writing data to a SharePoint.
It can also handle various types of spatial and non-spatial data formats such as GeoTIFF, GeoPackage, NetCDF, CSV, Excel, and more.

## Installation

To install the package, you can use the following command:

```bash
    pip config set global.extra-index-url https://repo.vito.be/artifactory/api/pypi/marvin-projects-pypi-local/simple
    pip install spytools 
```

If you want to install the package with all the dependencies, you can use the following command:

```bash
    pip install spytools[full]
```

## Building from Source

To build the package from source you can use the following commands:

```bash
    git clone https://git.vito.be/projects/MARVIN/repos/sharepoint_tools
    cd sharepoint_tools
    conda create -f conda_env.yml
    conda activate spytools 
    poetry install
```

## Configuration

Before using the package, you need to configure the settings to match your environment. 
The configuration is managed through a `settings` module which should include all the necessary configurations.

### **Settings Configuration**:
   Ensure you have a `settings` file (e.g., `.secrets.yaml` or `settings.yaml`) that provides the necessary configuration options. Example:

```python
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=['settings.yaml', '.secrets.yaml']
)
```
   
   The settings file should include the following configurations:
    
```yaml
    user_account: your.name@vito.be
```

### **Initialize Spio with Settings**:
   You need to initialize Spio with your settings before using any functionalities.

```python
from config import settings
from marvin.spytools import spio

spio.init_spio(settings)
```

## Usage

Here are some example usages of the package:

### Reading Data

- **Read GeoTIFF using Rasterio**:

```python
from marvin.spytools.spio import SPIO
import rasterio

geotiff_file = SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/geotiff.tiff')
with rasterio.open(geotiff_file.copy_bytes_io()) as src:
    # Read the dataset's metadata
    print("Metadata:", src.meta)
    print("CRS:", src.crs)
    print("Bounds:", src.bounds)
    data = src.read()
    print("data: ", data.shape)
```

- **Read GeoTIFF using GDAL**:

```python
from marvin.spytools.spio import SPIO
from osgeo import gdal

with SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/geotiff.tiff') as spio:
    dataset = gdal.Open(spio.copy_file())
    band = dataset.GetRasterBand(1)
    data = band.ReadAsArray()
    print("data: ", data.shape)
    # Close the dataset
    del dataset
```

- **Read GeoPackage**:

```python
from marvin.spytools.spio import SPIO
import geopandas as gpd

gdf = gpd.read_file(SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/geopackage.gpkg'))
print("gdf: ", gdf)
```

- **Read NetCDF (h5netcdf)**:

```python
from marvin.spytools.spio import SPIO
import xarray as xr

ds = xr.load_dataset(SPIO(
    'https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/netcdf.nc'))  # use engine='h5netcdf' if not detected correctly
print("ds: ", ds)
```

- **Read NetCDF (netcdf4)**:

```python
from marvin.spytools.spio import SPIO
import xarray as xr

with SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/netcdf.nc') as spio:
    ds = xr.load_dataset(spio.copy_file(), engine='netcdf4')
    print("ds: ", ds)
```

- **Read GRIB**:

```python
from marvin.spytools.spio import SPIO
import xarray as xr

with SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/grib.grb') as spio:
    grb_ds = xr.load_dataset(spio.copy_file())  # engine='cfgrib'
    print("grb_ds: ", grb_ds)
```

- **Read Parquet**:

```python
from marvin.spytools.spio import SPIO
import pandas as pd

df = pd.read_parquet(SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/data.parquet'))
print("df: ", df)
```

- **Read CSV**:

```python
from marvin.spytools.spio import SPIO
import pandas as pd

df = pd.read_csv(SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/data.csv'))
print(f"df: , df")

# read first lines
df_top = pd.read_csv(SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/data.csv',
                          read_chunks=SPIO.DEFAULT_CHUNK_SIZE), sep=';', nrows=10)
print(f"df_top: , df_top")
```

- **Read Excel**:

```python
from marvin.spytools.spio import SPIO
import pandas as pd

df = pd.read_excel(SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/data.xlsx'))
print("df: ", df)
```


### Writing Data

- **Write CSV**:

```python
from marvin.spytools.spio import SPIO
import pandas as pd

df = pd.read_csv('path/to/your/data.csv')
df.to_csv(SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/data.csv'))
```

- **Write Excel**:

```python
from marvin.spytools.spio import SPIO
import pandas as pd

df = pd.read_csv('path/to/your/data.csv')
df.to_excel(SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/data.xlsx'), engine='xlsxwriter')
```

- **Write Text**:

```python
from marvin.spytools.spio import SPIO

with SPIO('https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/data.txt') as spio:
    spio.write_lines(['Hello, SPIO!'])
```


- **Write GeoTiff**:

```python
from marvin.spytools.spio import SPIO
import rasterio

with rasterio.open('path/to/your/map.tiff') as src:
    data = src.read()[0]
    profile = src.profile

    with SPIO(
            'https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/map.tiff') as spio:  # rasterio will not flush or close the SPIO file, so we need to do it ourselves
        with rasterio.open(spio, 'w', **profile) as dst:
            dst.write(data, 1)
```


- **Write GeoPackage Fiona**:

```python
from marvin.spytools.spio import SPIO
import geopandas as gpd

gdf = gpd.read_file('path/to/your/geopackage.gpkg')

with SPIO(
        'https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/geopackage.gpkg') as spio:  # fiona will not flush or close the IO-object, so we need to do it ourselves
    gdf.to_file(spio, layer='mylayer', driver='GPKG', engine='fiona')
```

- **Write GeoPackage Fiona**:

```python
from marvin.spytools.spio import SPIO
import geopandas as gpd

gdf = gpd.read_file('path/to/your/geopackage.gpkg')

with SPIO(
        'https://yourdomain.sharepoint.com/:i:/r/sites/your-site/path/to/your/geopackage.gpkg') as spio:  # pyogrio will not flush the IO-object
    gdf.to_file(spio.io_delegate(), layer='mylayer', driver='GPKG',
                engine='pyogrio')  # pyogrio can only write to a real BytesIO object.
```

### Additional Functionalities

Spio also provides additional functions to handle different data formats and processes.
You can explore these in the https://git.vito.be/projects/MARVIN/repos/sharepoint_tools/browse/test/tst_spio.py.


## Contributing

If you want to contribute to spio, please follow the standard contributing guidelines and push your changes to a new branch in
https://git.vito.be/projects/MARVIN/repos/sharepoint_tools

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

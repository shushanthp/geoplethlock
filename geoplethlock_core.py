import os
import geopandas as gpd
import rasterio
from cryptography.fernet import Fernet

def load_raster(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Raster file not found at: {path}")
    return rasterio.open(path)

def load_choropleth(path):
    if not path.lower().endswith(('.shp', '.geojson', '.gpkg')):
        raise ValueError("Unsupported file format. Please provide a .shp, .geojson, or .gpkg file.")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Choropleth file not found at: {path}")
    return gpd.read_file(path)

def generate_key():
    return Fernet.generate_key()

def save_key(key, path):
    # Ensure directory exists
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(key)

def load_key(path):
    if not path or not os.path.exists(path):
        raise FileNotFoundError(f"Key file not found at: {path}")
    with open(path, 'rb') as f:
        return f.read()

def encrypt_coordinates(gdf, key):
    if 'geometry' not in gdf.columns:
        raise ValueError("Input GeoDataFrame must have a 'geometry' column.")
    fernet = Fernet(key)
    gdf['enc_coord'] = gdf['geometry'].apply(lambda geom: fernet.encrypt(str(geom.centroid).encode()))
    return gdf

def decrypt_coordinates(enc_gdf, key):
    if 'enc_coord' not in enc_gdf.columns:
        raise ValueError("Encrypted GeoDataFrame must have an 'enc_coord' column.")
    fernet = Fernet(key)
    return enc_gdf['enc_coord'].apply(lambda val: fernet.decrypt(val).decode())

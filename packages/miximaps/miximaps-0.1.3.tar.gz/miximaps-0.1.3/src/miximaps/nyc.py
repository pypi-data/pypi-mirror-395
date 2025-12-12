
import pandas as pd
import geopandas as gpd
from census import Census
import pygris
import os

from . import census as mc
from . import datacache as dc
from . import tiger

# some useful CRS projections
crs_meters = 2263
crs_feet = 6539
crs_leaflet = 4326  # wgsa84 World Geodetic System

def get_nyc_counties(region="metro"):
    """Get the FIPS codes for NYC and its inner suburbs"""
        

    city = {
        ('36', '005'): 'Bronx County',
        ('36', '047'): 'Kings County',
        ('36', '061'): 'New York County',
        ('36', '085'): 'Richmond County',
        ('36', '081'): 'Queens County'
    }
    ny_inner = {
        ('36', '119'): 'Westchester County',
        ('36', '059'): 'Nassau County',
    }
    ny_outer = {
        ('36', '027'): 'Dutchess County',
        ('36', '071'): 'Orange County',
        ('36', '079'): 'Putnam County',
        ('36', '087'): 'Rockland County',
        ('36', '103'): 'Suffolk County',
    }
    nj = {
        ('34', '003'): 'Bergen County',
        ('34', '013'): 'Essex County',
        ('34', '017'): 'Hudson County',
    }

    ct = {
        ('09', '001'): 'Fairfield County',
    }

    metro = city | ny_inner | ny_outer | nj | ct

    inner = city | ny_inner | nj | ct
    suburbs = ny_inner | ny_outer | nj | ct
    if region == "city":
        return city
    if region == "inner":
        return inner
    if region == "suburbs":
        return suburbs
    return metro


def get_tracts(c, table, year=2023, region="inner", cache=True):
    """Get census tracts for NYC and inner suburbs for an acs5 table"""


    filename = f"nyc_tracts_{table}-{region}-{year}.geojson"
    if not cache:
        print("clearing cache")
        dc.clear_cache(filename)

    county_fips = get_nyc_counties(region=region).keys()
    df = mc.get_tracts(c, table, county_fips,year=year,filename=filename)

    boros = {
        '005': 'Bronx',
        '047': 'Brooklyn',
        '061': 'Manhattan',
        '085': 'Staten Island',
        '081': 'Queens',
    }

    df['borough'] = df['countyfp'].map(boros).fillna('-')

    return df


def group_by_neighborhood(gdf, avg_cols=None, sum_cols=None):
    avg_cols = avg_cols or []
    sum_cols = sum_cols or []


    if not (avg_cols or sum_cols):
        raise ValueError("At least one of avg_cols or sum_cols must contain a valid column name.")

    weighted_cols = avg_cols + sum_cols

    gdf = gdf.copy()
    if "area" not in gdf.columns:
        gdf["area"] = gdf.geometry.area

    hoods = get_neighborhoods()
    # drop any columns in hood that's in gdf
    drop = hoods.columns.intersection(gdf.columns)
    hoods.drop(columns=drop, inplace=True, errors="ignore")

    inter = gpd.overlay(gdf, hoods, how="intersection", keep_geom_type=False)
    inter["inter_area"] = inter.geometry.area
    inter["weight"] = inter.inter_area / inter.area

    inter[weighted_cols] = inter[weighted_cols] * inter["weight"]

    results = inter[["nta2020", "weight"] + weighted_cols].groupby("nta2020").agg("sum").reset_index()
    if avg_cols:
        results[avg_cols] = results[avg_cols] / results["weight"]
    return results


def get_neighborhoods(cache=True):

    url ="https://data.cityofnewyork.us/resource/9nt8-h7nd.geojson"
    if cache:
        df = dc.read_file(url)
    else:
        df = gpd.read_file(url)

    df = df[['ntaname', 'boroname', 'nta2020', 'geometry']]
    cols = {
        'ntaname': 'neighborhood',
        'boroname': 'borough',
        'nta2020': 'nta2020'
    }
    df.rename(columns=cols, inplace=True)

    return df


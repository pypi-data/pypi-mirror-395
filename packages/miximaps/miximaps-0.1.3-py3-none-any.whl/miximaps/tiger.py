from shapely.geometry import box
from urllib.request import urlopen
from io import BytesIO
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
import pandas as pd
import geopandas as gpd
import us
from census import Census
import pygris


from urllib.parse import urlparse

import os
from . import datacache as dc
from . import census as mc

def make_multi(geo):
    if geo is None or geo.is_empty:
        return None
    if isinstance(geo, Polygon):
        return MultiPolygon([geo])
    if isinstance(geo, MultiPolygon):
        return geo

    # Handle GeometryCollection (and any geometry with .geoms)
    parts = getattr(geo, "geoms", ())
    polys = []
    for g in parts:
        if isinstance(g, Polygon):
            polys.append(g)
        elif isinstance(g, MultiPolygon):
            polys.extend(g.geoms)
        else:
            sub = make_multi(g)
            if isinstance(sub, MultiPolygon):
                polys.extend(sub.geoms)

    return MultiPolygon(polys) if polys else None


def clip_water(df, state_col="statefp", county_col="countyfp", threshold=.85, year=2023):
    """
    Remove large water areas from the GeoDataFrame
    """
    states = df[state_col].unique().tolist()
    CT = us.states.CT.fips

    def get_water(st):
        counties = df[df[state_col] == st][county_col].unique().tolist()
        if st == CT:
            counties = [f"0{c}" for c in counties if c.startswith("0")]
        return pygris.area_water(state=st, county=counties, year=2023, cache=True)

    water = [get_water(st) for st in states]
    water = pd.concat(water, ignore_index=True)
    water = gpd.GeoDataFrame(water, geometry='geometry', crs='EPSG:4269')
    waterways = water.dissolve(
        by="HYDROID",
        aggfunc={
            "FULLNAME": "first",
            "ANSICODE": "first",
            "MTFCC": "first",
            "ALAND": "sum",
            "AWATER": "sum"
        }
    ).reset_index()
    waterways['water_rank'] = waterways.AWATER.rank(pct=True)
    bigwater = waterways[waterways.water_rank > threshold]
    x = df.copy()
    x.geometry = x.geometry.apply(make_multi)

    clipped = gpd.overlay(x, bigwater, how='difference')
    return clipped



# def merge_states(df):
#     df["STATEFP"] = df.ucgid.str[-2:]
#     states = gpd.read_file(
#         "https://www2.census.gov/geo/tiger/TIGER2022/STATE/tl_2022_us_state.zip")
#     states = states[["STATEFP", "STUSPS", "geometry"]]
#     data = states.merge(df, on="STATEFP")
#     data.rename(columns={"NAME": "state_name",
#                 "STUSPS": "state", "STATEFP": "statefp"}, inplace=True)
#     cols = list(data.columns)
#     cols.remove("geometry")
#     cols = cols + ["geometry"]
#     data = data[cols]
#     return data


# def merge_counties(df):
#     land = gpd.read_file(
#         "https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_500k.zip")
#     df["GEOID"] = df.ucgid.apply(lambda x: x.split("US")[1])
#     df["state_name"] = df.NAME.apply(lambda x: x.split(",")[1].strip())
#     df.drop(columns=["NAME"], inplace=True)
#     county_url = "https://www2.census.gov/geo/tiger/TIGER2022/COUNTY/tl_2022_us_county.zip"
#     counties = gpd.read_file(county_url)
#     counties = counties[["GEOID", "STATEFP", "COUNTYFP", "NAME", "geometry"]]
#     data = counties.merge(df, on="GEOID")
#     data.rename(columns={"NAME": "county", "COUNTYFP": "countyfp",
#                 "STATEFP": "statefp"}, inplace=True)
#     data["state"] = data.statefp.apply(lookup_state)
#     cols = list(data.columns)
#     cols.remove("geometry")
#     cols = cols + ["geometry"]
#     data = data[cols]
#     land = land[land.STATEFP.isin(data.statefp.unique())]
#     data = gpd.clip(data, land)
#     return data


# def merge_tracts(df):
#     land = gpd.read_file(
#         "https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_500k.zip")

#     df["GEOID"] = df.ucgid.apply(lambda x: x.split("US")[1])
#     state_fips = df.ucgid.apply(lambda x: x.split("US")[1][:2])
#     state_fips = state_fips.unique()
#     for statefp in state_fips:

#         url = f"https://www2.census.gov/geo/tiger/TIGER2022/TRACT/tl_2022_{statefp}_tract.zip"
#         state = land[land.STATEFP == statefp]

#         tracts = gpd.read_file(url)
#         tracts = tracts[["GEOID", "geometry",
#                          "STATEFP", "COUNTYFP", "TRACTCE"]]

#         data = tracts.merge(df, on="GEOID")
#         # push geometry cols to the end
#         cols = list(df.columns) + ["STATEFP",
#                                    "COUNTYFP", "TRACTCE", "geometry"]
#         data = data[cols]
#         data.columns = [c.lower() for c in data.columns]
#         data = gpd.clip(data, state)
#     return data


# def merge_geography(data):
#     data = data.copy()
#     level_codes = {
#         "010": "Nation",
#         "020": "Region",
#         "030": "Division",
#         "040": "State",
#         "050": "County",
#         "060": "County Subdivision",
#         "067": "Subminor Civil Division",
#         "140": "Census Tract",
#         "150": "Census Block",
#         "160": "Place",
#         "170": "Consolidated City",
#         "230": "Alaska Native Regional Corporation",
#         "250": "American Indian Area/Alaska Native Area/Hawaiian Home Land",
#         "251": "American Indian Area (Reservation or Off-Reservation Trust Land)",
#         "252": "Alaska Native Village Statistical Area",
#         "254": "Oklahoma Tribal Statistical Area",
#         "256": "Tribal Designated Statistical Area",
#         "258": "American Indian Joint-Use Area",
#         "260": "Metropolitan Statistical Area/Micropolitan Statistical Area",
#         "310": "Metropolitan Division",
#         "314": "Combined Statistical Area",
#         "330": "State Metropolitan Statistical Area",
#         "335": "New England City and Town Area (NECTA)",
#         "336": "NECTA Division",
#         "350": "Combined NECTA",
#         "400": "Urban Area",
#         "500": "Congressional District",
#         "610": "State Legislative District (Upper Chamber)",
#         "620": "State Legislative District (Lower Chamber)",
#         "700": "Public Use Microdata Area (PUMA)",
#         "860": "ZIP Code Tabulation Area (ZCTA)",
#         "970": "School District (Elementary)",
#         "980": "School District (Secondary)",
#         "990": "School District (Unified)"
#     }
#     geo_levels = data.ucgid.apply(lambda x: x[:3]).unique()
#     assert len(geo_levels) == 1, "Data contains multiple geographic levels"
#     level = level_codes[geo_levels[0]]
#     print(f"Geographic level: {level}")
#     if level == "Nation":
#         warnings.warn("Nation level data is not merged with geography")
#         return data

#     if level == "State":
#         data = merge_states(data)
#         return data.sort_values(by="state")

#     if level == "County":
#         data = merge_counties(data)
#         return data.sort_values(by=["state", "county"])

#     if level == "Census Tract":
#         return merge_tracts(data)

#     warnings.warn(
#         f"Unsupported geographic level: {level}, no geography available")
#     return data


# def merge_meta(data, meta):
#     data = data.copy()
#     geo_vars = ['AIANHH', 'ANRC', 'CBSA', 'CD', 'COUNTY', 'COUSUB', 'CSA',
#                 'GEOCOMP', 'GEO_ID', 'METDIV', 'NAME', 'NATION',
#                 'PLACE', 'PRINCITY', 'PUMA', 'REGION', 'SDELM',
#                 'SDSEC', 'SDUNI', 'STATE', 'SUMLEVEL', 'UA',
#                 'block group', 'congressional district', 'county', 'for', 'in',
#                 'place', 'state', 'tract', 'ucgid', 'zcta']

#     metadata = requests.get(meta).json()
#     vars_url = metadata["dataset"][0]["c_variablesLink"]
#     vars = requests.get(vars_url).json()
#     vars = vars["variables"]

#     aliases = {}
#     for c in data.columns:
#         meta = vars.get(c, None)
#         predicate = meta.get(
#             "predicateOnly", False) if meta is not None else False
#         if c in geo_vars or predicate:
#             aliases[c] = c
#             continue

#         if meta is None:
#             # if not c.startswith("D"):
#             #     print(f"{c},")
#             continue

#         # try to convert to the correct type
#         t = meta.get("predicateType", None)
#         try:
#             if t in ["int", "float"]:
#                 i = data[c].astype(float)
#                 try:
#                     i = i.astype(int)
#                 except:
#                     pass
#                 data[c] = i
#         except:
#             print(f"Error converting {c} to {t}. Value ({data[c]})")

#         n = nice_name(meta["label"])
#         aliases[c] = n

#     # print(aliases)
#     aliases = de_dup(aliases)
#     data = data[aliases.keys()]
#     data.rename(columns=aliases, inplace=True)
#     duplicates = data.columns[data.columns.duplicated()]
#     assert len(duplicates) == 0, f"Duplicate columns:\n {duplicates}"
#     return data

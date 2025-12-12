import pandas as pd
import geopandas as gpd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import us
import geonamescache
import warnings
import appdirs

import os
from census import Census
import pygris
from . import datacache as dc
from . import tiger


def nice_label(var):
    var = var.replace("Estimate!!", "")
    var = var.lower()
    var = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', re.sub(r'[^a-zA-Z0-9]+', '_', var))

    if var.startswith("total_"):
        var = var[6:]

    var = "_".join(var.split(" "))
    if var.endswith(":"):
        var = var[:-1]
    return var

def table_vars(table, year=2023):
    """Look up a census ACS 5 data table from meta data.
        Parameters
        ----------
        table : str
            The census table ID, e.g. B01001
        year : int, optional
            The year of the ACS data, by default 2023
        Returns
        -------
        dict
            A dictionary of variable codes and nice labels.


        Example
        -------
        from miximaps import census as mc
        table = "B25044"
        fields = mc.table_vars(table)
         = 
    
    """
    url = f"https://api.census.gov/data/{year}/acs/acs5/groups/{table}.json"
    data = data = dc.read_file(url)
    vars = data["variables"]
    keys = [k for k in vars.keys() if not k.startswith(table) or k.endswith("E")]
    vars = {k: nice_label(vars[k]["label"]) for k in keys if k in vars}

    return vars

def lookup_state(statefp):
    if statefp == "11":
        return "DC"

    state = us.states.lookup(statefp)
    if state is not None:
        return state.abbr

    return statefp


def county_mapper(statefp="state", countyfp="county"):

    gc = geonamescache.GeonamesCache()
    counties = gc.get_us_counties()
    county_mapper = dict([(c["fips"], c["name"]) for c in counties])
    def m(r):
        fips = r[statefp] + r[countyfp]
        return county_mapper.get(fips, f"Unknown ({fips})")
    return m


def get_tracts(c, table, state_counties, year=2023, filename=None, geo=True):
    """
    Get census tracts and geographic data for an acs5 table.

    Parameters
    ----------
    c : Census
        An initialized Census object from the census module.
    table : str
        The ACS5 table identifier (e.g., "B01001").
    state_counties : list of tuples
        A list of (state_fips, [county_fips]) tuples to specify which counties
        to include.
    year : int, optional
        The year of the ACS data (default is 2023). This is used to match the
        tiger/line data to the ACS data year (which is initialized in the Census object).
    filename : str, optional
        If provided, the function will cache the results to this filename
        in the default data cache directory (i.e. provide just the unique filename, not a path).
        This cached file will be used in subsequent calls to avoid redundant API requests.
    geo : bool, optional
        If `True` (default), return TIGER/line tract geometries, else just return the
        ACS5 tract data.
    

    Returns
    -------
    GeoDataFrame
        A GeoDataFrame containing the ACS data. The data is merged with 
        TIGER/Line tract geometries if `geo` is `True` (default).
        Large water areas are removed from the geometries.
    """


    cache = False
    if filename:
        path = dc.local_path(filename)
        filename = os.path.join(path, filename)

        if os.path.exists(filename):
            return dc.read_file(filename, gdf=geo)
        cache = True

    fields = table_vars(table, year=year)
    # add population estimate into every query
    fields["B01003_001E"] = "total_population"
    vars = list(fields.keys())

    results = []
    for state, counties in state_counties:
        r = c.acs5.state_county_tract(vars, state, counties, Census.ALL)
        results.extend(r)

    df = pd.DataFrame(results)
    df.rename(columns=fields, inplace=True)

    # drop rows with no data
    df.dropna(inplace=True)

    # make nicer column names
    df["county_name"] = df.apply(county_mapper(), axis=1)
    df["statefp"] = df.state
    df["state"] = df.statefp.apply(lookup_state)
    df["countyfp"] = df["county"]
    df["county"] = df.county_name
    df.drop(columns=["county_name"], inplace=True)

    # get the tigerline files if requested
    if geo:
        state_fips = df.statefp.unique().tolist()

        # merge tiger tracts
        tracts = pd.concat([pygris.tracts(state=s, year=year, cache=True) for s in state_fips])
        tracts["geography"] = tracts.apply(lambda row: _get_geoidfq(row, year), axis=1)
        df = df.merge(tracts[["geography", "geometry"]], on="geography", )
        df = gpd.GeoDataFrame(df, geometry="geometry")
        df = tiger.clip_water(df)

    if cache:
        print("writing cache")
        dc.write_cache(df, filename)
    return df


def _get_geoidfq(row, year):
    if "GEOIDFQ" in row:
        return row["GEOIDFQ"]
    if "GEOID" in row:
        return f"1400000US{row['GEOID']}"
    suffix = str(year % 2000)
    st, ct, tc = f"STATEFP{suffix}", f"COUNTYFP{suffix}", f"TRACTCE{suffix}"
    return f"1400000US{row[st]}{row[ct]}{row[tc]}"


# def search(term, results=20):
#     tables = get_tables()
#     tables = tables[tables.concept.notnull()]
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(tables.concept)

#     query_vec = vectorizer.transform([term])
#     tables["match"] = cosine_similarity(query_vec, tfidf_matrix).flatten()
#     tables.sort_values(by='match', ascending=False, inplace=True)
#     tables = tables.head(results).copy()
#     results = tables.style.set_properties(subset=['concept'], **{'white-space': 'pre-wrap', 'word-wrap': 'break-word'})
#     results.format({'match': '{:.2%}', 'concept': lambda x: x.title()})
#     return results

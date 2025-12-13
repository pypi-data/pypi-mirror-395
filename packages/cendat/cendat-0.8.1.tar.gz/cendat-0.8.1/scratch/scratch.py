import os
from cendat import CenDatHelper

cdh = CenDatHelper(key=os.getenv("CENSUS_API_KEY"))

cdh.list_products(years=[2023], patterns=r"acs/acs5\)")
cdh.set_products()
# cdh.list_groups(patterns=r"^race")
cdh.set_groups(["B17001"])
# cdh.describe_groups()
cdh.set_variables(["B17001_001E", "B17001_002E"])
cdh.set_geos(["050"])
response = cdh.get_data(
    include_names=True,
    include_geoids=True,
    include_geometry=True,
    within={
        "state": [
            "08",
        ]
    },
    in_place=False,
)
# df = response.to_polars(destring=True, concat=True)
df = response.to_gpd(destring=True, join_strategy="inner")
print(df.head())
dfp = response.to_polars(destring=True, concat=True)
print(dfp.head())


response.tabulate(
    "NAME",
    "B17001_002E",
    "B17001_001E",
    where=[
        "B17001_001E > 1_000",
        "B17001_002E / B17001_001E < 0.1",
        "'CDP' not in NAME",
    ],
    weight_var="B17001_001E",
    strat_by="vintage",
)

# ------------------

cdh = CenDatHelper(key=os.getenv("CENSUS_API_KEY"))
cdh.list_products(years=[2023], patterns=r"/acs/acs5\)")
cdh.set_products()
cdh.set_variables("B01001_001E")  # total population
cdh.set_geos("150")
response = cdh.get_data(
    include_geometry=True,
    within={"state": ["08", "56"]},
)

# how many block groups
response.tabulate("state", where="B01001_001E > 2_500")

# how many people in those block groups
response.tabulate("state", weight_var="B01001_001E", where="B01001_001E > 2_500")

# ------------------

cdh = CenDatHelper(key=os.getenv("CENSUS_API_KEY"))
cdh.list_products(years=[2022, 2023], patterns="/cps/tobacco")
cdh.set_products()
cdh.list_groups()
cdh.set_variables(["PEA1", "PEA3", "PWNRWGT"])
cdh.set_geos("state", "desc")
response = cdh.get_data(
    within={"state": ["06", "48"]},
    include_attributes=True,
    include_names=True,
    include_geoids=True,
)
response.tabulate(
    "PEA1",
    "PEA3",
    strat_by="state",
    weight_var="PWNRWGT",
    weight_div=3,
)

test = response.to_polars(concat=True, destring=True)

# ------------------

cdh = CenDatHelper(key=os.getenv("CENSUS_API_KEY"))

cdh.list_products(patterns=r"2010/dec/sf1\)")
cdh.set_products()
cdh.list_groups(patterns=r"^race")
cdh.describe_groups("PCT23")
cdh.set_groups(["PCT23"])
cdh.set_geos("160")
response = cdh.get_data(
    within={"state": "08"},
    include_geometry=True,
    include_names=True,
    in_place=False,
)
gdf = response.to_gpd(destring=True)
df = response.to_polars(destring=True, concat=True)
df2 = response.to_pandas(destring=True, concat=True)

#

cdh = CenDatHelper(key=os.getenv("CENSUS_API_KEY"))

cdh.list_products(years=[2023], patterns=r"acs/acs5\)")
cdh.set_products()
cdh.set_groups(["B25014"])
cdh.describe_groups()
cdh.set_geos(["150"])
response = cdh.get_data(
    include_names=True,
    include_geoids=True,
    include_geometry=True,
    within={"state": "29", "county": "189"},
    in_place=False,
)

from ntpath import join
import os
from cendat import CenDatHelper

cdh = CenDatHelper(key=os.getenv("CENSUS_API_KEY"))

cdh.list_products(years=[2023], patterns=r"/acs/acs5\)")
cdh.set_products()
cdh.set_variables("B01001_001E")  # total population
cdh.set_geos("150")
response = cdh.get_data(
    include_geometry=True,
    within={"state": ["08", "56"]},
)
df = response.to_polars(concat=True)
print(f"\nTotal rows returned: {len(df)}")

gdf = response.to_gpd(join_strategy="inner")
print(f"\nTotal rows returned: {len(gdf)}")

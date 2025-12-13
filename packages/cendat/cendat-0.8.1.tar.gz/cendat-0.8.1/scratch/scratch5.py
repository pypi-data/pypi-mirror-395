import matplotlib.pyplot as plt
import os
from cendat import CenDatHelper


cdh = CenDatHelper(key=os.getenv("CENSUS_API_KEY"))

cdh.list_products(years=[2023], patterns=r"acs/acs5\)")
cdh.set_products()
cdh.list_groups(patterns=r"^median household income")
cdh.set_groups(["B19013"])
cdh.describe_groups()
# cdh.set_variables("B01001_001E")
cdh.set_geos(["150"])
response = cdh.get_data(
    # in_place=True,
    include_names=True,
    include_geometry=True,
    within={
        "state": [
            "08",
        ],
        "county": ["069", "123", "013"],
    },
)
# df = response.to_polars(destring=True, concat=True)
gdf = response.to_gpd(destring=True, join_strategy="inner")
gdf.loc[gdf["B19013_001E"] == -666666666, "B19013_001E"] = None

fig, ax = plt.subplots(1, 1, figsize=(11, 8.5))

# Plot the choropleth map
gdf.plot(
    column="B19013_001E",  # The data column to color the states by
    cmap="viridis",  # The color map (e.g., 'viridis', 'plasma', 'inferno', 'magma')
    linewidth=0.8,  # The width of the state borders
    ax=ax,  # The axes to plot on
    legend=True,  # Show the color legend
    alpha=1.0,
    legend_kwds={
        "label": "Income",
        "orientation": "horizontal",
        "location": "bottom",
        "shrink": 0.5,
        "fraction": 0.1,
        "format": "{x:,.0f}",
    },
    missing_kwds={
        "color": "lightgrey",
        "edgecolor": "grey",
        "hatch": "////",
        "label": "Missing values",
    },
)

# Customize the plot
ax.set_title(
    "Larimer, Weld, and Boulder County Med. HH Income by block group",
    fontdict={"fontsize": "12", "fontweight": "3"},
)
ax.set_axis_off()
plt.show()

# cendat

A Python helper for the U.S. Census Bureau API.

`cendat` provides a high-level, chainable interface for discovering datasets, filtering geographies and variables, and fetching data concurrently.

## Installation

```bash
pip install cendat
```

### Optional Dependencies

```bash
pip install cendat[pandas]     # pandas support
pip install cendat[polars]     # polars support
pip install cendat[geopandas]  # geopandas support
pip install cendat[all]        # all of the above
```

## Quick Example

```python
from cendat import CenDatHelper

# Initialize with your API key
cdh = CenDatHelper(years=[2023], key="your-api-key")

# Find and select a product
cdh.list_products(patterns=r"acs/acs5\)")
cdh.set_products()

# Select geography and variables
cdh.set_geos(["050"])  # Counties
cdh.set_variables(["B01001_001E"])  # Total population

# Fetch data
response = cdh.get_data(include_names=True)
df = response.to_polars(concat=True, destring=True)
```

## Documentation

📖 **Full documentation**: [mostlyunoriginal.github.io/cendat](https://mostlyunoriginal.github.io/cendat/)

## Links

- [GitHub Repository](https://github.com/mostlyunoriginal/cendat)
- [Developer Blog](https://mostlyunoriginal.github.io/posts.html#category=cendat)
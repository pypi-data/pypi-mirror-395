# cendat

A Python helper for the U.S. Census Bureau API.

---

## What is cendat?

`cendat` simplifies exploring and retrieving data from the Census Bureau's API. It provides a high-level, chainable interface for discovering datasets, filtering geographies and variables, and fetching data concurrently.

The library handles the complexities of the Census API's structure—geographic hierarchies, inconsistent product naming, and rate limiting—so you can focus on getting the data you need.

## The List → Set → Get → Convert Workflow

cendat is built around a simple, four-step pattern:

1. **List** – Use `list_products()`, `list_geos()`, `list_groups()`, and `list_variables()` to explore what's available. Filter with regex patterns to narrow your search.

2. **Set** – Use the corresponding `set_*` methods to lock in your selections. Call these without arguments to use results from your last "List" call.

3. **Get** – Call `get_data()` to execute all necessary API calls. This handles complex geographic requirements automatically and uses thread pooling for speed.

4. **Convert & Analyze** – Use `to_polars()`, `to_pandas()`, or `to_gpd()` on the response to get your data in DataFrame format. The `tabulate()` method provides quick, Stata-like frequency tables.

## Quick Example

```python
from cendat import CenDatHelper

# Initialize with your API key (recommended to avoid rate limits)
cdh = CenDatHelper(years=[2023], key="your-api-key")

# Find and select a product
cdh.list_products(patterns=r"acs/acs5\)")
cdh.set_products()

# Select geography and variables
cdh.set_geos(["050"])  # Counties
cdh.set_variables(["B01001_001E"])  # Total population

# Fetch data and convert to DataFrame
response = cdh.get_data(include_names=True)
df = response.to_polars(concat=True, destring=True)
```

---

## Installation

Install cendat using pip:

```bash
pip install cendat
```

### Optional Dependencies

Install support for your preferred DataFrame library:

```bash
# pandas support
pip install cendat[pandas]

# geopandas support (includes pandas)
pip install cendat[geopandas]

# polars support
pip install cendat[polars]

# all of the above
pip install cendat[all]
```

---

## Getting an API Key

While cendat works without an API key, requests are subject to stricter rate limits. Get a free key at [api.census.gov/data/key_signup.html](https://api.census.gov/data/key_signup.html).

Load your key when initializing:

```python
cdh = CenDatHelper(key="your-api-key")
```

Or set it later:

```python
cdh.load_key("your-api-key")
```

---

## Next Steps

- **[Tutorials](tutorials.md)** – Detailed walkthroughs for common use cases
- **[API Reference](reference/core.md)** – Complete documentation for all classes and methods

---

## Links

- [GitHub Repository](https://github.com/mostlyunoriginal/cendat)
- [Developer Blog](https://mostlyunoriginal.github.io/posts.html#category=cendat)


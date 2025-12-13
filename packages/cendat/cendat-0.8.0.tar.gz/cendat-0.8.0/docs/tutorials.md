# Tutorials

Step-by-step guides for common cendat workflows.

---

## Tutorial 1: ACS PUMS Microdata Analysis

This tutorial demonstrates analyzing person-level microdata from the American Community Survey (ACS) Public Use Microdata Sample (PUMS).

### Goal

Get age and sex data for adults in California and Texas, then create weighted frequency tables stratified by state.

### Setup

```python
import os
from cendat import CenDatHelper
from dotenv import load_dotenv

# Load your API key from environment
load_dotenv()
cdh = CenDatHelper(years=[2022], key=os.getenv("CENSUS_API_KEY"))
```

### Step 1: Find and Select the PUMS Product

```python
# Search for the ACS 1-year PUMS product
# The \b ensures we match the exact endpoint, not subpaths
cdh.list_products(patterns=r"acs/acs1/pums\b")
cdh.set_products()
```

### Step 2: Select Geography and Variables

```python
# For PUMS, geography is simpler—we just need "state"
cdh.set_geos(values="state", by="desc")

# Select the variables we need:
# - SEX: Person's sex
# - AGEP: Person's age
# - ST: State code
# - PWGTP: Person weight (crucial for microdata!)
cdh.set_variables(names=["SEX", "AGEP", "ST", "PWGTP"])
```

### Step 3: Get Data

```python
# Fetch data for California (06) and Texas (48)
response = cdh.get_data(
    within={"state": ["06", "48"]}
)
```

### Step 4: Analyze with Tabulate

The `tabulate()` method creates Stata-style frequency tables with proper weighting:

```python
# Age distribution by sex, stratified by state
# Only adults (AGEP > 17), using person weights
response.tabulate(
    "SEX", "AGEP",
    strat_by="ST",
    weight_var="PWGTP",
    where="AGEP > 17"
)
```

### Step 5: Convert to DataFrame

```python
# For further analysis, convert to a DataFrame
df = response.to_polars(concat=True, destring=True)
print(df.head())
```

---

## Tutorial 2: ACS 5-Year Aggregate Data

This tutorial covers the most common use case: fetching aggregate statistics from the ACS 5-Year estimates.

### Goal

Get poverty statistics for all places (cities, towns, CDPs) in a state.

### Setup

```python
cdh = CenDatHelper(key=os.getenv("CENSUS_API_KEY"))
```

### Step 1: Find the ACS 5-Year Product

```python
# The \) at the end matches products ending with a closing paren,
# which filters out sub-products like /profile, /subject, etc.
cdh.list_products(years=[2023], patterns=r"acs/acs5\)")
cdh.set_products()
```

### Step 2: Explore Variable Groups

For products like ACS with thousands of variables, groups are essential:

```python
# Search for poverty-related groups
cdh.list_groups(patterns="poverty")

# Let's use B17001 (Poverty Status by Sex by Age)
cdh.set_groups("B17001")

# See what variables are in this group
cdh.describe_groups()
```

The `describe_groups()` output shows the hierarchical structure, making it easy to pick specific variables.

### Step 3: Select Variables and Geography

```python
# B17001_001E = Total population for poverty calculation
# B17001_002E = Population below poverty level
cdh.set_variables(["B17001_001E", "B17001_002E"])

# 160 = Places (cities, towns, CDPs)
cdh.set_geos(["160"])
```

### Step 4: Get Data with Names

```python
response = cdh.get_data(
    include_names=True,      # Include place names
    include_attributes=True  # Include margins of error
)
```

### Step 5: Analyze

```python
# Convert to DataFrame
df = response.to_polars(concat=True, destring=True)
df.glimpse()

# Quick tabulation: how many places have >10,000 population?
response.tabulate("state", where="B17001_001E > 10_000")

# Weighted by population
response.tabulate(
    "state",
    weight_var="B17001_001E",
    where="B17001_001E > 10_000"
)
```

---

## Tutorial 3: Multi-Year Comparisons

cendat makes it easy to compare data across multiple years.

### Goal

Find Colorado incorporated places with very low poverty rates across recent years.

### Setup

```python
cdh = CenDatHelper(key=os.getenv("CENSUS_API_KEY"))

# Request multiple years at once
cdh.list_products(years=[2020, 2021, 2022, 2023], patterns=r"acs/acs5\)")
cdh.set_products()
```

### Step 2: Select Data

```python
cdh.set_groups(["B17001"])
cdh.set_geos(["160"])  # Places
```

### Step 3: Get Data

```python
# Filter to Colorado (state = 08)
response = cdh.get_data(
    include_names=True,
    within={"state": "08"}
)
```

### Step 4: Complex Filtering with Tabulate

The `where` parameter supports multiple conditions:

```python
response.tabulate(
    "NAME",
    "B17001_002E",  # Below poverty
    "B17001_001E",  # Total
    where=[
        "B17001_001E > 1_000",                    # Population > 1,000
        "B17001_002E / B17001_001E < 0.01",       # Poverty rate < 1%
        "'CDP' not in NAME",                      # Exclude CDPs
    ],
    weight_var="B17001_001E",
    strat_by="vintage"  # Separate results by year
)
```

!!! tip "Condition Syntax"
    The `where` parameter supports:
    
    - Simple comparisons: `"AGEP > 17"`
    - Division expressions: `"B17001_002E / B17001_001E < 0.01"`
    - String containment: `"'CDP' not in NAME"`

---

## Tutorial 4: Working with Geometries

cendat can fetch geographic boundaries alongside your data for mapping.

### Goal

Get race data with geometries for US regions.

### Setup

```python
cdh = CenDatHelper(key=os.getenv("CENSUS_API_KEY"))
cdh.list_products(years=[2011], patterns=r"acs/acs5\)")
cdh.set_products()
```

### Step 2: Select Data and Geography

```python
cdh.list_groups(patterns=r"^race")
cdh.set_groups(["B02001"])
cdh.describe_groups()

# 020 = Region
cdh.set_geos(["020"])
```

### Step 3: Get Data with Geometry

```python
response = cdh.get_data(
    include_names=True,
    include_geometry=True  # This fetches boundaries from TIGERweb
)
```

### Step 4: Convert to GeoDataFrame

```python
# to_gpd() returns a GeoDataFrame ready for mapping
gdf = response.to_gpd(destring=True, join_strategy="inner")
print(gdf)

# Use with matplotlib, folium, or your preferred mapping library
gdf.plot(column="B02001_001E", legend=True)
```

!!! note "Supported Geographies"
    Geometry fetching currently supports: regions (020), divisions (030), states (040), counties (050), county subdivisions (060), census tracts (140), block groups (150), and places (160).

---

## Tutorial 5: CPS Microdata

The Current Population Survey (CPS) supplements provide specialized microdata on topics like tobacco use, voting, and food security.

### Goal

Analyze tobacco use patterns across states using multi-year CPS data.

### Setup

```python
cdh = CenDatHelper(key=os.getenv("CENSUS_API_KEY"))

# Get multiple years of CPS Tobacco Use Supplement
cdh.list_products(years=[2022, 2023], patterns="/cps/tobacco")
cdh.set_products()
```

### Step 2: Explore and Select Variables

```python
# See available variable groups
cdh.list_groups()

# Select specific variables
# PEA1, PEA3: Tobacco use questions
# PWNRWGT: Person weight
cdh.set_variables(["PEA1", "PEA3", "PWNRWGT"])
cdh.set_geos("state", "desc")
```

### Step 3: Get Data

```python
response = cdh.get_data(within={"state": ["06", "48"]})
```

### Step 4: Analyze with Pooled Weights

When combining multiple survey years, divide the weights:

```python
response.tabulate(
    "PEA1",
    "PEA3",
    strat_by="state",
    weight_var="PWNRWGT",
    weight_div=3  # Divide weight for pooled years
)
```

---

## Tips and Best Practices

### Finding the Right Product

Use regex patterns to filter products efficiently:

```python
# ACS 5-year (main product, not profiles/subjects)
cdh.list_products(patterns=r"acs/acs5\)")

# ACS 1-year PUMS
cdh.list_products(patterns=r"acs/acs1/pums\b")

# Decennial Census
cdh.list_products(patterns="dec/")
```

### Using Groups Effectively

For products with many variables (ACS, Decennial), always start with groups:

```python
cdh.list_groups(patterns="your topic")
cdh.set_groups("GROUP_NAME")
cdh.describe_groups()  # See variable hierarchy
```

### Rate Limiting

For large requests, adjust `max_workers`:

```python
# For thousands of API calls, reduce concurrency
response = cdh.get_data(max_workers=50)
```

### The `in_place` Option

For iterative work or building up complex queries:

```python
# Keep data attached to the helper object
cdh.get_data(in_place=True)

# Access later via helper['params']
```

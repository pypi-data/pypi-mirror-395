# Tutorials

Step-by-step guides for common cendat workflows. Each tutorial is a fully executable Jupyter notebook with real Census API outputs.

---

## Interactive Tutorials

| Tutorial | Description |
|----------|-------------|
| [ACS PUMS Microdata](tutorials/01_pums_microdata.ipynb) | Analyze person-level microdata with weighted frequency tables |
| [ACS 5-Year Aggregate](tutorials/02_acs5_aggregate.ipynb) | Fetch aggregate statistics for places (cities, towns, CDPs) |
| [Multi-Year Comparisons](tutorials/03_multi_year.ipynb) | Compare data across multiple years with complex filtering |
| [Working with Geometries](tutorials/04_geometries.ipynb) | Fetch geographic boundaries for mapping |
| [CPS Microdata](tutorials/05_cps_microdata.ipynb) | Analyze CPS supplement data with pooled weights |

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
response = cdh.get_data(max_workers=25)
```

### The `in_place` Option

For iterative work or building up complex queries:

```python
# Keep data attached to the helper object
cdh.get_data(in_place=True)

# Access later via helper['params']
```

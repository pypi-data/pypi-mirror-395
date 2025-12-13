import time
import re
import requests
import itertools
import builtins
import copy
from collections import defaultdict
from typing import List, Union, Tuple, Dict, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from .CenDatResponse import CenDatResponse
from importlib.util import find_spec


class CenDatHelper:
    """
    A helper for exploring and retrieving data from the US Census Bureau API.

    This class provides a chainable, stateful interface to list, select, and
    combine datasets, geographies, and variables to build and execute API calls.

    Attributes:
        years (List[int]): The primary year or years of interest for data queries.
        products (List[Dict]): The currently selected data product details.
        geos (List[Dict]): The currently selected geographies.
        groups (List[Dict]): The currently selected variable groups.
        variables (List[Dict]): The currently selected variables.
        params (List[Dict]): The combined geo/variable parameters for API calls.
        n_calls (int): The number of API calls that will be made by get_data().
    """

    def __init__(
        self, years: Optional[Union[int, List[int]]] = None, key: Optional[str] = None
    ):
        """
        Initializes the CenDatHelper object.

        Args:
            years (Union[int, List[int]], optional): The year or years of
                interest. If provided, they are set upon initialization.
                Defaults to None.
            key (str, optional): A Census Bureau API key to load upon
                initialization. Defaults to None.
        """
        self.years: Optional[List[int]] = None
        self.products: List[Dict] = []
        self.geos: List[Dict] = []
        self.groups: List[Dict] = []
        self.variables: List[Dict] = []
        self.params: List[Dict] = []
        self.__key: Optional[str] = None
        self._products_cache: Optional[List[Dict[str, str]]] = None
        self._filtered_products_cache: Optional[List[Dict]] = None
        self._filtered_geos_cache: Optional[List[Dict]] = None
        self._filtered_groups_cache: Optional[List[Dict]] = None
        self._filtered_variables_cache: Optional[List[Dict]] = None
        self.n_calls: Optional[int] = None
        self.call_type: Optional[str] = None

        if years is not None:
            self.set_years(years)
        if key is not None:
            self.load_key(key)

    def __getitem__(self, key: str) -> Union[List[Dict], Optional[int]]:
        """
        Allows dictionary-style access to key attributes.

        Args:
            key (str): The attribute to access. One of 'products', 'geos',
                       'groups', 'variables', 'params', or 'n_calls'.

        Returns:
            The value of the requested attribute.

        Raises:
            KeyError: If the key is not a valid attribute name.
        """
        if key == "products":
            return self.products
        elif key == "geos":
            return self.geos
        elif key == "groups":
            return self.groups
        elif key == "variables":
            return self.variables
        elif key == "params":
            return self.params
        elif key == "n_calls":
            return self.n_calls
        else:
            raise KeyError(
                f"'{key}' is not a valid key. Available keys are: 'products', 'geos', 'groups', 'variables', 'params', 'n_calls'"
            )

    def set_years(self, years: Union[int, List[int]]):
        """
        Sets the object's active years for filtering API metadata.

        Args:
            years (Union[int, List[int]]): The year or list of years to set.

        Raises:
            TypeError: If `years` is not an integer or a list of integers.
        """
        if isinstance(years, int):
            self.years = [years]
        elif isinstance(years, list) and all(isinstance(y, int) for y in years):
            self.years = sorted(list(set(years)))
        else:
            raise TypeError("'years' must be an integer or a list of integers.")
        print(f"✅ Years set to: {self.years}")

    def load_key(self, key: Optional[str] = None):
        """
        Loads a Census API key for authenticated requests.

        Using a key is recommended to avoid stricter rate limits on anonymous
        requests.

        Args:
            key (str, optional): The API key string. Defaults to None.
        """
        if key:
            self.__key = key
            print("✅ API key loaded successfully.")
        else:
            print("⚠️ No API key provided. API requests may have stricter rate limits.")

    def _request_with_retry(
        self,
        url: str,
        params: Optional[Dict] = None,
        timeout: int = 30,
        max_retries: int = 3,
        backoff_base: int = 2,
    ) -> requests.Response:
        """
        Makes an HTTP GET request with automatic retry on connection errors.

        Handles transient network failures (ConnectionError, Timeout, OSError)
        with exponential backoff. Does NOT retry on HTTP error status codes
        (those are handled by the caller via raise_for_status).

        Args:
            url (str): The URL to fetch.
            params (Dict, optional): Query parameters.
            timeout (int): Request timeout in seconds.
            max_retries (int): Maximum retry attempts on connection errors.
            backoff_base (int): Base for exponential backoff calculation.

        Returns:
            requests.Response: The response object.

        Raises:
            requests.exceptions.RequestException: If all retries fail.
        """
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                return requests.get(url, params=params, timeout=timeout)
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                OSError,
            ) as e:
                last_exception = e
                if attempt < max_retries:
                    backoff = backoff_base ** (attempt + 1)
                    print(
                        f"⚠️ Connection error ({type(e).__name__}), retrying in {backoff}s... "
                        f"(attempt {attempt + 1}/{max_retries})"
                    )
                    time.sleep(backoff)
                else:
                    print(f"❌ Connection failed after {max_retries} retries: {e}")
                    raise
        # This should never be reached, but just in case
        raise last_exception

    def _get_json_from_url(
        self, url: str, params: Optional[Dict] = None, timeout: int = 30
    ) -> Optional[List[List[str]]]:
        """
        Internal helper to fetch and parse JSON from a URL with error handling.

        Args:
            url (str): The URL to fetch.
            params (Dict, optional): Dictionary of query parameters.
            timeout (int): Request timeout in seconds.

        Returns:
            Optional[List[List[str]]]: The parsed JSON data (typically a list of lists), or None if an error occurs.
        """
        if not params:
            params = {}
        if self.__key:
            params["key"] = self.__key

        try:
            response = self._request_with_retry(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        # The Census API can return a 200 OK with an error message in the body
        # that is not valid JSON. This is common when a requested geography
        # does not exist within a parent geography (e.g., a tract in the wrong county).
        except requests.exceptions.JSONDecodeError as e:
            print(f"❌ Failed to decode JSON from {url}. Server response: {e}")
            params_minus = {key: value for key, value in params.items() if key != "key"}
            print(f"Query parameters: {params_minus}")
            print(
                "Note: this may be the result of the 'in' geography being a special case "
                "in which the 'for' summary level does not exist. All valid parent geographies "
                "are queried without regard for whether or not the requested summary level exists "
                "within them. If this is the case, your results will still be valid (barring other "
                "errors)."
            )
        except requests.exceptions.RequestException as e:
            error_message = str(e)
            if e.response is not None:
                api_error = e.response.text.strip()
                if api_error:
                    error_message += f" - API Message: {api_error}"
            print(
                f"❌ Error fetching data from {url} with params {params}: {error_message}"
            )
        return None

    def _get_json_from_url_with_status(
        self, url: str, params: Optional[Dict] = None, timeout: int = 30
    ) -> Tuple[Optional[List[List[str]]], Optional[int]]:
        """
        Internal helper to fetch and parse JSON from a URL, returning status code.

        This variant of _get_json_from_url returns a tuple of (data, status_code)
        to enable retry logic to distinguish between retryable server errors
        (429, 5xx) and non-retryable client errors (4xx).

        Args:
            url (str): The URL to fetch.
            params (Dict, optional): Dictionary of query parameters.
            timeout (int): Request timeout in seconds.

        Returns:
            Tuple[Optional[List[List[str]]], Optional[int]]: A tuple of (parsed JSON data, HTTP status code). Returns (None, status_code) on error, or (None, None) on connection/timeout errors.
        """
        if not params:
            params = {}
        if self.__key:
            params["key"] = self.__key

        try:
            response = self._request_with_retry(url, params=params, timeout=timeout)
            status_code = response.status_code
            response.raise_for_status()
            return response.json(), status_code
        except requests.exceptions.JSONDecodeError:
            # Server returned 200 but invalid JSON - treat as success with no data
            return None, response.status_code if 'response' in dir() else None
        except requests.exceptions.RequestException as e:
            status_code = e.response.status_code if e.response is not None else None
            return None, status_code

    def _parse_vintage(self, vintage_input: Union[str, int]) -> List[int]:
        """
        Internal helper to parse a vintage value, which can be a single year
        (e.g., 2022) or a multi-year range (e.g., "2018-2022").

        Robustly parses a vintage value which can be a single year or a range.

        Args:
            vintage_input (Union[str, int]): The vintage string or integer
                                             (e.g., 2020, "2010-2014").

        Returns:
            List[int]: A list of integer years.
        """
        if not vintage_input:
            return []
        vintage_str = str(vintage_input)
        try:
            if "-" in vintage_str:
                start, end = map(int, vintage_str.split("-"))
                return list(range(start, end + 1))
            return [int(vintage_str)]
        except (ValueError, TypeError):
            return []

    def list_products(
        self,
        years: Optional[Union[int, List[int]]] = None,
        patterns: Optional[Union[str, List[str]]] = None,
        to_dicts: bool = True,
        logic: Callable[[iter], bool] = all,
        match_in: str = "title",
    ) -> Union[List[str], List[Dict[str, str]]]:
        """
        Lists available data products, with options for filtering.

        Fetches all available datasets from the main Census API endpoint and
        filters them based on year and string patterns. Results are cached
        for subsequent calls.

        Args:
            years (Union[int, List[int]], optional): Filter products available
                for this year or list of years. Defaults to years set on the object.
            patterns (Union[str, List[str]], optional): A regex pattern or list
                of patterns to search for in the product metadata.
            to_dicts (bool): If True (default), returns a list of dictionaries
                with full product details. If False, returns a list of titles.
            logic (Callable): The function to apply when multiple `patterns` are
                provided. Use `all` (default) for AND logic or `any` for OR logic.
            match_in (str): The metadata field to search within. Must be 'title'
                (default) or 'desc'.

        Returns:
            A list of product dictionaries or a list of product titles.
        """
        # Strategy: Fetch all products from the main data.json endpoint once and cache them.
        # Subsequent calls will use the cache and apply filters.
        if not self._products_cache:
            data = self._get_json_from_url("https://api.census.gov/data.json")
            if not data or "dataset" not in data:
                return []
            products = []
            for d in data["dataset"]:
                is_micro = str(d.get("c_isMicrodata", "false")).lower() == "true"
                is_agg = str(d.get("c_isAggregate", "false")).lower() == "true"
                # We only support aggregate and microdata products, not timeseries or other types.
                if not is_micro and not is_agg:
                    continue

                access_url = next(
                    (
                        dist.get("accessURL")
                        for dist in d.get("distribution", [])
                        if "api.census.gov/data" in dist.get("accessURL", "")
                    ),
                    None,
                )
                if not access_url:
                    continue
                c_dataset_val = d.get("c_dataset")
                dataset_type = "N/A"
                if isinstance(c_dataset_val, list) and len(c_dataset_val) > 1:
                    dataset_type = "/".join(c_dataset_val)
                elif isinstance(c_dataset_val, str):
                    dataset_type = c_dataset_val

                # Create a more descriptive and unique title by appending the API path fragment.
                # This helps distinguish between similarly named products (e.g., ACS1 vs ACS5).
                title = d.get("title")
                title = (
                    f"{title} ({re.sub(r'http://api.census.gov/data/','', access_url)})"
                )

                products.append(
                    {
                        "title": title,
                        "desc": d.get("description"),
                        "vintage": self._parse_vintage(d.get("c_vintage")),
                        "type": dataset_type,
                        "url": access_url,
                        "is_microdata": is_micro,
                        "is_aggregate": is_agg,
                    }
                )
            self._products_cache = products

        # Apply filters based on the provided arguments or the object's state.
        target_years = self.years
        if years is not None:
            target_years = [years] if isinstance(years, int) else list(years)

        filtered = self._products_cache
        if target_years:
            target_set = set(target_years)
            filtered = [
                p
                for p in filtered
                if p.get("vintage") and target_set.intersection(p["vintage"])
            ]

        if patterns:
            if match_in not in ["title", "desc"]:
                print("❌ Error: `match_in` must be either 'title' or 'desc'.")
                return []
            pattern_list = [patterns] if isinstance(patterns, str) else patterns
            try:
                regexes = [re.compile(p, re.IGNORECASE) for p in pattern_list]
                filtered = [
                    p
                    for p in filtered
                    if p.get(match_in)
                    and logic(regex.search(p[match_in]) for regex in regexes)
                ]
            except re.error as e:
                print(f"❌ Invalid regex pattern: {e}")
                return []

        self._filtered_products_cache = filtered
        return filtered if to_dicts else [p["title"] for p in filtered]

    def set_products(self, titles: Optional[Union[str, List[str]]] = None):
        """
        Sets the active data products for subsequent method calls.

        Args:
            titles (Union[str, List[str]], optional): The title or list of
                titles of the products to set. If None, sets all products from
                the last `list_products` call.
        """
        prods_to_set = []
        if titles is None:
            if not self._filtered_products_cache:
                print("❌ Error: No products to set. Run `list_products` first.")
                return
            prods_to_set = self._filtered_products_cache
        else:
            title_list = [titles] if isinstance(titles, str) else titles
            all_prods = self.list_products(to_dicts=True, years=self.years or [])
            for title in title_list:
                matching_products = [p for p in all_prods if p.get("title") == title]
                if not matching_products:
                    print(
                        f"⚠️ Warning: No product with the title '{title}' found. Skipping."
                    )
                    continue
                prods_to_set.extend(matching_products)

        if not prods_to_set:
            print("❌ Error: No valid products were found to set.")
            return

        self.products = []
        self.groups = []
        self.variables = []
        self.geos = []
        for product in prods_to_set:
            product["base_url"] = product.get("url", "")
            self.products.append(product)
            print(
                f"✅ Product set: '{product['title']}' (Vintage: {product.get('vintage')})"
            )

    def list_geos(
        self,
        to_dicts: bool = False,
        patterns: Optional[Union[str, List[str]]] = None,
        logic: Callable[[iter], bool] = all,
    ) -> Union[List[str], List[Dict[str, str]]]:
        """
        Lists available geographies for the currently set products.

        Args:
            to_dicts (bool): If True, returns a list of dictionaries with full
                geography details. If False (default), returns a sorted list of
                unique summary level names ('sumlev').
            patterns (Union[str, List[str]], optional): A regex pattern or list
                of patterns to search for in the geography description.
            logic (Callable): The function to apply when multiple `patterns` are
                provided. Use `all` (default) for AND logic or `any` for OR logic.

        Returns:
            A list of geography dictionaries or a list of summary level strings.
        """
        # Strategy: Iterate through each set product, fetch its specific geography.json,
        # and aggregate all available geographies into a single flat list.
        if not self.products:
            print("❌ Error: Products must be set first via `set_products()`.")
            return []
        flat_geo_list = []
        for product in self.products:
            url = f"{product['base_url']}/geography.json"
            data = self._get_json_from_url(url)
            if not data or "fips" not in data:
                continue
            for geo_info in data["fips"]:
                sumlev = geo_info.get("geoLevelDisplay")
                if not sumlev:
                    continue
                # Capture all relevant metadata for each geography, including the keys
                # needed to determine API call structure (requires, wildcard, etc.).
                flat_geo_list.append(
                    {
                        "sumlev": sumlev,
                        "desc": geo_info.get("name"),
                        "product": product["title"],
                        "vintage": product["vintage"],
                        "requires": geo_info.get("requires"),
                        "wildcard": geo_info.get("wildcard"),
                        "optionalWithWCFor": geo_info.get("optionalWithWCFor"),
                        "url": product["url"],
                    }
                )
        result_list = flat_geo_list
        if patterns:
            pattern_list = [patterns] if isinstance(patterns, str) else patterns
            try:
                regexes = [re.compile(p, re.IGNORECASE) for p in pattern_list]
                result_list = [
                    g
                    for g in result_list
                    if g.get("desc")
                    and logic(regex.search(g["desc"]) for regex in regexes)
                ]
            except re.error as e:
                print(f"❌ Invalid regex pattern: {e}")
                return []
        self._filtered_geos_cache = result_list
        return (
            result_list
            if to_dicts
            else sorted(list(set([g["sumlev"] for g in result_list])))
        )

    def set_geos(
        self,
        values: Optional[Union[str, List[str]]] = None,
        by: str = "sumlev",
    ):
        """
        Sets the active geographies for data retrieval.

        Args:
            values (Union[str, List[str]], optional): The geography values to set.
                If None, sets all geos from the last `list_geos` call.
            by (str): The key to use for matching `values`. Must be either
                'sumlev' (default) or 'desc'.
        """
        if by not in ["sumlev", "desc"]:
            print("❌ Error: `by` must be either 'sumlev' or 'desc'.")
            return

        geos_to_set = []
        if values is None:
            if not self._filtered_geos_cache:
                print("❌ Error: No geos to set. Run `list_geos` first.")
                return
            geos_to_set = self._filtered_geos_cache
        else:
            value_list = [values] if isinstance(values, str) else values
            all_geos = self.list_geos(to_dicts=True)
            geos_to_set = [g for g in all_geos if g.get(by) in value_list]

        if not geos_to_set:
            print("❌ Error: No valid geographies were found to set.")
            return

        # Microdata products have a constraint: you can only query for one type of
        # geography at a time (e.g., PUMAs within states).
        is_microdata_present = any(
            p.get("is_microdata")
            for p in self.products
            if p["title"] in [g["product"] for g in geos_to_set]
        )

        unique_geos = set(g["desc"] for g in geos_to_set)
        if is_microdata_present and len(unique_geos) > 1:
            print(
                "❌ Error: Only a single geography type (e.g., 'public use microdata area') can be set when working with microdata products."
            )
            return

        self.geos = geos_to_set
        # Create a user-friendly message summarizing the requirements for the set geos.
        # This helps the user know what to provide in the `get_data` `within` clause.
        messages = {}
        for geo in self.geos:
            desc = geo["desc"]
            reqs = geo.get("requires") or []
            if desc not in messages:
                messages[desc] = set(reqs)
            else:
                messages[desc].update(reqs)
        message_parts = []
        for desc, reqs in messages.items():
            if reqs:
                message_parts.append(
                    f"'{desc}' (requires `within` for: {', '.join(sorted(list(reqs)))})"
                )
            else:
                message_parts.append(f"'{desc}'")
        print(f"✅ Geographies set: {', '.join(message_parts)}")

    def list_groups(
        self,
        to_dicts: bool = True,
        patterns: Optional[Union[str, List[str]]] = None,
        logic: Callable[[iter], bool] = all,
        match_in: str = "description",
    ) -> Union[List[str], List[Dict[str, str]]]:
        """
        Lists available variable groups for the currently set products.

        Args:
            to_dicts (bool): If True (default), returns a list of dictionaries
                with full group details. If False, returns a sorted list of
                unique group names.
            patterns (Union[str, List[str]], optional): A regex pattern or list
                of patterns to search for in the group metadata.
            logic (Callable): The function to apply when multiple `patterns` are
                provided. Use `all` (default) for AND logic or `any` for OR logic.
            match_in (str): The metadata field to search within. Must be
                'description' (default) or 'name'.

        Returns:
            A list of group dictionaries or a list of group name strings.
        """
        # Strategy: Similar to list_geos, iterate through each set product,
        # fetch its groups.json, and aggregate the results.
        if not self.products:
            print("❌ Error: Products must be set first via `set_products()`.")
            return []

        flat_group_list = []
        for product in self.products:
            url = f"{product['base_url']}/groups.json"
            data = self._get_json_from_url(url)
            if not data or "groups" not in data:
                continue
            for group_details in data["groups"]:
                flat_group_list.append(
                    {
                        "name": group_details.get("name", "N/A"),
                        "description": group_details.get("description", "N/A"),
                        "product": product["title"],
                        "vintage": product["vintage"],
                        "url": product["url"],
                    }
                )
        result_list = flat_group_list

        if match_in not in ["description", "name"]:
            print("❌ Error: `match_in` must be either 'description' or 'name'.")
            return []

        if patterns:
            pattern_list = [patterns] if isinstance(patterns, str) else patterns
            try:
                regexes = [re.compile(p, re.IGNORECASE) for p in pattern_list]
                result_list = [
                    g
                    for g in result_list
                    if g.get(match_in)
                    and logic(regex.search(g[match_in]) for regex in regexes)
                ]
            except re.error as e:
                print(f"❌ Invalid regex pattern: {e}")
                return []

        self._filtered_groups_cache = result_list
        return (
            result_list
            if to_dicts
            else sorted(list(set([g["name"] for g in result_list])))
        )

    def set_groups(self, names: Optional[Union[str, List[str]]] = None):
        """
        Sets the active variable groups for subsequent method calls.

        Args:
            names (Union[str, List[str]], optional): The name or list of names
                of the groups to set. If None, sets all groups from the
                last `list_groups` call.
        """
        groups_to_set = []
        if names is None:
            if not self._filtered_groups_cache:
                print("❌ Error: No groups to set. Run `list_groups` first.")
                return
            groups_to_set = self._filtered_groups_cache
        else:
            name_list = [names] if isinstance(names, str) else names
            all_groups = self.list_groups(to_dicts=True)
            groups_to_set = [g for g in all_groups if g.get("name") in name_list]

        if not groups_to_set:
            print("❌ Error: No valid groups were found to set.")
            return

        self.groups = groups_to_set
        self.variables = []
        unique_names = sorted(list(set(g["name"] for g in self.groups)))
        print(f"✅ Groups set: {', '.join(unique_names)}")

    def describe_groups(self, groups: Optional[Union[str, List[str]]] = None):
        """
        Displays the variables within specified groups in a formatted, indented list.

        This method fetches all variables for the currently set products and
        filters them to show only those belonging to the specified groups. The
        output is formatted to reflect the hierarchical structure of the variables
        as indicated by their labels.

        Args:
            groups (Union[str, List[str]], optional): A group name or list of
                names to describe. If None, it will use the groups previously
                set on the helper object via `set_groups()`.
        """
        if not self.products:
            print("❌ Error: Products must be set first via `set_products()`.")
            return

        # Determine which groups to filter by
        groups_to_filter = None
        if groups is not None:
            groups_to_filter = groups
        elif self.groups:
            groups_to_filter = [g["name"] for g in self.groups]

        if not groups_to_filter:
            print(
                "❌ Error: No groups specified or set. Use `set_groups()` or the 'groups' parameter."
            )
            return

        if isinstance(groups_to_filter, str):
            groups_to_filter = [groups_to_filter]

        # A set is used for efficient lookup of whether a variable's group
        # is in the list of groups to be described.
        group_set = set(groups_to_filter)

        # Fetch all variables and group descriptions
        all_vars = self.list_variables(to_dicts=True)
        all_groups_details = self.list_groups(to_dicts=True)

        # Create a lookup for group descriptions
        group_descriptions = {g["name"]: g["description"] for g in all_groups_details}

        # Filter variables that belong to the selected groups
        group_vars = [v for v in all_vars if v.get("group") in group_set]

        if not group_vars:
            print(
                f"ℹ️ No variables found for the specified group(s): {', '.join(group_set)}"
            )
            return

        # Organize variables by group and product/vintage for structured printing
        vars_by_group_product = {}
        for var in group_vars:
            key = (var["group"], var["product"], var["vintage"][0])
            if key not in vars_by_group_product:
                vars_by_group_product[key] = []
            vars_by_group_product[key].append(var)

        # Print the formatted output
        last_group_printed = None
        for key in sorted(vars_by_group_product.keys()):
            group_name, product_title, vintage = key

            if group_name != last_group_printed:
                group_desc = group_descriptions.get(
                    group_name, "No description available."
                )
                # Print a header for each new group.
                print(f"\n--- Group: {group_name} ({group_desc}) ---")
                last_group_printed = group_name

            print(f"\n  Product: {product_title} (Vintage: {vintage})")

            sorted_vars = sorted(vars_by_group_product[key], key=lambda x: x["name"])

            for var in sorted_vars:
                label = var.get("label", "")

                # The Census API uses "!!" in variable labels to denote hierarchy.
                # We can use the count of this delimiter to determine indentation depth.
                depth = label.count("!!")
                indent = "  " * depth

                # Get the last part of the label after splitting by '!!'
                final_label_part = label.split("!!")[-1]

                print(f"    {indent}{var['name']}: {final_label_part.strip()}")

    def list_variables(
        self,
        to_dicts: bool = True,
        patterns: Optional[Union[str, List[str]]] = None,
        logic: Callable[[iter], bool] = all,
        match_in: str = "label",
        groups: Optional[Union[str, List[str]]] = None,
    ) -> Union[List[str], List[Dict[str, str]]]:
        """
        Lists available variables for the currently set products.

        Args:
            to_dicts (bool): If True (default), returns a list of dictionaries
                with full variable details. If False, returns a sorted list of
                unique variable names.
            patterns (Union[str, List[str]], optional): A regex pattern or list
                of patterns to search for in the variable metadata.
            logic (Callable): The function to apply when multiple `patterns` are
                provided. Use `all` (default) for AND logic or `any` for OR logic.
            match_in (str): The metadata field to search within. Must be 'label'
                (default), 'name', or 'concept'.
            groups (Union[str, List[str]], optional): A group name or list of
                names to filter variables by. If provided, only variables
                belonging to these groups will be returned.

        Returns:
            A list of variable dictionaries or a list of variable name strings.
        """
        # Strategy: Iterate through each set product, fetch its variables.json,
        # and aggregate all available variables into a single flat list.
        if not self.products:
            print("❌ Error: Products must be set first via `set_products()`.")
            return []
        flat_variable_list = []
        for product in self.products:
            url = f"{product['base_url']}/variables.json"
            data = self._get_json_from_url(url)
            if not data or "variables" not in data:
                continue
            for name, details in data["variables"].items():
                # Exclude reserved names used by the API for query parameters.
                if name in ["GEO_ID", "for", "in", "ucgid"]:
                    continue
                flat_variable_list.append(
                    {
                        "name": name,
                        "label": details.get("label", "N/A"),
                        "concept": details.get("concept", "N/A"),
                        "group": details.get("group", "N/A"),
                        "values": details.get("values", "N/A"),
                        "type": details.get("predicateType", "N/A"),
                        "attributes": details.get("attributes", "N/A"),
                        "sugg_wgt": details.get("suggested-weight", "N/A"),
                        "product": product["title"],
                        "vintage": product["vintage"],
                        "url": product["url"],
                    }
                )
        result_list = flat_variable_list

        # Determine which groups to filter by: use the 'groups' parameter if
        # provided, otherwise fall back to the groups set on the object.
        groups_to_filter = None
        if groups is not None:
            groups_to_filter = groups
        elif self.groups:
            # Extract group names from the list of group dictionaries
            groups_to_filter = [g["name"] for g in self.groups]

        # Apply the group filter if there are any groups to filter by
        if groups_to_filter:
            # Ensure groups_to_filter is a list for set creation
            if isinstance(groups_to_filter, str):
                groups_to_filter = [groups_to_filter]
            group_set = set(groups_to_filter)
            result_list = [v for v in result_list if v.get("group") in group_set]

        if match_in not in ["label", "name", "concept"]:
            print("❌ Error: `match_in` must be either 'label', 'name', or 'concept'.")
            return []

        if patterns:
            pattern_list = [patterns] if isinstance(patterns, str) else patterns
            try:
                regexes = [re.compile(p, re.IGNORECASE) for p in pattern_list]
                result_list = [
                    v
                    for v in result_list
                    if v.get(match_in)
                    and logic(regex.search(v[match_in]) for regex in regexes)
                ]
            except re.error as e:
                print(f"❌ Invalid regex pattern: {e}")
                return []

        self._filtered_variables_cache = result_list
        return (
            result_list
            if to_dicts
            else sorted(list(set([v["name"] for v in result_list])))
        )

    def set_variables(
        self,
        names: Optional[Union[str, List[str]]] = None,
    ):
        """
        Sets the active variables for data retrieval.

        Args:
            names (Union[str, List[str]], optional): The name or list of names
                of the variables to set. If None, sets all variables from the
                last `list_variables` call.
        """
        vars_to_set = []
        if names is None:
            if not self._filtered_variables_cache:
                print("❌ Error: No variables to set. Run `list_variables` first.")
                return
            vars_to_set = self._filtered_variables_cache
        else:
            name_list = [names] if isinstance(names, str) else names
            all_vars = self.list_variables(to_dicts=True, patterns=None)
            vars_to_set = [v for v in all_vars if v.get("name") in name_list]
        if not vars_to_set:
            print("❌ Error: No valid variables were found to set.")
            return
        # Collapse the list of variables by product and vintage. This is a crucial
        # step to group all variables that can be requested in a single API call,
        # as each call is specific to one product/vintage.
        collapsed_vars = {}
        for var_info in vars_to_set:
            key = (var_info["product"], tuple(var_info["vintage"]), var_info["url"])
            if key not in collapsed_vars:
                collapsed_vars[key] = {
                    "product": var_info["product"],
                    "vintage": var_info["vintage"],
                    "url": var_info["url"],
                    "names": [],
                    "labels": [],
                    "values": [],
                    "types": [],
                    "attributes": [],
                    "sugg_wgts": [],
                }
            for collapsed, granular in zip(
                ["names", "labels", "values", "types", "attributes", "sugg_wgts"],
                ["name", "label", "values", "type", "attributes", "sugg_wgt"],
            ):
                collapsed_vars[key][collapsed].append(var_info[granular])
        self.variables = list(collapsed_vars.values())
        self.call_type = "variable"
        print("✅ Variables set:")
        for var_group in self.variables:
            print(
                f"  - Product: {var_group['product']} (Vintage: {var_group['vintage']})"
            )
            print(f"    Variables: {', '.join(var_group['names'])}")

    def _create_params(self):
        """
        Internal method to combine set geos, variables, and/or groups into API parameters.

        This method joins the user-selected geographies with either selected
        variables or a single selected group, based on matching product and vintage.
        This creates the final parameter sets for `get_data`.

        The logic handles two main scenarios:
        1. The user has explicitly set variables via `set_variables()`.
        2. The user has set groups via `set_groups()` and expects the library to
           fetch all variables within those groups. This is only valid if exactly
           one group is specified per product/vintage combination.
        This creates the final parameter sets for `get_data`.
        """
        if not self.geos:
            print("❌ Error: Geographies must be set before creating parameters.")
            return

        self.params = []  # Reset params

        micro_indicators = {
            p["url"]: p.get("is_microdata", False) for p in self.products
        }

        # Case 1: Variables are set (standard behavior)
        if self.variables and not self.call_type == "group":
            for geo in self.geos:
                for var_group in self.variables:
                    if (
                        geo["product"] == var_group["product"]
                        and geo["vintage"] == var_group["vintage"]
                        and geo["url"] == var_group["url"]
                    ):
                        # Combine the geography and variable information into a single
                        # parameter dictionary.
                        self.params.append(
                            {
                                "product": geo["product"],
                                "vintage": geo["vintage"],
                                "sumlev": geo["sumlev"],
                                "desc": geo["desc"],
                                "requires": geo.get("requires"),
                                "wildcard": geo.get("wildcard"),
                                "optionalWithWCFor": geo.get("optionalWithWCFor"),
                                "names": var_group["names"],
                                "labels": var_group["labels"],
                                "values": var_group["values"],
                                "types": var_group["types"],
                                "attributes": var_group["attributes"],
                                "url": geo["url"],
                                "is_microdata": micro_indicators[geo["url"]],
                            }
                        )

        # Case 2: No variables, but exactly one group is set per vintage * geo
        elif self.groups:
            # First, verify that exactly one group is set for each product URL.
            # The Census API's `group()` parameter can only handle one group at a time.
            groups_by_url = defaultdict(set)
            for group in self.groups:
                groups_by_url[group["url"]].add(group["name"])

            # Check if any product/vintage has more than one group selected.
            # This is invalid because we can only request one 'group()' per API call.
            if any(len(names) > 1 for names in groups_by_url.values()):
                print(
                    "❌ Error: You must set variables if any set product has more than 1 set group."
                )
                return

            _ = self.list_variables()
            self.set_variables()
            self.call_type = "group"

            for geo in self.geos:
                for i, group in enumerate(self.groups):
                    if (
                        geo["product"] == group["product"]
                        and geo["vintage"] == group["vintage"]
                        and geo["url"] == group["url"]
                    ):
                        self.params.append(
                            {
                                "product": geo["product"],
                                "vintage": geo["vintage"],
                                "sumlev": geo["sumlev"],
                                "desc": geo["desc"],
                                "requires": geo.get("requires"),
                                "wildcard": geo.get("wildcard"),
                                "optionalWithWCFor": geo.get("optionalWithWCFor"),
                                "group_name": group["name"],
                                "names": self.variables[i]["names"],
                                "labels": self.variables[i]["labels"],
                                "values": self.variables[i]["values"],
                                "types": self.variables[i]["types"],
                                "attributes": self.variables[i]["attributes"],
                                "url": geo["url"],
                                "is_microdata": micro_indicators[geo["url"]],
                            }
                        )

        # Case 3: Invalid state
        else:
            print(
                "❌ Error: You must set variables (using `set_variables`) OR set exactly one group (using `set_groups`) before getting data."
            )
            return  # self.params is already empty

        if not self.params:
            print(
                "⚠️ Warning: No matching product-vintage combinations found between set geos and variables/groups."
            )
        else:
            print(
                f"✅ Parameters created for {len(self.params)} geo-variable/group combinations."
            )

    def _get_parent_geo_combinations(
        self,
        base_url: str,
        required_geos: List[str],
        current_in_clause: Dict = {},
        timeout: int = 30,
        max_workers: Optional[int] = None,
    ) -> List[Dict]:
        """
        Recursively fetches all valid combinations of parent geographies.

        For aggregate data, if a geography requires parent geos (e.g., a county
        requires a state), this method fetches all possible parent FIPS codes
        to build the necessary `in` clauses for the final data query.

        Args:
            base_url (str): The base API URL for the product.
            required_geos (List[str]): A list of parent geo levels to fetch.
            current_in_clause (Dict): The `in` clause built so far in the recursion.
            timeout (int): Request timeout in seconds.
            max_workers (int, optional): Max concurrent threads for fetching.

        Returns:
            List[Dict]: A list of dictionaries, where each dict is a valid `in` clause for a data request.

        Strategy: This is a recursive function.
        - Base Case: If there are no more required geographies to fetch, return the
          `in` clause that has been built up so far.
        - Recursive Step: Fetch all FIPS codes for the current level of geography.
          Then, for each FIPS code, make a recursive call to fetch the next level down.
        """
        if not required_geos:
            return [current_in_clause]
        level_to_fetch = required_geos[0]
        remaining_levels = required_geos[1:]
        params = {"get": "NAME", "for": f"{level_to_fetch}:*"}
        if current_in_clause:
            in_parts = []
            for k, v in current_in_clause.items():
                if isinstance(v, list):
                    in_parts.append(f"{k}:{','.join(v)}")
                else:
                    in_parts.append(f"{k}:{v}")
            params["in"] = " ".join(in_parts)
        data = self._get_json_from_url(base_url, params, timeout=timeout)
        if not data or len(data) < 2:
            return []
        try:
            fips_index = data[0].index(level_to_fetch)
        except ValueError:
            print(
                f"❌ Could not find FIPS column for '{level_to_fetch}' in API response."
            )
            return []
        all_combinations = []
        # Use a ThreadPoolExecutor to fetch combinations for the next level in parallel,
        # significantly speeding up discovery for deep geographic hierarchies.
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_fips = {
                executor.submit(
                    self._get_parent_geo_combinations,
                    base_url,
                    remaining_levels,
                    {**current_in_clause, level_to_fetch: row[fips_index]},
                    timeout=timeout,
                    max_workers=max_workers,
                ): row[fips_index]
                for row in data[1:]
            }
            for future in as_completed(future_to_fips):
                all_combinations.extend(future.result())
        return all_combinations

    def _get_gdf_from_url(
        self,
        layer_id: int,
        where_clause: str,
        service: str = "TIGERweb/tigerWMS_Current",
        timeout: int = None,
        offset: int = None,
        n_records: int = None,
        count_only: bool = False,
    ) -> Union["gpd.GeoDataFrame", int]:
        """
        Fetches geographic polygons or a feature count from the US Census TIGERweb REST API.

        Args:
            layer_id (int): The numeric ID for the desired geography layer.
            where_clause (str): An SQL-like clause to filter the geographies.
            service (str): The name of the TIGERweb map service to query.
            timeout (int, optional): Request timeout in seconds.
            offset (int, optional): The starting record offset for pagination.
            n_records (int, optional): The number of records to return per page.
            count_only (bool): If True, returns only the count of matching records.

        Returns:
            If count_only is True, returns an integer count. Otherwise, returns a GeoDataFrame with the requested geometries.
        """
        import geopandas as gpd

        API_URL = f"https://tigerweb.geo.census.gov/arcgis/rest/services/{service}/MapServer/{layer_id}/query"

        params = {
            "where": where_clause,
            "outFields": "GEOID,NAME",
            "outSR": "4326",
            "f": "geojson",
            "returnGeometry": "true" if not count_only else "false",
            "returnCountOnly": str(count_only).lower(),
            "resultOffset": offset,
            "resultRecordCount": n_records,
            "timeout": timeout,
        }
        # Filter out None values before making the request
        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = self._request_with_retry(API_URL, params=params)
            response.raise_for_status()
            json_response = response.json()

            if count_only:
                return json_response.get("count", 0)

            return gpd.GeoDataFrame.from_features(json_response["features"])

        except requests.exceptions.RequestException as e:
            print(f"❌ HTTP Request failed: {e}")
        except (KeyError, ValueError) as e:
            print(f"❌ Failed to parse response JSON: {e}")
            print(f"   Server Response: {response.text[:200]}...")

        return gpd.GeoDataFrame() if not count_only else 0

    def _get_gdf_from_url_with_status(
        self,
        layer_id: int,
        where_clause: str,
        service: str = "TIGERweb/tigerWMS_Current",
        timeout: int = None,
        offset: int = None,
        n_records: int = None,
        count_only: bool = False,
    ) -> Tuple[Union["gpd.GeoDataFrame", int], Optional[int]]:
        """
        Fetches geographic data from TIGERweb, returning status code for retry logic.

        This variant of _get_gdf_from_url returns a tuple of (result, status_code)
        to enable retry logic to distinguish between retryable server errors
        (429, 5xx) and non-retryable client errors (4xx). Connection errors
        return status_code=None, which should also be treated as retryable.

        Args:
            layer_id (int): The numeric ID for the desired geography layer.
            where_clause (str): An SQL-like clause to filter the geographies.
            service (str): The name of the TIGERweb map service to query.
            timeout (int, optional): Request timeout in seconds.
            offset (int, optional): The starting record offset for pagination.
            n_records (int, optional): The number of records to return per page.
            count_only (bool): If True, returns only the count of matching records.

        Returns:
            Tuple of (result, status_code). Result is either an int (count) or GeoDataFrame. status_code is None for connection errors.
        """
        import geopandas as gpd

        API_URL = f"https://tigerweb.geo.census.gov/arcgis/rest/services/{service}/MapServer/{layer_id}/query"

        params = {
            "where": where_clause,
            "outFields": "GEOID,NAME",
            "outSR": "4326",
            "f": "geojson",
            "returnGeometry": "true" if not count_only else "false",
            "returnCountOnly": str(count_only).lower(),
            "resultOffset": offset,
            "resultRecordCount": n_records,
            "timeout": timeout,
        }
        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = self._request_with_retry(API_URL, params=params, timeout=timeout or 30)
            status_code = response.status_code
            response.raise_for_status()
            json_response = response.json()

            if count_only:
                return json_response.get("count", 0), status_code

            return gpd.GeoDataFrame.from_features(json_response["features"]), status_code

        except requests.exceptions.RequestException as e:
            status_code = e.response.status_code if e.response is not None else None
            return (gpd.GeoDataFrame() if not count_only else 0), status_code
        except (KeyError, ValueError):
            # JSON parse error - treat as non-retryable (likely bad response format)
            return (gpd.GeoDataFrame() if not count_only else 0), 200

    def _data_fetching(
        self,
        tasks: List[Tuple[str, Dict, Dict]] = None,
        max_workers: Optional[int] = None,
        timeout: Optional[int] = None,
        auto_retry: bool = True,
        max_retries: int = 3,
        min_workers: int = 5,
    ):
        """
        Takes data API tasks and runs them in a thread pool with adaptive retry.

        When server errors (429, 5xx) are detected, this method automatically:
        1. Waits with exponential backoff
        2. Reduces worker count by 50%
        3. Retries failed requests

        Args:
            tasks: List of (url, params, context) tuples for API calls.
            max_workers: Maximum concurrent threads.
            timeout: Request timeout in seconds.
            auto_retry: If True, automatically retry on server errors.
            max_retries: Maximum retry attempts before giving up.
            min_workers: Floor for worker reduction (won't go below this).
        """
        results_aggregator = {
            i: {"schema": None, "data": []} for i in range(len(self.params))
        }

        pending_tasks = list(tasks)
        current_workers = max_workers
        retry_count = 0

        # Status codes that indicate server overload - these are retryable
        RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

        while pending_tasks:
            failed_tasks = []
            server_error_count = 0

            with ThreadPoolExecutor(max_workers=current_workers) as executor:
                future_to_task = {
                    executor.submit(
                        self._get_json_from_url_with_status, url, params, timeout
                    ): (url, params, context)
                    for url, params, context in pending_tasks
                }

                for future in as_completed(future_to_task):
                    url, params, context = future_to_task[future]
                    param_index = context["param_index"]

                    try:
                        data, status_code = future.result()

                        # Check if this is a retryable server error
                        # Also retry on connection errors (status_code is None)
                        if status_code in RETRYABLE_STATUS_CODES or status_code is None:
                            server_error_count += 1
                            failed_tasks.append((url, params, context))
                        elif data and len(data) > 1:
                            # Success - aggregate the data
                            if results_aggregator[param_index]["schema"] is None:
                                results_aggregator[param_index]["schema"] = data[0]
                            results_aggregator[param_index]["data"].extend(data[1:])
                        # else: request succeeded but returned no/empty data - that's OK

                    except Exception as exc:
                        print(f"❌ Task for {context} generated an exception: {exc}")

            # Decide whether to retry
            if failed_tasks and auto_retry and retry_count < max_retries:
                # Calculate error rate
                error_rate = server_error_count / len(pending_tasks)

                if error_rate > 0.1:  # More than 10% failed with server errors
                    retry_count += 1
                    # Reduce workers by 50%, but don't go below minimum
                    current_workers = max(min_workers, current_workers // 2)
                    # Exponential backoff
                    backoff_time = 2 ** retry_count

                    print(
                        f"⚠️ {server_error_count}/{len(pending_tasks)} requests failed with server errors. "
                        f"Retry {retry_count}/{max_retries}: reducing workers to {current_workers} "
                        f"and waiting {backoff_time}s..."
                    )
                    time.sleep(backoff_time)
                    pending_tasks = failed_tasks
                else:
                    # Low error rate - probably not a rate limiting issue
                    if server_error_count > 0:
                        print(
                            f"⚠️ {server_error_count} requests failed but error rate is low. Not retrying."
                        )
                    pending_tasks = []
            elif failed_tasks and retry_count >= max_retries:
                print(
                    f"❌ Maximum retries ({max_retries}) exceeded. "
                    f"{len(failed_tasks)} requests could not be completed."
                )
                pending_tasks = []
            else:
                pending_tasks = []

        # After all tasks are complete, attach the aggregated data to self.params
        print("✅ Data fetching complete. Stacking results.")
        for i, param in enumerate(self.params):
            aggregated_result = results_aggregator[i]
            if aggregated_result["schema"]:
                param["schema"] = aggregated_result["schema"]
                param["data"] = aggregated_result["data"]
            else:
                # Ensure 'data' key exists, even if empty, for downstream consistency.
                param["data"] = []

    def _geometry_fetching(
        self,
        tasks: List[Dict],
        max_workers: Optional[int] = None,
        timeout: Optional[int] = None,
        verbose: bool = False,
        auto_retry: bool = True,
        max_retries: int = 3,
        min_workers: int = 5,
    ):
        """
        Takes TIGERweb tasks, handles pagination, and fetches geometries in a thread pool.

        This method uses an iterative approach for pagination to avoid Python's
        recursion depth limits, which is safer for queries that could return
        many thousands of features.

        When server errors (429, 5xx) or connection errors are detected, this method
        automatically:
        1. Waits with exponential backoff
        2. Reduces worker count by 50%
        3. Retries failed requests

        Strategy:
        1. For each initial task, make a pre-flight request to get the total count
           of geometries. These requests are run concurrently.
        2. Based on the count, calculate how many paginated requests are needed.
        3. Create a list of all sub-tasks (one for each page).
        4. Execute all sub-tasks concurrently in a thread pool with retry logic.
        5. Aggregate the resulting GeoDataFrames and attach them to the corresponding
           item in `self.params`.
        """
        # This will hold all the individual page-fetching tasks
        paginated_tasks = []

        RECORDS_PER_PAGE = 1000
        RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

        if not tasks:
            return

        import pandas as pd
        import geopandas as gpd

        if verbose:
            print("ℹ️ Pre-querying for geometry counts to determine pagination...")

        # Step 1 & 2: Concurrently pre-flight requests to get counts and create paginated tasks
        # Pre-flight requests also use retry logic
        pending_preflight = list(tasks)
        current_workers = max_workers
        retry_count = 0

        while pending_preflight:
            failed_preflight = []
            server_error_count = 0

            with ThreadPoolExecutor(max_workers=current_workers) as executor:
                future_to_task = {
                    executor.submit(
                        self._get_gdf_from_url_with_status,
                        layer_id=task["layer_id"],
                        where_clause=task["where_clause"],
                        service=task["map_server"],
                        timeout=timeout,
                        count_only=True,
                    ): task
                    for task in pending_preflight
                }

                for future in as_completed(future_to_task):
                    task = future_to_task[future]
                    where_clause = task["where_clause"]
                    try:
                        total_records, status_code = future.result()

                        # Check if this is a retryable error
                        if status_code in RETRYABLE_STATUS_CODES or status_code is None:
                            server_error_count += 1
                            failed_preflight.append(task)
                            continue

                        if total_records == 0:
                            if verbose:
                                print(
                                    f"  - No geometries found for WHERE '{where_clause[:60]}...'. Skipping."
                                )
                            continue

                        if verbose:
                            print(
                                f"  - Found {total_records} geometries for WHERE '{where_clause[:60]}...'. Building paginated tasks."
                            )

                        # Step 3: Create sub-tasks for each page
                        for offset in range(0, total_records, RECORDS_PER_PAGE):
                            paginated_tasks.append(
                                {
                                    "param_index": task["param_index"],
                                    "layer_id": task["layer_id"],
                                    "where_clause": where_clause,
                                    "service": task["map_server"],
                                    "offset": offset,
                                    "n_records": RECORDS_PER_PAGE,
                                }
                            )
                    except Exception as exc:
                        print(
                            f"❌ Failed during geometry count pre-flight for {where_clause}: {exc}"
                        )

            # Decide whether to retry pre-flight
            if failed_preflight and auto_retry and retry_count < max_retries:
                error_rate = server_error_count / len(pending_preflight)
                if error_rate > 0.1:
                    retry_count += 1
                    current_workers = max(min_workers, current_workers // 2)
                    backoff_time = 2 ** retry_count
                    print(
                        f"⚠️ {server_error_count}/{len(pending_preflight)} pre-flight requests failed. "
                        f"Retry {retry_count}/{max_retries}: reducing workers to {current_workers} "
                        f"and waiting {backoff_time}s..."
                    )
                    time.sleep(backoff_time)
                    pending_preflight = failed_preflight
                else:
                    pending_preflight = []
            elif failed_preflight and retry_count >= max_retries:
                print(
                    f"❌ Maximum retries ({max_retries}) exceeded for pre-flight. "
                    f"{len(failed_preflight)} requests could not be completed."
                )
                pending_preflight = []
            else:
                pending_preflight = []

        if not paginated_tasks:
            if verbose:
                print("ℹ️ No paginated geometry tasks to execute.")
            return

        # Dictionary to aggregate GDFs for each original param
        results_aggregator = defaultdict(list)

        # Step 4: Execute all paginated tasks concurrently with retry logic
        if verbose:
            print(
                f"ℹ️ Fetching geometries across {len(paginated_tasks)} paginated calls..."
            )

        pending_tasks = list(paginated_tasks)
        current_workers = max_workers  # Reset workers for this phase
        retry_count = 0

        while pending_tasks:
            failed_tasks = []
            server_error_count = 0

            with ThreadPoolExecutor(max_workers=current_workers) as executor:
                future_to_context = {
                    executor.submit(
                        self._get_gdf_from_url_with_status,
                        layer_id=p_task["layer_id"],
                        where_clause=p_task["where_clause"],
                        service=p_task["service"],
                        timeout=timeout,
                        offset=p_task["offset"],
                        n_records=p_task["n_records"],
                    ): p_task
                    for p_task in pending_tasks
                }

                for future in as_completed(future_to_context):
                    context = future_to_context[future]
                    param_index = context["param_index"]
                    try:
                        gdf, status_code = future.result()

                        # Check if this is a retryable error
                        if status_code in RETRYABLE_STATUS_CODES or status_code is None:
                            server_error_count += 1
                            failed_tasks.append(context)
                        elif not gdf.empty:
                            results_aggregator[param_index].append(gdf)
                        # else: request succeeded but returned no data - that's OK

                    except Exception as exc:
                        print(f"❌ Geometry fetch task failed for {context}: {exc}")

            # Decide whether to retry
            if failed_tasks and auto_retry and retry_count < max_retries:
                error_rate = server_error_count / len(pending_tasks)
                if error_rate > 0.1:
                    retry_count += 1
                    current_workers = max(min_workers, current_workers // 2)
                    backoff_time = 2 ** retry_count
                    print(
                        f"⚠️ {server_error_count}/{len(pending_tasks)} geometry requests failed. "
                        f"Retry {retry_count}/{max_retries}: reducing workers to {current_workers} "
                        f"and waiting {backoff_time}s..."
                    )
                    time.sleep(backoff_time)
                    pending_tasks = failed_tasks
                else:
                    if server_error_count > 0:
                        print(
                            f"⚠️ {server_error_count} geometry requests failed but error rate is low. Not retrying."
                        )
                    pending_tasks = []
            elif failed_tasks and retry_count >= max_retries:
                print(
                    f"❌ Maximum retries ({max_retries}) exceeded for geometry fetching. "
                    f"{len(failed_tasks)} requests could not be completed."
                )
                pending_tasks = []
            else:
                pending_tasks = []

        # Step 5: Concatenate GDFs and attach to self.params
        print("✅ Geometry fetching complete. Stacking results.")
        for i, param in enumerate(self.params):
            if i in results_aggregator:
                # Concatenate all the GeoDataFrame pages into a single one
                combined_gdf = pd.concat(results_aggregator[i], ignore_index=True)
                param["geometry"] = gpd.GeoDataFrame(combined_gdf)
            else:
                param["geometry"] = gpd.GeoDataFrame()


    def get_data(
        self,
        within: Union[str, Dict, List[Dict]] = "us",
        max_workers: Optional[int] = 25,
        timeout: int = 30,
        preview_only: bool = False,
        include_names: bool = False,
        include_geoids: bool = False,
        include_attributes: bool = False,
        include_geometry: bool = False,
        in_place: bool = False,
        verbose: bool = False,
        auto_retry: bool = True,
        max_retries: int = 3,
        min_workers: int = 5,
    ) -> "CenDatResponse":
        """
        Retrieves data from the Census API based on the set parameters.

        This is the final method in the chain. It constructs and executes all
        necessary API calls in parallel, aggregates the results, and returns
        a CenDatResponse object for further processing.

        Args:
            within (Union[str, Dict, List[Dict]]): Specifies the geographic
                scope. Can be "us" (default), or a dictionary defining parent
                geographies (e.g., `{'state': '06'}` for California), or a list
                of such dictionaries for multiple scopes.
            max_workers (int, optional): The maximum number of concurrent
                threads to use for API calls. Defaults to 25.
            timeout (int): Request timeout in seconds for each API call.
                Defaults to 30.
            preview_only (bool): If True, builds the list of API calls but does
                not execute them. Useful for debugging. Defaults to False.
            auto_retry (bool): If True (default), automatically retry failed
                requests caused by server overload (429, 5xx errors) with
                reduced worker count and exponential backoff.
            max_retries (int): Maximum number of retry attempts when
                auto_retry is enabled. Defaults to 3.
            min_workers (int): Minimum number of workers to use when
                retrying. Worker count won't be reduced below this. Defaults to 5.

        Returns:
            CenDatResponse: An object containing the aggregated data from all successful API calls.

        High-level Strategy:
        1. Generate parameter sets by combining set products, geos, and variables/groups.
        2. For each parameter set, determine the necessary API calls based on the `within` clause.
        3. This involves handling microdata vs. aggregate data, and for aggregate data, determining if parent geography discovery or wildcards are needed.
        4. Build a list of all API call tasks (URL + parameters).
        5. If not in preview mode, execute all tasks concurrently using a thread pool.
        6. Aggregate the results and return them in a `CenDatResponse` object.
        """
        self._create_params()

        if not self.params:
            print(
                "❌ Error: Could not create parameters. Please set geos and variables."
            )
            return CenDatResponse([])

        if include_geometry:
            if find_spec("geopandas") is None or find_spec("pandas") is None:
                print(
                    "❌ GeoPandas and/or Pandas are not installed. Please install them with 'pip install geopandas pandas'"
                )
                return CenDatResponse([])

            include_geoids = True

            valid_sumlevs_geometry = {
                "020": ["Census Regions"],
                "030": ["Census Divisions"],
                "040": ["States"],
                "050": ["Counties"],
                "060": ["County Subdivisions"],
                "140": ["Census Tracts"],
                "150": ["Census Block Groups"],
                "160": ["Incorporated Places", "Census Designated Places"],
            }

            desc_map = {
                "region": "REGION",
                "division": "DIVISION",
                "state": "STATE",
                "county": "COUNTY",
                "county subdivision": "COUSUB",
                "tract": "TRACT",
                "block group": "BLKGRP",
                "place": "PLACE",
            }

            state_codes = {
                "WA": "53",
                "DE": "10",
                "DC": "11",
                "WI": "55",
                "WV": "54",
                "HI": "15",
                "FL": "12",
                "WY": "56",
                "PR": "72",
                "NJ": "34",
                "NM": "35",
                "TX": "48",
                "LA": "22",
                "NC": "37",
                "ND": "38",
                "NE": "31",
                "TN": "47",
                "NY": "36",
                "PA": "42",
                "AK": "02",
                "NV": "32",
                "NH": "33",
                "VA": "51",
                "CO": "08",
                "CA": "06",
                "AL": "01",
                "AR": "05",
                "VT": "50",
                "IL": "17",
                "GA": "13",
                "IN": "18",
                "IA": "19",
                "MA": "25",
                "AZ": "04",
                "ID": "16",
                "CT": "09",
                "ME": "23",
                "MD": "24",
                "OK": "40",
                "OH": "39",
                "UT": "49",
                "MO": "29",
                "MN": "27",
                "MI": "26",
                "RI": "44",
                "KS": "20",
                "MT": "30",
                "MS": "28",
                "SC": "45",
                "KY": "21",
                "OR": "41",
                "SD": "46",
            }

            url = (
                "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb?f=pjson"
            )

            map_servers = []  # Initialize to empty list
            map_servers_fetched = False

            try:
                response = self._request_with_retry(url)
                response.raise_for_status()
                map_servers = [
                    item["name"]
                    for item in response.json()["services"]
                    if re.search(r"ACS|Census|Current", item["name"])
                ]
                map_servers_fetched = True
                if verbose:
                    print("✅ Successfully fetched map servers.")

            except requests.exceptions.RequestException as e:
                print(f"❌ HTTP Request failed: {e}")

            # Helper function to correctly format TIGERweb SQL WHERE clauses,
            # handling both single values and lists of values.
            def format_sql_in_clause(key, value):
                # Map the user-facing geo name (e.g., 'state') to the TIGERweb field name (e.g., 'STATE')
                field = desc_map[key]
                if isinstance(value, list):
                    # For a list, create a comma-separated, quoted string: "'val1','val2'"
                    values_str = ",".join(f"'{item}'" for item in value)
                    return f"{field} IN ({values_str})"
                else:
                    # For a single value, just wrap it in quotes
                    return f"{field} IN ('{value}')"

        data_tasks = []
        geo_tasks = []

        raw_within_clauses = within if isinstance(within, list) else [within]
        if (
            include_geometry
            and raw_within_clauses in [[], ["us"]]
            and any(param["sumlev"] == "040" for param in self.params)
        ):
            raw_within_clauses = [{"state": list(state_codes.values())}]

        # Expand the `within` clauses. If a user provides a list of codes for a
        # geography (e.g., `{'state': '08', 'county': ['001', '005']}`), this
        # logic expands it into separate clauses for each combination.
        expanded_within_clauses = []
        for clause in raw_within_clauses:
            # Use builtins.dict to prevent shadowing errors with local variables
            if not isinstance(clause, builtins.dict):
                expanded_within_clauses.append(clause)
                continue

            # Separate keys with list values from those with single values
            list_items = {k: v for k, v in clause.items() if isinstance(v, list)}
            single_items = {k: v for k, v in clause.items() if not isinstance(v, list)}

            if not list_items:
                expanded_within_clauses.append(clause)
                continue

            # Create all combinations of the list values
            keys, values = zip(*list_items.items())
            for v_combination in itertools.product(*values):
                new_clause = single_items.copy()
                new_clause.update(builtins.dict(zip(keys, v_combination)))
                expanded_within_clauses.append(new_clause)

        # Iterate through each parameter set (a unique product/vintage/geo combination)
        # and each `within` clause to build the full list of API calls.
        for i, param in enumerate(self.params):
            product_info = next(
                (p for p in self.products if p["title"] == param["product"]), None
            )
            if not product_info:
                continue

            if include_geometry:
                skip_geometry = False
                if not map_servers_fetched:
                    skip_geometry = True
                    print("❌ Skipping geometry: could not fetch available map servers.")
                elif (
                    product_info["type"].split("/")[0] == "dec"
                    and product_info["vintage"][0] >= 2010
                ):
                    map_server = f"TIGERweb/tigerWMS_Census{product_info['vintage'][0]}"
                elif product_info["type"].split("/")[0] == "acs":
                    if (
                        product_info["vintage"][0] >= 2012
                        and product_info["vintage"][0] != 2020
                    ):
                        map_server = (
                            f"TIGERweb/tigerWMS_ACS{product_info['vintage'][0]}"
                        )
                    elif product_info["vintage"][0] >= 2012:
                        map_server = "TIGERweb/tigerWMS_Census2020"
                    else:
                        map_server = "TIGERweb/tigerWMS_Census2010"
                else:
                    map_server = "TIGERweb/tigerWMS_Current"

                if map_server not in map_servers:
                    skip_geometry = True
                    print(
                        f"❌ Error: the requested map server '{map_server}' is not available."
                    )
                if param["sumlev"] not in valid_sumlevs_geometry.keys():
                    skip_geometry = True
                    print(
                        f"❌ Error: the requested summary level ({param['sumlev']}) is currently supported for geometry."
                    )
                if not skip_geometry:
                    url = f"https://tigerweb.geo.census.gov/arcgis/rest/services/{map_server}/MapServer?f=pjson"

                    try:
                        response = self._request_with_retry(url)
                        response.raise_for_status()

                        map_server_layers = [
                            item["id"]
                            for item in response.json()["layers"]
                            if item["name"] in valid_sumlevs_geometry[param["sumlev"]]
                        ]
                        if verbose:
                            print("✅ Successfully fetched map server layers.")

                    except requests.exceptions.RequestException as e:
                        print(f"❌ HTTP Request failed: {e}")

            # Conditionally build the 'get' parameter string based on call type
            if "group_name" in param:  # This is a group-based call, not variable-based
                vars_to_get = [f"group({param['group_name']})"]
                if include_geoids and param["is_microdata"]:
                    print("ℹ️ GEO_ID not valid for microdata - request ignored.")
                elif include_geoids:
                    vars_to_get.insert(0, "GEO_ID")
                if include_names and param["is_microdata"]:
                    print("ℹ️ NAME not valid for microdata - request ignored.")
                elif include_names:
                    vars_to_get.insert(0, "NAME")
                # `include_attributes` is ignored for group calls as it's not applicable.
            else:
                vars_to_get = param["names"].copy()
                if include_geoids and param["is_microdata"]:
                    print("ℹ️ GEO_ID not valid for microdata - request ignored.")
                elif include_geoids:
                    vars_to_get.insert(0, "GEO_ID")
                if include_names and param["is_microdata"]:
                    print("ℹ️ NAME not valid for microdata - request ignored.")
                elif include_names:
                    vars_to_get.insert(0, "NAME")
                if include_attributes:
                    all_attributes = set()
                    # Iterate through the list of attribute strings for the selected variables
                    for attr_string in param.get("attributes", []):
                        # Check if the string is valid and not the "N/A" placeholder
                        if attr_string and attr_string != "N/A":
                            # The 'attributes' key contains a comma-separated string of variable names.
                            # We split this string and add the names to our set.
                            all_attributes.update(attr_string.split(","))

                    # Add the unique, valid attributes to the list of variables to request.
                    if all_attributes:
                        vars_to_get.extend(list(all_attributes))

            variable_names = ",".join(vars_to_get)
            target_geo = param["desc"]
            vintage_url = param["url"]
            context = {"param_index": i}

            for within_clause in expanded_within_clauses:
                # --- Microdata Path ---
                # Microdata requests are simpler: they require a dictionary specifying
                # the target geography and its codes, plus any parent geographies.
                if product_info.get("is_microdata"):
                    if not isinstance(within_clause, builtins.dict):
                        print(
                            "❌ Error: A `within` dictionary or list of dictionaries is required for microdata requests."
                        )
                        continue

                    if include_geometry:
                        print("ℹ️ Geometry not valid for microdata - request ignored.")

                    within_copy = within_clause.copy()
                    target_geo_codes = within_copy.pop(target_geo, None)

                    if target_geo_codes is None:
                        print(
                            f"❌ Error: `within` dictionary must contain the target geography: '{target_geo}'"
                        )
                        continue

                    codes_str = (
                        target_geo_codes
                        if isinstance(target_geo_codes, str)
                        else ",".join(target_geo_codes)
                    )

                    api_params = {
                        "get": variable_names,
                        "for": f"{target_geo}:{codes_str}",
                    }
                    if within_copy:
                        api_params["in"] = " ".join(
                            [f"{k}:{v}" for k, v in within_copy.items()]
                        )
                    data_tasks.append((vintage_url, api_params, context))

                # --- Aggregate Data Path ---
                # This path is more complex as it needs to handle geographic hierarchies.
                elif product_info.get("is_aggregate"):
                    required_geos = param.get("requires") or []
                    provided_parent_geos = {}
                    target_geo_codes = None
                    # If `within` is a dictionary, parse out the target geography codes
                    # and any provided parent geographies.
                    if isinstance(within_clause, builtins.dict):
                        within_copy = within_clause.copy()
                        target_geo_codes = within_copy.pop(target_geo, None)
                        provided_parent_geos = {
                            k: v for k, v in within_copy.items() if k in required_geos
                        }

                    # Case A: The target geography itself is specified in `within`.
                    # No discovery or wildcards needed; we can build the call directly.
                    if target_geo_codes:
                        codes_str = (
                            target_geo_codes
                            if isinstance(target_geo_codes, str)
                            else ",".join(map(str, target_geo_codes))
                        )
                        api_params = {
                            "get": variable_names,
                            "for": f"{target_geo}:{codes_str}",
                        }
                        if provided_parent_geos:
                            api_params["in"] = " ".join(
                                [f"{k}:{v}" for k, v in provided_parent_geos.items()]
                            )
                        data_tasks.append((vintage_url, api_params, context))
                        if include_geometry and not skip_geometry:
                            geo_params = [
                                {
                                    "param_index": i,
                                    "map_server": map_server,
                                    "layer_id": map_server_layer,
                                    "where_clause": " AND ".join(
                                        [
                                            format_sql_in_clause(k, v)
                                            for k, v in within_clause.items()
                                        ]
                                    ),
                                }
                                for map_server_layer in map_server_layers
                            ]
                            geo_tasks.extend(geo_params)
                        continue

                    # Case B: Target geography is not specified. We need to figure out
                    # the `for` and `in` clauses using wildcards or discovery.
                    # `final_in_clause` will store the components of the `in` parameter.
                    # A value of `None` indicates a level that needs discovery.
                    final_in_clause = {}
                    if include_geometry:
                        param.pop("optionalWithWCFor", None)
                        if "wildcard" in param and isinstance(param["wildcard"], list):
                            param["wildcard"] = param["wildcard"][1:]
                    if required_geos:
                        for geo in required_geos:
                            if geo in provided_parent_geos:
                                final_in_clause[geo] = provided_parent_geos[geo]
                            elif param.get("wildcard") and geo in param["wildcard"]:
                                final_in_clause[geo] = "*"
                            else:
                                final_in_clause[geo] = None  # Needs discovery

                    # Some geographies have an optional parent for wildcards.
                    # If that optional parent isn't provided, we should not include it
                    # in the `in` clause at all.

                    optional_level = param.get("optionalWithWCFor")
                    if optional_level and optional_level not in provided_parent_geos:
                        final_in_clause.pop(optional_level, None)

                    geos_to_fetch = [
                        geo for geo, code in final_in_clause.items() if code is None
                    ]

                    # If there are levels that need discovery, call the recursive helper.
                    combinations = []
                    if geos_to_fetch:
                        if verbose:
                            print(
                                f"ℹ️ Discovering parent geographies for: {geos_to_fetch}"
                            )
                        resolved_parents = {
                            k: v
                            for k, v in final_in_clause.items()
                            if v is not None and v != "*"
                        }
                        combinations = self._get_parent_geo_combinations(
                            vintage_url,
                            geos_to_fetch,
                            resolved_parents,
                            timeout=timeout,
                            max_workers=max_workers,
                        )
                    else:
                        combinations = [final_in_clause]

                    if combinations and verbose:
                        print(
                            f"✅ Found {len(combinations)} combinations. Building API queries..."
                        )

                    # Build an API task for each discovered parent geography combination.
                    for combo in combinations:
                        call_in_clause = final_in_clause.copy()
                        call_in_clause.update(combo)
                        call_in_clause = {
                            k: v for k, v in call_in_clause.items() if v is not None
                        }

                        api_params = {"get": variable_names, "for": f"{target_geo}:*"}
                        if call_in_clause:
                            api_params["in"] = " ".join(
                                [f"{k}:{v}" for k, v in call_in_clause.items()]
                            )
                        data_tasks.append((vintage_url, api_params, context))

                        # Corrected logic for geometry task creation
                        if include_geometry and not skip_geometry:
                            # Build the WHERE clause conditions from the call_in_clause dictionary.
                            where_conditions = [
                                format_sql_in_clause(k, v)
                                for k, v in call_in_clause.items()
                                if v != "*"
                            ]

                            # If there are no conditions (e.g., a nationwide query for "us"),
                            # use '1=1' as a universal "select all" filter. Otherwise, join them.
                            final_where_clause = (
                                " AND ".join(where_conditions)
                                if where_conditions
                                else "1=1"
                            )

                            geo_params = [
                                {
                                    "param_index": i,
                                    "map_server": map_server,
                                    "layer_id": map_server_layer,
                                    "where_clause": final_where_clause,
                                }
                                for map_server_layer in map_server_layers
                            ]
                            geo_tasks.extend(geo_params)

        if not data_tasks:
            print("❌ Error: Could not determine any API calls to make.")
            return CenDatResponse([])

        self.n_calls = len(data_tasks)

        # If in preview mode, print the first few planned calls and exit.
        if preview_only:
            print(f"ℹ️ Preview: this will yield {self.n_calls} API call(s).")
            for i, (url, params, _) in enumerate(data_tasks[:5]):
                print(
                    f"  - Call {i+1}: {url}?get={params.get('get')}&for={params.get('for')}&in={params.get('in','')}"
                )
            if len(data_tasks) > 5:
                print(f"  ... and {len(data_tasks) - 5} more.")
            return CenDatResponse([])

        else:
            if verbose:
                print(f"ℹ️ Making {self.n_calls} API call(s)...")
            # Execute all API calls concurrently.
            try:
                with ThreadPoolExecutor(max_workers=2) as executor:
                    # Submit the two master jobs for data and geometry fetching.
                    future_geo = executor.submit(
                        self._geometry_fetching,
                        geo_tasks,
                        max_workers,
                        timeout,
                        verbose,
                        auto_retry,
                        max_retries,
                        min_workers,
                    )
                    future_data = executor.submit(
                        self._data_fetching,
                        data_tasks,
                        max_workers,
                        timeout,
                        auto_retry,
                        max_retries,
                        min_workers,
                    )

                    # Wait for both futures to complete. The .result() call will
                    # re-raise any exceptions that occurred in the thread.
                    future_data.result()
                    future_geo.result()

            except Exception as exc:
                print(f"❌ A master fetching task failed: {exc}")
                # Return an empty response if a master task fails
                return CenDatResponse([])

            if in_place is False:
                params_copy = copy.deepcopy(self.params)
                self.params = []
                return CenDatResponse(params_copy)

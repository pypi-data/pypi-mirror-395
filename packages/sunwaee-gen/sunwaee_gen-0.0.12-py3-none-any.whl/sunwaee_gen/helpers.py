# standard
# third party
# custom


# NOTE this has been AI generated
def get_nested_dict_value(data: dict | list, path: str, sep: str = "."):
    """
    Get nested dictionary value with support for array filtering.

    Supports patterns like:
    - "content.[type=thinking].thinking" - filter content array for type=thinking, get thinking field
    - "content.[type=text].text" - filter content array for type=text, get text field
    - "content.[type=tool_use]" - filter content array for type=tool_use items
    - "parts.[functionCall].name" - filter parts array for items with functionCall key, get name field
    - "a.[b].b.[c].c" - filter array 'a' for items with key 'b', get field 'b', filter for items with key 'c', get field 'c'
    - "data.[status=active].items.[category=tech].name" - multiple chained filters with conditions
    - Regular paths like "choices.0.message.content" still work

    Returns:
    - Single value if only one result found
    - List of values if multiple results found
    - None if no results found or path is invalid
    """

    def _parse_filter_pattern(filter_pattern: str) -> tuple[str, str | None]:
        """Parse filter pattern to extract key and optional value."""
        if "=" in filter_pattern:
            filter_key, filter_value = filter_pattern.split("=", 1)
            return filter_key, filter_value
        return filter_pattern, None

    def _apply_array_filter(
        items: list, filter_key: str, filter_value: str | None
    ) -> list:
        """Apply filter to array items based on key and optional value."""
        filtered_items = []
        for item in items:
            if not isinstance(item, dict):  # pragma: no cover
                continue

            if filter_value is not None:
                # Filter condition: key=value
                if item.get(filter_key) == filter_value:
                    filtered_items.append(item)
            else:
                # Filter condition: key exists (any non-null value)
                if filter_key in item and item[filter_key] is not None:
                    filtered_items.append(item)

        return filtered_items

    def _extract_field_values(items: list, field_key: str) -> list:
        """Extract field values from a list of dictionary items."""
        field_values = []
        for item in items:
            if isinstance(item, dict) and field_key in item:
                field_values.append(item[field_key])
        return field_values

    def _handle_array_filtering(current: list, key: str, keys: list, i: int) -> tuple:
        """Handle array filtering logic and return new current value and index."""
        # Parse the filter pattern
        base_key, filter_pattern = key.split("[", 1)
        filter_pattern = filter_pattern.rstrip("]")

        filter_key, filter_value = _parse_filter_pattern(filter_pattern)
        filtered_items = _apply_array_filter(current, filter_key, filter_value)

        # If we have more keys to process, get the next field from each item
        if i + 1 < len(keys):
            next_key = keys[i + 1]
            field_values = _extract_field_values(filtered_items, next_key)
            return field_values, i + 2  # Skip the next key since we processed it
        else:
            # Just return the filtered items
            return filtered_items if filtered_items else None, len(keys)

    def _normalize_result(result):
        """Normalize the final result - return single item if list has one element."""
        if isinstance(result, list):
            if len(result) == 1:
                return result[0]
            elif len(result) == 0:  # pragma: no cover
                return None
        return result

    # Main processing logic
    keys = path.split(sep)
    current = data
    i = 0

    while i < len(keys):
        if current is None:
            return None

        key = keys[i]

        # Check for array filtering pattern: [key=value] or [key]
        if isinstance(current, list) and "[" in key and "]" in key:
            current, i = _handle_array_filtering(current, key, keys, i)
            if i >= len(keys):  # Early return from array filtering
                return _normalize_result(current)
        elif isinstance(current, dict):
            current = current.get(key)
            i += 1
        elif isinstance(current, list):
            try:
                current = current[int(key)]
            except (ValueError, IndexError):
                current = None
            i += 1
        else:
            current = None
            i += 1

    return _normalize_result(current)

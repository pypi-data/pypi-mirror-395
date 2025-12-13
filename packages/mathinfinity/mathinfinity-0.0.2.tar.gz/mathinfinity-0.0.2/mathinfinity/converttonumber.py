def converttonumber(value):
    try:
        value_str = str(value).strip()
        return float(value_str) if "." in value_str else int(value_str)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid numeric input: '{value}'")
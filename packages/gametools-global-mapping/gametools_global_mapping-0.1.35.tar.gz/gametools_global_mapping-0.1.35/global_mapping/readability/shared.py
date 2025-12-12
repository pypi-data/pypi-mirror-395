def format_percentage_value(
    value: int | float, format_value: bool = True
) -> str | int | float:
    if format_value:
        return f"{value}%"
    else:
        return value

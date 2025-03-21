from django import template

register = template.Library()


@register.filter
def decimal_to_american(decimal_odds):
    """Convert decimal odds to American odds and round to nearest integer, with a plus sign for positive values."""
    if decimal_odds > 2:
        result = (decimal_odds - 1) * 100
    else:
        result = -100 / (decimal_odds - 1)

    # Round the result and add a plus sign for positive values
    return f"+{round(result)}" if result > 0 else str(round(result))

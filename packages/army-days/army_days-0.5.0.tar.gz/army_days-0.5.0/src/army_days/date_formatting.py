from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from dateutil.relativedelta import relativedelta

from .models import DisplayFormat


@dataclass
class TimeComponents:
    """Calendar-accurate time components"""

    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0
    is_butt: bool = False
    is_negative: bool = False


def calculate_time_components(start_date: datetime, end_date: datetime, is_butt: bool = False) -> TimeComponents:
    """
    Calculate calendar-accurate time components using relativedelta.

    Args:
        start_date: The starting date (typically current date)
        end_date: The ending date (event date)
        is_butt: Whether the "and a butt" flag is set

    Returns:
        TimeComponents with calendar-accurate years, months, weeks, days
    """
    is_negative = end_date < start_date
    if is_negative:
        start_date, end_date = end_date, start_date

    # Use relativedelta for accurate month/year calculations
    delta = relativedelta(end_date, start_date)

    # For weeks calculation, we need to get total remaining days after months
    # relativedelta gives us remaining days in the last partial month
    # We need to calculate weeks from these remaining days
    remaining_days = delta.days
    weeks = remaining_days // 7
    days = remaining_days % 7

    return TimeComponents(
        years=delta.years, months=delta.months, weeks=weeks, days=days, is_butt=is_butt, is_negative=is_negative
    )


def determine_auto_format(total_days: float) -> DisplayFormat:
    """
    Intelligently choose display format based on magnitude.

    Thresholds:
    - < 14 days: "days"
    - < 90 days: "weeks"
    - < 730 days (2 years): "months"
    - >= 730 days: "years"

    Args:
        total_days: The number of days (can be negative for past events)

    Returns:
        The appropriate DisplayFormat
    """
    abs_days = abs(total_days)
    if abs_days < 14:
        return "days"
    elif abs_days < 90:
        return "weeks"
    elif abs_days < 730:
        return "months"
    else:
        return "years"


def _pluralize(count: int, singular: str) -> str:
    """Helper to handle singular/plural forms"""
    if count == 1:
        return f"{count} {singular}"
    return f"{count} {singular}s"


def format_time_string(
    components: TimeComponents, format_type: DisplayFormat, direction: Literal["until", "since", "today"]
) -> str:
    """
    Format time components into display string.

    Examples:
    - Days: "64 and a butt days until"
    - Weeks: "9 weeks, 1 day, and a butt until"
    - Months: "2 months, 3 weeks until"
    - Years: "1 year, 5 months until"
    - Today: "Today is"

    Args:
        components: TimeComponents with time breakdown
        format_type: How to format (days/weeks/months/years)
        direction: "until", "since", or "today"

    Returns:
        Formatted time string
    """
    if direction == "today":
        return "Today is"

    parts = []

    if format_type == "days":
        # Convert everything to days for display
        total_days = (
            components.years * 365 + components.months * 30 + components.weeks * 7 + components.days
        )  # Approximate for display purposes
        if components.is_butt:
            # Format as "X and a butt days"
            day_word = "day" if total_days == 1 else "days"
            result = f"{total_days} and a butt {day_word} {direction}"
            return result
        else:
            parts = [_pluralize(total_days, "day")]

    elif format_type == "weeks":
        # Show weeks and remaining days
        if components.weeks > 0:
            parts.append(_pluralize(components.weeks, "week"))
        if components.days > 0:
            parts.append(_pluralize(components.days, "day"))
        if not parts:  # Handle 0 weeks, 0 days case
            parts.append("0 days")
        if components.is_butt:
            parts.append("and a butt")

    elif format_type == "months":
        # Show total months (years converted to months) and remaining weeks
        total_months = components.years * 12 + components.months
        if total_months > 0:
            parts.append(_pluralize(total_months, "month"))
        if components.weeks > 0:
            parts.append(_pluralize(components.weeks, "week"))
        if not parts:  # Handle 0 months, 0 weeks case
            parts.append("0 weeks")
        if components.is_butt:
            parts.append("and a butt")

    elif format_type == "years":
        # Show years and remaining months
        if components.years > 0:
            parts.append(_pluralize(components.years, "year"))
        if components.months > 0:
            parts.append(_pluralize(components.months, "month"))
        if not parts:  # Handle 0 years, 0 months case
            parts.append("0 months")
        if components.is_butt:
            parts.append("and a butt")

    # Join parts and add direction
    result = ", ".join(parts)
    result += f" {direction}"

    return result

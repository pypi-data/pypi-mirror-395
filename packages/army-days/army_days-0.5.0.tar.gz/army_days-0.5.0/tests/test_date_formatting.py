from datetime import datetime

from freezegun import freeze_time

from army_days.date_formatting import (
    TimeComponents,
    calculate_time_components,
    determine_auto_format,
    format_time_string,
)


@freeze_time("2024-08-05T13:00:00")
def test_calculate_time_components_weeks():
    """Test week calculation using relativedelta (returns months + remaining days)"""
    start = datetime(2024, 8, 5)
    end = datetime(2024, 10, 8)  # 64 days later (2 months, 3 days)

    components = calculate_time_components(start, end, is_butt=False)
    # relativedelta gives us 2 months and 3 days remaining
    assert components.months == 2
    assert components.weeks == 0  # 3 days = 0 weeks
    assert components.days == 3
    assert components.years == 0
    assert components.is_butt is False
    assert components.is_negative is False


@freeze_time("2024-08-05T13:00:00")
def test_calculate_time_components_months():
    """Test month calculation"""
    start = datetime(2024, 8, 5)
    end = datetime(2024, 11, 5)  # 3 months later

    components = calculate_time_components(start, end, is_butt=False)
    assert components.months == 3
    assert components.years == 0


@freeze_time("2024-01-31T13:00:00")
def test_calculate_time_components_leap_year():
    """Test month calculation handles leap years correctly"""
    start = datetime(2024, 1, 31)  # Leap year
    end = datetime(2024, 2, 29)  # Valid in leap year

    components = calculate_time_components(start, end, is_butt=False)
    # relativedelta from Jan 31 to Feb 29 = 1 month, 0 days
    # (Jan 31 + 1 month = Feb 29, last day of February in leap year)
    assert components.months == 1
    assert components.weeks == 0
    assert components.days == 0


@freeze_time("2024-08-05T13:00:00")
def test_calculate_time_components_negative():
    """Test past events (negative time delta)"""
    start = datetime(2024, 8, 5)
    end = datetime(2024, 7, 1)  # 35 days ago (1 month, 4 days)

    components = calculate_time_components(start, end, is_butt=False)
    # relativedelta gives us 1 month, 4 days
    assert components.months == 1
    assert components.weeks == 0  # 4 days = 0 weeks
    assert components.days == 4
    assert components.is_negative is True


@freeze_time("2024-08-05T13:00:00")
def test_calculate_time_components_with_butt():
    """Test that is_butt flag is preserved"""
    start = datetime(2024, 8, 5)
    end = datetime(2024, 10, 8)

    components = calculate_time_components(start, end, is_butt=True)
    assert components.is_butt is True


def test_determine_auto_format_days():
    """Test auto format selection for days (<14 days)"""
    assert determine_auto_format(5) == "days"
    assert determine_auto_format(13) == "days"
    assert determine_auto_format(-5) == "days"


def test_determine_auto_format_weeks():
    """Test auto format selection for weeks (14-89 days)"""
    assert determine_auto_format(14) == "weeks"
    assert determine_auto_format(30) == "weeks"
    assert determine_auto_format(89) == "weeks"
    assert determine_auto_format(-30) == "weeks"


def test_determine_auto_format_months():
    """Test auto format selection for months (90-729 days)"""
    assert determine_auto_format(90) == "months"
    assert determine_auto_format(200) == "months"
    assert determine_auto_format(729) == "months"
    assert determine_auto_format(-200) == "months"


def test_determine_auto_format_years():
    """Test auto format selection for years (>=730 days)"""
    assert determine_auto_format(730) == "years"
    assert determine_auto_format(800) == "years"
    assert determine_auto_format(1500) == "years"
    assert determine_auto_format(-800) == "years"


def test_format_time_string_today():
    """Test formatting for today (zero days)"""
    components = TimeComponents()
    result = format_time_string(components, "days", "today")
    assert result == "Today is"


def test_format_time_string_days_singular():
    """Test formatting for singular day"""
    components = TimeComponents(days=1)
    result = format_time_string(components, "days", "until")
    assert result == "1 day until"


def test_format_time_string_days_plural():
    """Test formatting for multiple days"""
    components = TimeComponents(weeks=9, days=1)  # 64 days total
    result = format_time_string(components, "days", "until")
    assert result == "64 days until"


def test_format_time_string_days_with_butt():
    """Test formatting for days with 'and a butt'"""
    components = TimeComponents(weeks=9, days=1, is_butt=True)
    result = format_time_string(components, "days", "until")
    assert result == "64 and a butt days until"


def test_format_time_string_weeks_no_butt():
    """Test formatting for weeks without 'and a butt'"""
    components = TimeComponents(weeks=9, days=1)
    result = format_time_string(components, "weeks", "until")
    assert result == "9 weeks, 1 day until"


def test_format_time_string_weeks_with_butt():
    """Test formatting for weeks with 'and a butt'"""
    components = TimeComponents(weeks=9, days=1, is_butt=True)
    result = format_time_string(components, "weeks", "until")
    assert result == "9 weeks, 1 day, and a butt until"


def test_format_time_string_weeks_only():
    """Test formatting for exact weeks (no remaining days)"""
    components = TimeComponents(weeks=5, days=0)
    result = format_time_string(components, "weeks", "until")
    # When there are no days, we only show weeks
    assert result == "5 weeks until"


def test_format_time_string_weeks_singular():
    """Test formatting for singular week"""
    components = TimeComponents(weeks=1, days=2)
    result = format_time_string(components, "weeks", "until")
    assert result == "1 week, 2 days until"


def test_format_time_string_months():
    """Test formatting for months"""
    components = TimeComponents(months=2, weeks=3)
    result = format_time_string(components, "months", "until")
    assert result == "2 months, 3 weeks until"


def test_format_time_string_months_with_butt():
    """Test formatting for months with 'and a butt'"""
    components = TimeComponents(months=2, weeks=3, is_butt=True)
    result = format_time_string(components, "months", "until")
    assert result == "2 months, 3 weeks, and a butt until"


def test_format_time_string_months_singular():
    """Test formatting for singular month"""
    components = TimeComponents(months=1, weeks=2)
    result = format_time_string(components, "months", "until")
    assert result == "1 month, 2 weeks until"


def test_format_time_string_months_with_years():
    """Test that months format converts years to total months"""
    # 1 year, 5 months = 17 months total
    components = TimeComponents(years=1, months=5, weeks=2)
    result = format_time_string(components, "months", "until")
    assert result == "17 months, 2 weeks until"


def test_format_time_string_months_multiple_years():
    """Test that months format handles multiple years correctly"""
    # 2 years, 3 months = 27 months total
    components = TimeComponents(years=2, months=3, weeks=1)
    result = format_time_string(components, "months", "until")
    assert result == "27 months, 1 week until"


def test_format_time_string_years():
    """Test formatting for years"""
    components = TimeComponents(years=1, months=5)
    result = format_time_string(components, "years", "until")
    assert result == "1 year, 5 months until"


def test_format_time_string_years_with_butt():
    """Test formatting for years with 'and a butt'"""
    components = TimeComponents(years=1, months=5, is_butt=True)
    result = format_time_string(components, "years", "until")
    assert result == "1 year, 5 months, and a butt until"


def test_format_time_string_years_plural():
    """Test formatting for multiple years"""
    components = TimeComponents(years=3, months=2)
    result = format_time_string(components, "years", "until")
    assert result == "3 years, 2 months until"


def test_format_time_string_since():
    """Test formatting for past events (since)"""
    components = TimeComponents(weeks=5, days=0, is_negative=True)
    result = format_time_string(components, "weeks", "since")
    # When there are no days, we only show weeks
    assert result == "5 weeks since"


def test_format_time_string_zero_components():
    """Test formatting when all components are zero"""
    components = TimeComponents()
    result = format_time_string(components, "days", "until")
    assert result == "0 days until"

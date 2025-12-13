import contextlib
import io
import json

from freezegun import freeze_time

from army_days.core import compute_results
from army_days.output import _output_color_events, _output_json_events


@freeze_time("2024-08-05T13:00:00")
def test_output_color_events(standard_test_config):
    standard_test_config.config.show_completed = True
    results = compute_results(standard_test_config)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            _output_color_events(results)
        output_data = buf.getvalue()
    lines = output_data.split("\n")
    assert len(lines) == 8  # 8 lines of output including final \n
    assert "840 days since" in lines[1]
    assert "1 day since" in lines[2]
    assert "Today is " in lines[3]
    assert "1 day until" in lines[4]
    assert "129 days until" in lines[5]
    # testing army butt days
    standard_test_config.config.show_completed = True
    standard_test_config.config.use_army_butt_days = True
    results = compute_results(standard_test_config)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            _output_color_events(results)
        output_data = buf.getvalue()
    lines = output_data.split("\n")
    assert len(lines) == 8  # 8 lines of output including final \n
    assert "840 days since" in lines[1]
    assert "1 day since" in lines[2]
    assert "Today is " in lines[3]
    assert "0 and a butt days until" in lines[4]
    assert "128 and a butt days until" in lines[5]


@freeze_time("2024-08-05T13:00:00")
def test_output_json_events(standard_test_config):
    results = compute_results(standard_test_config)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            _output_json_events(results)
        output_data = buf.getvalue()
    assert output_data is not None
    data = json.loads(output_data)  # check that it's valid json
    assert data != {}
    assert data[0]["days"] == 0.0


@freeze_time("2024-08-05T13:00:00")
def test_output_weeks_format(standard_test_config):
    """Test weeks format output: 129 days = 18 weeks, 3 days"""
    standard_test_config.config.default_display_format = "weeks"
    results = compute_results(standard_test_config)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            _output_color_events(results)
        output_data = buf.getvalue()
    # Item 1 is 129 days away = 18 weeks, 3 days
    assert "18 weeks, 3 days until" in output_data


@freeze_time("2024-08-05T13:00:00")
def test_output_weeks_with_butt(standard_test_config):
    """Test weeks format with 'and a butt'"""
    standard_test_config.config.default_display_format = "weeks"
    standard_test_config.config.use_army_butt_days = True
    results = compute_results(standard_test_config)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            _output_color_events(results)
        output_data = buf.getvalue()
    # Should have "and a butt" in the output for future events after noon
    assert "and a butt until" in output_data


@freeze_time("2024-08-05T13:00:00")
def test_output_months_format(standard_test_config):
    """Test months format output"""
    standard_test_config.config.default_display_format = "months"
    results = compute_results(standard_test_config)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            _output_color_events(results)
        output_data = buf.getvalue()
    # Item 1 is 129 days away (Aug 5 to Dec 12) = 4 months, 1 week
    assert "4 months, 1 week until" in output_data


@freeze_time("2024-08-05T13:00:00")
def test_output_years_format(standard_test_config):
    """Test years format output for far future events"""
    # Use Item 5 which is 2030-01-01 (far future)
    standard_test_config.config.default_display_format = "years"
    results = compute_results(standard_test_config)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            _output_color_events(results)
        output_data = buf.getvalue()
    # Item 5 should be displayed in years format
    # 2024-08-05 to 2030-01-01 = 5 years, 4 months, 27 days -> 5 years, 4 months
    assert "5 years, 4 months until" in output_data


@freeze_time("2024-08-05T13:00:00")
def test_output_mixed_formats(standard_test_config):
    """Test that per-event format overrides work in output"""
    # Set global default to days
    standard_test_config.config.default_display_format = "days"
    # Override Item 1 to use weeks
    standard_test_config.entries[0].display_format = "weeks"

    results = compute_results(standard_test_config)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            _output_color_events(results)
        output_data = buf.getvalue()

    # Item 1 should be in weeks format
    assert "18 weeks, 3 days until" in output_data
    # Other items should be in days format
    assert "0 days until" in output_data or "Today is" in output_data


@freeze_time("2024-08-05T13:00:00")
def test_output_auto_format(standard_test_config):
    """Test that auto format resolution works in output"""
    standard_test_config.config.default_display_format = "auto"
    results = compute_results(standard_test_config)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            _output_color_events(results)
        output_data = buf.getvalue()

    # Item 2 (today, 0 days) should use days format
    assert "Today is" in output_data
    # Item 1 (129 days) should use months format (auto selects months for 90-729 days)
    assert "4 months, 1 week until" in output_data

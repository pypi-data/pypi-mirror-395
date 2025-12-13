import json
import sys
from datetime import datetime

from .ansi_text import (
    RESET,
    UNDERLINE,
    rgb_background,
    rgb_foreground,
)
from .date_formatting import calculate_time_components, format_time_string
from .models import ComputedEventModel

BG_BLACK = rgb_background(0, 0, 0)
BG_DARK_GRAY = rgb_background(30, 30, 30)
FG_YELLOW = rgb_foreground(255, 255, 0)

HEADING = " Days"


def _output_json_events(events: list[ComputedEventModel]):
    print(json.dumps([json.loads(event.model_dump_json()) for event in events]))


def _output_color_events(events: list[ComputedEventModel]):
    lines = []
    longest_line = HEADING

    # Get current date for calculations
    now = datetime.now()
    current = datetime(now.year, now.month, now.day)

    for event in events:
        # Determine direction
        if event.days == 0:
            direction = "today"
        elif event.days > 0:
            direction = "until"
        else:
            direction = "since"

        # Calculate components based on format type
        event_date = datetime(event.date.year, event.date.month, event.date.day)
        is_butt = (event.days % 1 == 0.5)

        # For days and weeks formats, use simple day arithmetic
        # For months and years, use calendar-accurate relativedelta
        if event.display_format_resolved in ("days", "weeks"):
            # Use simple day count
            total_days = int(abs(event.days))
            weeks = total_days // 7
            days = total_days % 7

            from .date_formatting import TimeComponents

            components = TimeComponents(
                years=0, months=0, weeks=weeks, days=days, is_butt=is_butt, is_negative=(event.days < 0)
            )
        else:
            # Use calendar-accurate calculation for months/years
            components = calculate_time_components(start_date=current, end_date=event_date, is_butt=is_butt)

        # Format using resolved format
        time_string = format_time_string(
            components=components, format_type=event.display_format_resolved, direction=direction
        )

        line = f"{time_string} {event.title}."
        if len(line) > len(longest_line):
            longest_line = line
        lines.append(line)

    max_len = len(longest_line)
    sys.stdout.write(f"{FG_YELLOW}{UNDERLINE}{HEADING:<{max_len}}{RESET}\n")
    for i, line in enumerate(lines):
        bg = BG_BLACK if i % 2 != 0 else BG_DARK_GRAY
        sys.stdout.write(f"{bg}{line:<{max_len}}{RESET}")
        sys.stdout.write("\n")


def output_events(events: list[ComputedEventModel]):
    if sys.stdout.isatty():
        _output_color_events(events)
    else:
        _output_json_events(events)

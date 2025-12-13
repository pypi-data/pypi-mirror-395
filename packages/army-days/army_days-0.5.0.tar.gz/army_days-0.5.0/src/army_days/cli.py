import os
import sys

import click
import yaml
import yaml.scanner
from pydantic_core import ValidationError

from .config import DEFAULT_CONFIG_FILES
from .core import compute_results, generate_default_configuration
from .models import DaysModel
from .output import output_events
from .utils import find_default_config_file


@click.command()
@click.version_option()
@click.option(
    "-f",
    "--filename",
    type=click.Path(),
    default="",
    help=f"configuration file; by default searches: {"\n".join(DEFAULT_CONFIG_FILES)}.",
)
@click.option(
    "-g",
    "--generate-sample",
    is_flag=True,
    show_default=True,
    default=False,
    help="generate sample data in yaml format (sends to stdout).",
)
@click.option(
    "-p",
    "--show-past",
    type=int,
    is_flag=False,
    flag_value=0,
    default=None,
    help="show past events; optionally limit to events within the past X days (e.g., --show-past or --show-past 365).",
)
@click.option(
    "-a",
    "--show-all",
    is_flag=True,
    show_default=True,
    default=False,
    help="show all future events, bypassing max_days_future config limit.",
)
def main(filename, generate_sample, show_past, show_all):
    if generate_sample:
        print(yaml.dump(generate_default_configuration().model_dump(mode="json")))
    else:
        config_filename = filename or find_default_config_file()
        if not config_filename or not os.path.exists(config_filename):
            sys.stderr.write(f"\nConfiguration file: '{config_filename}' not found.\n")
            sys.exit(1)
        with open(config_filename) as file:
            try:
                data = DaysModel(**yaml.load(file.read().replace("\t", " "), yaml.SafeLoader))
            except (yaml.scanner.ScannerError, yaml.error.YAMLError, ValidationError) as ex:
                sys.stderr.write(f"\nError parsing configuration file: {file.name} error: {ex}\n")
                sys.exit(1)
            output_events(compute_results(data, show_past_days=show_past, show_all_future=show_all))

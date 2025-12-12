from . import config as c
import click
import shutil
import tomllib
import tomli_w
from datetime import datetime
import os
import subprocess
import ast


def check_odoo_version():
    """
    Checks current branch in universe setup to make sure profiler is compatible
    """
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=os.path.join(get_config_option("UNIVERSE_PATH"), "odoo"),
            text=True,
            check=True,
            capture_output=True,
        )
        odoo_version = result.stdout.strip()

    except Exception as e:
        raise LookupError(f"Fatal: Could not detect Odoo version: \n{e}")

    if odoo_version not in c.INJECT_PATHS:
        raise NotImplementedError(
            f"Fatal: Odoo version {odoo_version} is not supported. Supported versions:\n{list(c.INJECT_PATHS.keys())}"
        )

    set_config_option("ODOO_VERSION", odoo_version)


def convert(raw_size: int, units):
    # Convert bytes from profile to desired unit
    unit_map = {
        "gb": 1000000000,
        "mb": 1000000,
        "kb": 1000,
    }

    # Default to mb if an unsupported unit is provided
    return round(raw_size / unit_map.get(units, unit_map["mb"]), c.DECIMAL_PLACES)


def group_by(data, dimension, metric):
    grouped = {}

    for d in data:
        grouped[d[dimension]] = grouped.get(d[dimension], 0) + d[metric]

    return grouped


def validate_config():
    if not os.path.exists(c.CONFIG_PATH):
        click.echo("No config found")
        click.echo(f"Creating config at {c.CONFIG_PATH}")

        try:
            shutil.copy(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "odoo_deets.toml"
                ),
                c.CONFIG_PATH,
            )
        except Exception as e:
            print(f"Could not create config. Permissions issue?\n{e}")
            return

    # Check that an odoo src path and venvs path has been added

    with open(c.CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)

    # TODO: DRY this up hehe
    if not config["UNIVERSE_PATH"]:
        click.echo("No Odoo universe path configured!")

        src_path = None
        while not src_path:
            src_path = click.prompt(
                "Enter your universe src/ path (parent of /odoo/ and /enterprise/)",
                type=str,
            )

            # Validate if the path is valid

            # Expand home dir if ~
            if src_path[0] == "~":
                src_path = os.path.join(c.HOME, src_path[2:])

            if not os.path.exists(src_path):
                src_path = None
                click.echo("Invalid filepath!")

        set_config_option("UNIVERSE_PATH", src_path)

    if not config["VENVS_PATH"]:
        click.echo("No Universe VENVS path configured!")

        src_path = None
        while not src_path:
            src_path = click.prompt(
                "Enter your universe venvs/ path (parent of 18.0/, saas-18.3/ etc...)",
                type=str,
            )

            # Validate if the path is valid

            # Expand home dir if ~
            if src_path[0] == "~":
                src_path = os.path.join(c.HOME, src_path[2:])

            if not os.path.exists(src_path):
                src_path = None
                click.echo("Invalid filepath!")

        set_config_option("VENVS_PATH", src_path)


def set_config_option(key: str, val: any):
    with open(c.CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)

    config[key] = val
    with open(c.CONFIG_PATH, "wb") as f:
        tomli_w.dump(config, f)

    return config[key]


def get_config_option(key: str):
    with open(c.CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)

    return config[key]


def update_file_name():
    """
    Update the output file with the current timestamp
    """
    dt = datetime.now()
    pretty = dt.strftime("%Y-%m-%d_%H:%M:%S") + ".deets"

    pretty = os.path.join(c.OUTPUT_FOLDER, pretty)

    # Also make the output directory if it doesnt exist
    if not os.path.exists(c.OUTPUT_FOLDER):
        os.mkdir(c.OUTPUT_FOLDER)

    return set_config_option("FILE_NAME", pretty)


def validate_output(f_path):
    """
    Check that an output file was actually created. One would not be created if no events were recorded
    """

    return os.path.exists(f_path)


def parse_deetsfile(path):
    entries = []
    with open(path, "r") as f:
        for l in f:
            if l.strip() != "":
                entries.append(ast.literal_eval(l.strip()))
    return entries

import click
import webbrowser
from .utils import (
    validate_config,
    set_config_option,
    update_file_name,
    validate_output,
    check_odoo_version,
    get_config_option,
)
from .renderer import render_html
from . import config as c
import os
import subprocess


@click.group()
def deets():
    # Check to make sure config is in place
    validate_config()

    # Update config with odoo version based on git branch and make sure profiler is compatible
    check_odoo_version()

    # Check if update is available

    # Turn off recording if it was stuck 'on' (from user ctrl+c/z)
    set_config_option("RECORDING", False)


@deets.command()
def info():
    """
    Provides compatibility information for profiler
    """
    click.echo("Odoo Compatibility")
    for v in c.INJECT_PATHS:
        click.echo(f"  - {v}")


@deets.command()
def inject():
    """
    Automatically inject profiler into Odoo source code and install Deets to Odoo Universe venv
    """
    odoo_version = get_config_option("ODOO_VERSION")

    click.echo(f"Current Odoo version: {odoo_version}")

    venv_path = os.path.join(get_config_option("VENVS_PATH"), odoo_version)

    # Get the pip path
    pip_path = os.path.join(venv_path, "bin", "pip")

    install_command = [
        pip_path,
        "install",
        "--no-cache-dir",
        "odoo-deets",
    ]

    click.echo(f"Installing Deets to {venv_path}...")
    subprocess.run(install_command, check=True)

    click.echo("\nInjecting profiler...")

    # Prep injection
    inject_details = c.INJECT_PATHS[odoo_version]

    f_path = os.path.join(get_config_option("UNIVERSE_PATH"), inject_details["file"])
    import_ln = inject_details["import_line"] - 1
    dec_ln = inject_details["decorator_line"] - 1
    checks = inject_details["checks"]

    # Open file
    with open(f_path, "r") as f:
        lines = f.readlines()

    # Make sure that file has not been injected
    if lines[import_ln] == c.IMPORT_TXT and lines[dec_ln] == c.DECORATOR_TXT:
        click.echo("File already injected.")
        return

    # Check that the file is as expected
    for ln, txt in checks:
        if lines[ln - 1].strip() != txt:
            raise IndexError(
                f"Could not inject! {f_path} has been altered. Please discard any local changes to the file."
            )

    # Inject lines
    lines.insert(import_ln, c.IMPORT_TXT)
    lines.insert(dec_ln, c.DECORATOR_TXT)

    # Write to file
    with open(f_path, "w") as f:
        f.writelines(lines)

    click.echo("Success!")


@deets.command()
def remove():
    """
    Remove injected profiler from Odoo src
    """

    # TODO: DRY
    odoo_version = get_config_option("ODOO_VERSION")
    inject_details = c.INJECT_PATHS[odoo_version]

    f_path = os.path.join(get_config_option("UNIVERSE_PATH"), inject_details["file"])
    import_ln = inject_details["import_line"] - 1
    dec_ln = inject_details["decorator_line"] - 1

    # Open file
    with open(f_path, "r") as f:
        lines = f.readlines()

    # Make sure that file has been injected
    if lines[import_ln] == c.IMPORT_TXT and lines[dec_ln] == c.DECORATOR_TXT:
        lines.pop(import_ln)
        lines.pop(dec_ln - 1)

        with open(f_path, "w") as f:
            f.writelines(lines)

        click.echo("Success!")
    else:
        click.echo(
            "File was already reset or has been edited. You should discard local changes."
        )


@deets.command()
def record():
    """
    Starts a memory profile recording

    This works by updating a recording flag in the config .toml, and specifying an output filepath based on current datetime.
    Once these are set, whenever the decorated functions are hit, any profiling output will be calculated and written
    to the file.

    When a recording is stopped, the recording flag is reset to 'off', whereby no more content will be written to that output file.

    """
    # Update recording file name to write to
    f_name = update_file_name()
    set_config_option("RECORDING", True)

    click.echo(f"Recording to {f_name}")
    input("Press [ENTER] to stop recording\n")

    # User has ended recording
    set_config_option("RECORDING", False)

    if validate_output(f_name):
        # Prepare the html output
        click.echo("Preparing HTML report...")
        report = render_html(f_name)

        click.echo(f"Successfully wrote profile to {report}")
        if click.confirm("Would you like to open it now in your browser?"):
            webbrowser.open(report)
    else:
        click.echo("No events were recorded")


if __name__ == "__main__":
    deets()

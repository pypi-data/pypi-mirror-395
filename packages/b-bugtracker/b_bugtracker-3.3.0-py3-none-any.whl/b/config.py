# ======================================================================================================================
#        File:  /b/config.py
#     Project:  B Bug Tracker
# Description:  Simple bug tracker
#      Author:  Jared Julien <jaredjulien@exsystems.net>
#   Copyright:  (c) 2010-2011 Michael Diamond <michael@digitalgemstones.com>
#               (c) 2022-2025 Jared Julien <jaredjulien@exsystems.net>
# ----------------------------------------------------------------------------------------------------------------------
"""Config commands for b."""

# ======================================================================================================================
# Import Statements
# ----------------------------------------------------------------------------------------------------------------------
from rich import print
import rich_click as click

from b.context import Context




# ======================================================================================================================
# Configuration Subcommands
# ----------------------------------------------------------------------------------------------------------------------
@click.group()
def config():
    """Change configuration settings for b."""


# ----------------------------------------------------------------------------------------------------------------------
@config.command()
@click.argument('key')
@click.pass_context
def unset(ctx: Context, key):
    """Remove the saved setting identified by KEY.

    This restores the setting to it's default value.

    To list the current settings, issue the "config list" command.
    """
    ctx.obj.settings.unset(key)
    ctx.obj.settings.store()


# ----------------------------------------------------------------------------------------------------------------------
@config.command()
@click.pass_context
@click.argument('key')
@click.argument('value')
def set(ctx: Context, key: str, value: str):
    """Set the setting identified by KEY to the provided VALUE."""
    ctx.obj.settings.set(key, value)
    print(f'"{key}" set to "{value}"')
    ctx.obj.settings.store()


# ----------------------------------------------------------------------------------------------------------------------
@config.command()
@click.argument('key')
@click.pass_context
def get(ctx: Context, key: str):
    """Get the current value for the setting identified by KEY."""
    print(key, '=', ctx.obj.settings.get(key))


# ----------------------------------------------------------------------------------------------------------------------
@config.command()
@click.pass_context
def list(ctx: Context):
    """List all of the currently configured settings."""
    if ctx.obj.settings.exists:
        print(f"Config file is located at [green]{ctx.obj.settings.file}")
    else:
        print('All settings are currently defaults')

    print('Legend: [blue]setting is default[/blue] | [yellow]configured setting[/yellow] | [cyan]default value[/cyan]')

    for key, (value, default) in ctx.obj.settings.list():
        if value == default:
            color = 'blue'
            default = ''
        else:
            color = 'yellow'
            default = f'[cyan]([i]{default}[/i])[/cyan]'
        print(f'[magenta]{key:>20}:[/magenta] [{color}]{value}[/{color}] {default}')




# End of File

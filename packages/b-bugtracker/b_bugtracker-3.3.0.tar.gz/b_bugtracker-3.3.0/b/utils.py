# ======================================================================================================================
#        File:  config.py
#     Project:  B Bug Tracker
# Description:  Simple bug tracker
#      Author:  Jared Julien <jaredjulien@exsystems.net>
#   Copyright:  (c) 2010-2011 Michael Diamond <michael@digitalgemstones.com>
#               (c) 2022-2023 Jared Julien <jaredjulien@exsystems.net>
# ----------------------------------------------------------------------------------------------------------------------
"""Utility functions shared across the project."""

# ======================================================================================================================
# Imports
# ----------------------------------------------------------------------------------------------------------------------
from typing import Dict

import rich_click as click

from b.context import Context




# ======================================================================================================================
# Click Types
# ----------------------------------------------------------------------------------------------------------------------
class TemplateFileType(click.Choice):
    """A custom ParamType specifically for a template file."""
    def __init__(self, **kwargs):
        super().__init__(choices=[], **kwargs)


    def _get_choices(self, ctx: Context) -> Dict[str, str]:
        return ctx.obj.tracker.list_templates()


    def _normalized_mapping(self, ctx: Context | None = None) -> str:
        """
        Returns mapping where keys are the original choices and the values are
        the normalized values that are accepted via the command line.

        This is a simple wrapper around :meth:`normalize_choice`, use that
        instead which is supported.
        """
        return {
            choice: self.normalize_choice(
                choice=choice,
                ctx=ctx,
            )
            for choice in self._get_choices(ctx).keys()
        }


    def get_missing_message(self, param: click.Parameter, ctx: Context | None) -> str:
        """Message shown when no choice is passed."""
        choices = [f'{key:>12}: {value}' for key, value in self._get_choices(ctx).items()]
        return f"Choose from:\n{'\n'.join(choices)}"




# End of File

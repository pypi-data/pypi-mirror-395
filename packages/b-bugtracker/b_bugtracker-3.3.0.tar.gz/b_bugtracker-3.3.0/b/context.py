# ======================================================================================================================
#        File:  /b/context.py
#     Project:  B Bug Tracker
# Description:  Simple bug tracker
#      Author:  Jared Julien <jaredjulien@exsystems.net>
#   Copyright:  (c) 2010-2011 Michael Diamond <michael@digitalgemstones.com>
#               (c) 2022-2025 Jared Julien <jaredjulien@exsystems.net>
# ---------------------------------------------------------------------------------------------------------------------
"""Click context definitions to share with commands."""

# ======================================================================================================================
# Import Statements
# ----------------------------------------------------------------------------------------------------------------------
import dataclasses

import rich_click as click

from b.bugs import Tracker
from b.settings import Settings



# ======================================================================================================================
# Context Helpers
# ----------------------------------------------------------------------------------------------------------------------
@dataclasses.dataclass
class Config:
    settings: Settings = None
    tracker: Tracker = None


# ----------------------------------------------------------------------------------------------------------------------
class Context(click.Context):
    obj: Config


# ----------------------------------------------------------------------------------------------------------------------
def load_context(ctx: Context):
    ctx.ensure_object(Config)
    ctx.obj.settings = Settings()
    ctx.obj.tracker = Tracker(
        ctx.params.get('directory') or ctx.obj.settings.get('dir'),
        ctx.obj.settings.get('user'),
        ctx.obj.settings.get('editor')
    )




# End of File

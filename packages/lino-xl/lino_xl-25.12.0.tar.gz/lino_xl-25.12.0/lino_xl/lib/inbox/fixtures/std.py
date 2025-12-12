# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Creates the :setting:`inbox.upload_volume` if the `uploads` plugin is
installed.

"""

from lino.api import dd, rt
from lino import logger


def objects():
    ref = dd.plugins.inbox.upload_volume
    if not ref:
        return
    if not dd.is_installed('uploads'):
        return
    root_dir = dd.settings.SITE.site_dir / "tmp"
    # if root_dir.exists():
    #     logger.info("20240907 %s existed already", root_dir)
    # else:
    #     logger.info("20240907 Created %s", root_dir)
    root_dir.mkdir(exist_ok=True)
    desc = f"""Used by the `inbox` plugin to store incoming attachements.
The reference of this volume ("{ref}") corresponds to the
plugin setting `upload_volume`."""

    yield rt.models.uploads.Volume(root_dir=root_dir, ref=ref, description=desc)

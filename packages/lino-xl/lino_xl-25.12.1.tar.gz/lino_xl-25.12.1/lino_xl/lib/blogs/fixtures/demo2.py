# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import base64
from pathlib import Path
import lino
from lino.api import dd, rt


logo_file = Path(lino.__file__).parent / "sphinxcontrib/logo/static/logo.png"
with logo_file.open('rb') as f:
    logo = base64.b64encode(f.read()).decode("ascii")

imageDataURL = f"data:image/png;base64,{logo}"
body_with_img = f"""\
<p>Here is an image:</p>
<p><img src="{imageDataURL}" class="bar"></p>\
"""

def objects():
    if dd.is_installed("comments"):
        ses = rt.login("robin")
        obj = rt.models.comments.Comment(body=body_with_img)
        obj.on_create(ses)
        obj.after_ui_create(ses)
        obj.before_ui_save(ses, None)
        yield obj
        obj.after_ui_save(ses, None)

# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Runs the :manage:`procmail` management command.

"""

from django.core.management import call_command


def objects():
    call_command("procmail", discard=False)
    return []

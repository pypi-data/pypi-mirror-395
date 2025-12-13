# -*- coding: UTF-8 -*-
# Copyright 2015-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.core.management.base import BaseCommand, CommandError

from lino_xl.lib.inbox.models import process_inbox

from lino.api import rt, dd


class Command(BaseCommand):
    help = """

    Process the inbox.

    """

    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--discard",
            action="store_true",
            dest="discard",
            default=dd.plugins.inbox.discard_processed_message,
            help="Discard messages when processed.",
        )

    def handle(self, *args, **options):
        ar = rt.login()
        process_inbox(ar, discard=options["discard"])

# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _
from lino.utils.cycler import Cycler

named_model = dd.get_plugin_setting('nicknames', 'named_model', None)

NAMES = ["inbox", "friday", "daily"]

if named_model is not None:

    def objects():
        Naming = rt.models.nicknames.Naming
        nameables = Cycler(named_model.objects.all())
        assert len(nameables) > 0

        for u in rt.models.users.User.objects.exclude(username=""):
            for n in NAMES:
                yield Naming(user=u, named=nameables.pop(), nickname=n)

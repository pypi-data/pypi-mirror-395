# Copyright 2016 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds the notion of "user teams".

This defines common things for all user teams:

- Define the `Team` model
- Inject into `users.User` a pointer to `teams.Team`
- Define a `UsersByTeam` view
- Add a menu command to configure the list of teams.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.Plugin`."

    verbose_name = _("User teams")
    needs_plugins = ['lino.modlib.users']

    def setup_config_menu(config, site, user_type, m, ar=None):
        mg = site.plugins.system
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('teams.Teams')

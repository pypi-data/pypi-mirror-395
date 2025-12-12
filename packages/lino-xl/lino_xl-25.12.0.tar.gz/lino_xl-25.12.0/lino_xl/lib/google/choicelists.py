# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from typing import Optional, Union

from lino.api import dd, _
from lino_xl.lib.cal.choicelists import EntryStates, EntryState, GuestStates, GuestState

if dd.is_installed('google'):

    add = EntryStates.add_item

    ALLOWED_STATES_IN_GOOGLE = ('confirmed', 'tentative', 'cancelled')

    values = []
    states = []

    for state in ALLOWED_STATES_IN_GOOGLE:
        if EntryStates.get_by_name(state, None) is None:
            states.append(state)

    for v in [str(n) for n in range(51, 100)]:
        if EntryStates.get_by_value(v) is None:
            values.append(v)
            if len(values) == len(states):
                break

    for i, state in enumerate(states):
        add(values[i], _(state.capitalize()), state)

    class AccessRoles(dd.ChoiceList):
        verbose_name = _("Access Role")

    add = AccessRoles.add_item
    add('p', _("Free busy reader"),
        'freeBusyReader')  # has access to only the public events.
    add('r', _("Reader"), 'reader')
    add('w', _("Writer"), 'writer')
    add('o', _("Owner"), 'owner')

    ALLOWED_GUEST_STATES_IN_GOOGLE = [
        'needsAction', 'declined', 'tentative', 'accepted'
    ]
    values = []
    states = []

    for state in ALLOWED_GUEST_STATES_IN_GOOGLE:
        if GuestStates.get_by_name(state, None) is None:
            states.append(state)

    for v in [str(n) for n in range(51, 100)]:
        if GuestStates.get_by_value(v) is None:
            values.append(v)
            if len(values) == len(states):
                break

    add = GuestStates.add_item

    for i, state in enumerate(states):
        text = state.capitalize()
        if state == 'needsAction':
            test = "Action required"
        add(values[i], _(text), state)


def google_status(state: Union[EntryState, GuestState]) -> Optional[str]:
    if isinstance(state, EntryState):
        translation = dd.plugins.google.entry_state_translation
    else:
        assert isinstance(state, GuestState)
        translation = dd.plugins.google.guest_state_translation
    for status, st in translation:
        if state.name in st and status in ALLOWED_STATES_IN_GOOGLE:
            return status

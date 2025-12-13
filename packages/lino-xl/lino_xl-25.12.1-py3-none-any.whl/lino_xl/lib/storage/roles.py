# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core.roles import UserRole


class StorageUser(UserRole):
    pass


class StorageStaff(StorageUser):
    pass

# -*- coding: UTF-8 -*-
# Copyright 2011-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core.gfks import gfk2lookup
from lino.utils.instantiator import create_row
from lino.api import dd, rt, _
from .roles import TopicsUser

if dd.is_installed("topics"):

    class AddTagField(dd.VirtualField):
        """Virtual field for quickly adding a tag to a database object. """

        editable = True

        def __init__(self):
            return_type = dd.ForeignKey('topics.Topic',
                                        verbose_name=_("Add tag"),
                                        blank=True,
                                        null=True)
            dd.VirtualField.__init__(self, return_type)

        def set_value_in_object(self, ar, obj, value):
            if value is not None:
                Tag = rt.models.topics.Tag
                qs = Tag.objects.filter(
                    **gfk2lookup(Tag.owner, obj, topic=value))
                if qs.count() == 0:
                    create_row(Tag, topic=value, owner=obj)
                    ar.set_response(refresh=True)
                else:
                    ar.set_response(alert=_("Tried to tag {} again").format(value))
            return obj


    class AddInterestField(dd.VirtualField):
        """Virtual field adding an interest to a partner. """
        editable = True

        def __init__(self):
            return_type = dd.ForeignKey('topics.Topic',
                                        verbose_name=_("Add interest"),
                                        blank=True,
                                        null=True)
            dd.VirtualField.__init__(self, return_type, None)

        def set_value_in_object(self, ar, obj, value):
            # dd.logger.info("20170508 set_value_in_object(%s, %s)", obj, value)
            # if value is None:
            #     raise Exception("20170508")
            if value is not None:
                Interest = rt.models.topics.Interest
                if Interest.objects.filter(partner=obj, topic=value).count() == 0:
                    try:
                        create_row(Interest, topic=value, partner=obj)
                    except Exception as e:
                        dd.logger.warning("20240422 ignoring %s", e)
            return obj

        def value_from_object(self, obj, ar):
            return None

else:

    AddTagField = dd.DummyField
    AddInterestField = dd.DummyField


class Taggable(dd.Model):

    class Meta:
        abstract = True
        app_label = 'topics'

    # add_interest = AddInterestField()
    add_tag = AddTagField()

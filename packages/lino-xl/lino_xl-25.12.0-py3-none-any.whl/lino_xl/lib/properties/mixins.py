# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.conf import settings

from lino.api import dd, rt, _


class PropertyOccurence(dd.Model):

    class Meta:
        abstract = True

    group = dd.ForeignKey('properties.PropGroup')
    property = dd.ForeignKey('properties.Property')
    value = models.CharField(_("Value"),
                             max_length=settings.SITE.propvalue_max_length,
                             blank=True)

    @dd.chooser()
    def value_choices(cls, property):
        if property is None:
            return []
        return property.type.choices_for(property)

    @dd.chooser()
    def property_choices(cls, group):
        #~ print 20120212, group
        if group is None:
            return []
        return rt.models.properties.Property.objects.filter(
            group=group).order_by('name')

    def get_value_display(self, value):
        if self.property_id is None:
            return value
        return self.property.type.get_text_for_value(value)

    def full_clean(self):
        if self.property_id is not None:
            self.group = self.property.group
        super().full_clean()

    def __str__(self):
        if self.property_id is None:
            return "Undefined %s" % self.group
        # We must call str() because get_text_for_value might return a
        # lazyly translatable string:
        return str(self.property.type.get_text_for_value(self.value))
        # try:
        #     return str(self.property.type.get_text_for_value(self.value))
        # except UnicodeError:
        #     value = self.property.type.get_text_for_value(self.value)
        #     raise Exception("Failed get_text_for_value(%s, %r)" % (
        #         self.property.type.choicelist, value))

    #~ def __unicode__(self):
    #~ if self.property_id is None:
    #~ return u"Undefined %s" % self.group
    #~ return u'%s.%s=%s' % (
    #~ self.group,self.property,
    #~ self.property.type.get_text_for_value(self.value))

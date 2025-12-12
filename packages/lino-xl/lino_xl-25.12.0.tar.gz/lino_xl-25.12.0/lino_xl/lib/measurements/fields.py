# -*- coding: UTF-8 -*-
# Copyright 2022-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core.store import StoreField
from lino.core.elems import CharFieldElement

try:
    from django_measurement.models import MeasurementField
except ImportError:

    class MeasurementField:
        pass

class MeasurementStoreField(StoreField):
    def extract_form_data(self, obj, post_data, ar=None):
        unit = self.field.measurement.STANDARD_UNIT
        if hasattr(obj, "unit"):
            new_unit = post_data.get("unitHidden", None)
            if new_unit is not None:
                unit = new_unit
            elif obj.unit is not None:
                unit = obj.unit.name
        return self.field.measurement(**{unit: float(post_data.get(self.name, "0.0"))})

MeasurementStoreField.register_for_field(MeasurementField, CharFieldElement)

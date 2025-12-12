# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from lino.utils import SumCollector
from lino.api import dd, rt, _
from lino_xl.lib.accounting.mixins import LedgerRegistrable
from lino_xl.lib.invoicing.mixins import InvoiceGenerator
# from lino.utils.quantities import Quantity

# NO_TRANSFER_RULE = "No transfer rule for {}. Available rules are {}"


class Storable(dd.Model):  # inherited by products.Product

    class Meta:
        abstract = True

    if dd.is_installed('storage'):
        storage_management = models.BooleanField(_("Storage management"),
                                                 default=False)
    else:
        storage_management = dd.DummyField()


# class StorageTransferer(dd.Model):
class StorageTransferer(LedgerRegistrable):

    class Meta:
        abstract = True

    if dd.is_installed('storage'):

        def check_provisions_by_product(self, product):
            # called when voucher is registered or de-registered
            partner = self.get_partner()
            qs = rt.models.storage.Movement.objects.filter(
                product=product, partner=partner).order_by('value_date')
            # print("20230614 {} {} -> {}".format(partner, product, qs))
            jnl_sums = SumCollector()
            for mvt in qs:
                jnl_sums.collect(mvt.voucher.journal, mvt.qty)
            # print("20230614 jnl_sums is {}".format(jnl_sums))
            state_sums = SumCollector()
            for jnl, qty in jnl_sums.items():
                qty = jnl.dc.normalized_amount(qty)
                for tr in rt.models.storage.TransferRule.objects.filter(
                        journal=jnl):
                    if tr.from_state is not None:
                        state_sums.collect(tr.from_state, -qty)
                    if tr.to_state is not None:
                        state_sums.collect(tr.to_state, qty)
            # print("20230614 state_sums is {}".format(state_sums))
            # raise Exception("20230614 {}".format(state_sums))
            for ss, qty in state_sums.items():
                # print("20230614", ss, qty)
                obj, created = rt.models.storage.Provision.objects.get_or_create(
                    product=product, partner=partner, provision_state=ss)
                obj.qty = qty
                obj.full_clean()
                # print("20230614", obj.qty)
                obj.save()

        def get_wanted_movements(self, ar=None):

            for mvt in super().get_wanted_movements(ar):
                yield mvt

            # TransferRule = rt.models.storage.TransferRule
            # state = TransferRule.find_target_state(self)
            # if state is None:
            #     print(NO_TRANSFER_RULE.format(
            #         self.journal, list(map(str, TransferRule.objects.all()))))
            #     return

            if not self.journal.make_storage_movements:
                return
            # print("20230614 get_wanted_movements(ar)")
            Component = rt.models.storage.Component
            sums = SumCollector()
            for i in self.items.filter(product__isnull=False).exclude(qty=""):
                qty = self.journal.dc.normalized_amount(i.qty)
                if i.product.storage_management:
                    sums.collect(i.product, qty)
                    # yield self.create_storage_movement(i, i.product, qty)
                for ci in Component.objects.filter(
                        parent=i.product).order_by('id'):
                    # qty = qty * ci.qty
                    # print("20230622 {} * {} = {} ({})".format(
                    #     i.qty.__class__, ci.qty.__class__, qty, i.product.delivery_unit))
                    sums.collect(ci.child, qty * ci.qty)
                    # yield self.create_storage_movement(i, ci.child, qty * ci.qty)
                    # raise Exception("20230620 yes")
            for product, qty in sums.items():
                yield self.create_storage_movement(i, product, qty)

        def create_storage_movement(self, item, product, qty, **kw):
            # print("20230528 create_storage_movement()")
            # if product.storage_management:
            #     kw.update(cleared=False)
            # else:
            #     kw.update(cleared=True)
            # kw['amount'] = amount
            kw['voucher'] = self
            kw['product'] = product
            kw['value_date'] = self.entry_date
            kw['partner'] = self.get_partner()
            kw['qty'] = qty
            return rt.models.storage.Movement(**kw)

        @classmethod
        def check_clearings_by_partner(cls, partner, matches=[]):
            super().check_clearings_by_partner(partner, matches=matches)
            # TODO: clear storage movements for this partner

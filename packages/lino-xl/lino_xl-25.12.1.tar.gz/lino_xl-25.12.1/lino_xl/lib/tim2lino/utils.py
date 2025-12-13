# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Import legacy data from TIM (basic version).
"""

import os
import traceback
import datetime
from pathlib import Path
from dateutil import parser as dateparser
from click import progressbar
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from lino.utils import AttrDict
# from lino import logger
from lino.api import dd, rt
from lino.utils import dbfreader
from lino_xl.lib.accounting.utils import DC, ZERO
from lino_xl.lib.accounting.choicelists import VoucherTypes


def datevalue(v):
    if v:
        if isinstance(v, str):
            v = dateparser.parse(v)
        if isinstance(v, datetime.datetime):
            v = v.date()
    return v


def store_date(row, obj, rowattr, objattr):
    if v := datevalue(row[rowattr]):
        setattr(obj, objattr, v)


ignore_diffs_below = dd.get_plugin_setting('tim2lino', 'ignore_diffs_below', 0.02)


def isdiff(a, b):
    return abs((a or ZERO) - (b or ZERO)) > ignore_diffs_below


class TimLoader:

    LEN_IDGEN = 6
    ROOT = None

    archived_tables = set()
    archive_name = None
    codepage = 'cp850'
    # codepage = 'cp437'
    # etat_registered = "C"¹
    etat_registered = u"¹"

    FINDER_FIELDS = {
        rt.models.countries.Place: ('country', 'zip_code', 'name'),
        rt.models.countries.Country: ('isocode', 'name'),
        rt.models.accounting.Account: ("ref",),
        rt.models.periods.StoredPeriod: ("ref",),
        rt.models.users.User: ("username",),
        rt.models.sepa.Account: ("iban",),
    }

    def __init__(self, dbpath, languages=None, logger=None, **kwargs):
        self.dbpath = Path(dbpath).expanduser()
        self.VENDICT = dict()
        self.FINDICT = dict()
        self.GROUPS = dict()
        self.languages = dd.resolve_languages(languages
                                              or dd.plugins.tim2lino.languages)
        self.must_register = []
        self.must_match = {}
        self.duplicate_zip_codes = dict()
        self.logger = logger or dd.logger
        indfile = settings.SITE.site_dir / "tim2lino.ind"
        for k, v in kwargs.items():
            assert hasattr(self, k)
            setattr(self, k, v)
        if indfile.exists():
            self.last_import_time = indfile.stat().st_mtime
            lit = datetime.datetime.fromtimestamp(self.last_import_time)
            self.logger.info("Last import time was %s", lit)
        else:
            self.last_import_time = None

        if dd.is_installed('products'):
            self.FINDER_FIELDS[rt.models.products.Product] = ("ref",)
        if dd.is_installed('accounting'):
            self.FINDER_FIELDS[rt.models.accounting.Journal] = ("ref",)
            for m in rt.models_by_base(rt.models.accounting.Voucher):
                if m is not rt.models.accounting.Voucher:
                    self.FINDER_FIELDS[m] = ('journal', 'number', 'fiscal_year')
                    if hasattr(m, 'items'):
                        self.FINDER_FIELDS[m.get_items_model()] = ('voucher', 'seqno')

        # rt.models.trading.VatProductInvoice:
        # rt.models.trading.InvoiceItem:
        # rt.models.vat.VatAccountInvoice: ('journal', 'number', 'fiscal_year'),
        # rt.models.vat.InvoiceItem: ('voucher', 'seqno'),
        # rt.models.finan.BankStatement: ('journal', 'number', 'fiscal_year'),
        # rt.models.finan.BankStatementItem: ('voucher', 'seqno'),
        # rt.models.finan.JournalEntry: ('journal', 'number', 'fiscal_year'),
        # rt.models.finan.JournalEntryItem: ('voucher', 'seqno'),
        # rt.models.finan.PaymentOrder: ('journal', 'number', 'fiscal_year'),
        # rt.models.finan.PaymentOrderItem: ('voucher', 'seqno'),

    def get_or_save(self, row, model, **values):
        if (flds := self.FINDER_FIELDS.get(model)) is None:
            flds = ('id', )
            # raise Exception(f"{model} has no entry in FINDER_FIELDS")
        for k in flds:
            if k not in values:
                raise Exception(f"get_or_save() requires {k} for {model}")
        kw = {k: values[k] for k in flds}
        qs = model.objects.filter(**kw)
        if qs.count() == 1:
            self.logger.debug("Reuse existing %s %s", model, kw)
            obj = qs.first()
            diffs = []
            for k, v in values.items():
                if v:
                    if (old := getattr(obj, k)) != v:
                        diffs.append(f"{k} {old} != {v}")
            if len(diffs):
                self.logger.warning(
                    "Reuse %s from %s, but %s", obj, row, ", ".join(diffs))
            return obj
        elif qs.count() > 1:
            raise Exception(f"{model} has multiple rows for {kw}")
        obj = model(**values)
        try:
            obj.full_clean()
        except ValidationError as e:
            raise
            self.logger.warning("Failed to save %s: %s", obj, e)
            return
        dd.plugins.tim2lino.on_row_create(settings.SITE, obj)
        obj.save()
        return obj

    def finalize(self):
        if len(self.duplicate_zip_codes):
            for country, codes in self.duplicate_zip_codes.items():
                self.logger.warning("%d duplicate zip codes in %s : %s",
                                    len(codes), country, ', '.join(codes))

        if self.ROOT is None:
            self.logger.info("Nothing to finalize (no root user)")
            return

        ses = rt.login(self.ROOT.username)

        Journal = rt.models.accounting.Journal
        self.logger.info("Register %d vouchers", len(self.must_register))
        failures = 0
        with progressbar(self.must_register) as bar:
            for doc, checkdict in bar:
                # puts("Registering {0}".format(doc))
                try:
                    doc.register(ses)
                except Exception as e:
                    self.logger.exception("Failed to register %s : %s ", doc, e)
                    failures += 1
                    if failures > 100:
                        self.logger.warning("Abandoned after 100 failures.")
                        break
                diffs = dict()
                for k, v in checkdict.items():
                    if isdiff(getattr(doc, k), v):
                        diffs[k] = f"{k} is {getattr(doc, k)} instead of {v}"
                if len(diffs):
                    self.logger.warning(
                        "Checkdict failure after registering %s : %s", doc, diffs)

        # Given a string `ms` of type 'VKR940095', locate the corresponding
        # movement.
        self.logger.info("Resolving %d matches", len(self.must_match))
        for ms, lst in self.must_match.items():
            for (voucher, matching) in lst:
                if matching.pk is None:
                    self.logger.warning("Ignored match %s in %s (pk is None)" %
                                        (ms, matching))
                    continue
                idjnl, iddoc = ms[:3], ms[3:]
                try:
                    year, num = year_num(iddoc)
                except ValueError as e:
                    self.logger.warning("Ignored match %s in %s (%s)" %
                                        (ms, matching, e))
                try:
                    jnl = Journal.objects.get(ref=idjnl)
                except Journal.DoesNotExist:
                    self.logger.warning("Ignored match %s in %s (invalid JNL)" %
                                        (ms, matching))
                    continue
                qs = Movement.objects.filter(voucher__journal=jnl,
                                             voucher__number=num,
                                             voucher__year=year,
                                             partner__isnull=False)
                if qs.count() == 0:
                    self.logger.warning("Ignored match %s in %s (no movement)" %
                                        (ms, matching))
                    continue
                matching.match = qs[0]
                matching.save()
                voucher.deregister(ses)
                voucher.register(ses)
        indfile = settings.SITE.site_dir / "tim2lino.ind"
        indfile.touch()

    def par_class(self, row):
        # wer eine nationalregisternummer hat ist eine Person, selbst wenn er
        # auch eine MwSt-Nummer hat.
        if True:  # must convert them manually
            return rt.models.contacts.Company
        prt = row.idprt
        if prt == 'O':
            return rt.models.contacts.Company
        elif prt == 'L':
            return rt.models.lists.List
        elif prt == 'P':
            return rt.models.contacts.Person
        elif prt == 'F':
            return rt.models.households.Household
        # self.logger.warning("Unhandled PAR->IdPrt %r",prt)

    def dc2lino(self, dc):
        if dc == "D":
            return DC.debit
        elif dc == "C":
            return DC.credit
        elif dc == "A":
            return DC.debit
        elif dc == "E":
            return DC.credit
        raise Exception("Invalid D/C value %r" % dc)

    def create_users(self):
        pass

    def dbfmemo(self, s):
        if s is None:
            return ''
        s = s.replace('\r\n', '\n')
        s = s.replace(u'\xec\n', '')
        # s = s.replace(u'\r\nì',' ')
        # if u'ì' in s:
        #     raise Exception("20121121 %r contains \\xec" % s)
        # it might be at the end of the string:
        s = s.replace(u'ì', '')
        return s.strip()

    def after_gen_load(self):
        return
        Account = rt.models.accounting.Account
        sc = dict()
        for k, v in dd.plugins.tim2lino.siteconfig_accounts.items():
            sc[k] = Account.get_by_ref(v)
        settings.SITE.site_config.update(**sc)
        # func = dd.plugins.tim2lino.setup_tim2lino
        # if func:
        #     func(self)

    def after_jnl_load(self):
        if dd.is_installed("peppol"):
            obj = self.get_or_save(
                None, rt.models.accounting.Journal,
                ref="INB", name="Inbound invoices",
                trade_type=rt.models.vat.TradeTypes.purchases,
                voucher_type=VoucherTypes.get_for_table(
                   rt.models.peppol.ReceivedInvoicesByJournal
                   ),
                journal_group=rt.models.accounting.JournalGroups.purchases,
                auto_check_clearings=False, dc=DC.debit)

    def after_par_load(self):
        pass
        # if (x := dd.plugins.tim2lino.site_owner_id) is not None:
        #     settings.SITE.site_config.update(site_company_id=x)

    def decode_string(self, v):
        return v
        # return v.decode(self.codepage)

    def babel2kw(self, tim_fld, lino_fld, row, kw):
        if dd.plugins.tim2lino.use_dbf_py:
            import dbf
            ex = dbf.FieldMissingError
        else:
            ex = Exception
        for i, lng in enumerate(self.languages):
            try:
                v = getattr(row, tim_fld + str(i + 1), '').strip()
                if v:
                    v = self.decode_string(v)
                    kw[lino_fld + lng.suffix] = v
                    if lino_fld not in kw:
                        kw[lino_fld] = v
            except ex as e:
                pass
                self.logger.info("Ignoring %s", e)

    def load_jnl_alias(self, row, **kw):
        vtt = None  # voucher_type table: the table used to select the voucher type
        accounting = rt.models.accounting
        if row.alias == 'VEN':
            vat = rt.models.vat
            trading = rt.models.trading
            if row.idctr == 'V':
                kw.update(trade_type=vat.TradeTypes.sales)
                kw.update(journal_group=accounting.JournalGroups.sales)
                vtt = trading.InvoicesByJournal
            elif row.idctr == 'E':
                kw.update(trade_type=vat.TradeTypes.purchases)
                vtt = vat.InvoicesByJournal
                kw.update(journal_group=accounting.JournalGroups.purchases)
            else:
                raise Exception("Invalid JNL->IdCtr '{0}'".format(row.idctr))
        elif row.alias == 'FIN':
            vat = rt.models.vat
            finan = rt.models.finan
            idgen = row.idgen.strip()
            kw.update(journal_group=accounting.JournalGroups.financial)
            if idgen:
                kw.update(account=accounting.Account.get_by_ref(idgen))
                if idgen.startswith('58'):
                    kw.update(trade_type=vat.TradeTypes.purchases)
                    vtt = finan.PaymentOrdersByJournal
                elif idgen.startswith('5'):
                    vtt = finan.BankStatementsByJournal
            else:
                vtt = finan.JournalEntriesByJournal
        # if vt is None:
        #     raise Exception("Journal type not recognized: %s" % row.idjnl)
        vtt = dd.plugins.tim2lino.override_voucher_type(row, vtt)
        return vtt, kw

    def load_jnl(self, row, **kw):
        idjnl = row.idjnl.strip()
        if idjnl in dd.plugins.tim2lino.ignore_journals:
            self.logger.debug("Ignore journal %s mentioned in ignore_journals", idjnl)
            return
        if row.alias == 'FIN' and dd.plugins.tim2lino.import_finan:
            self.logger.info("Ignore journal %s because import_finan is False", idjnl)
            return
        kw.update(ref=idjnl, name=row.libell)
        if not row.dc.strip():
            self.logger.info("Ignore journal %s because DC is empty", kw)
            return
        kw.update(dc=self.dc2lino(row.dc).opposite())
        # kw.update(seqno=self.seq2lino(row.seq.strip()))
        kw.update(seqno=int(row.seq.strip()))
        # kw.update(seqno=row.recno())
        kw.update(auto_check_clearings=False)
        vtt, kw = self.load_jnl_alias(row, **kw)
        if vtt is not None:
            vt = VoucherTypes.get_for_table(vtt)
            kw = vt.get_journal_kwargs(**kw)
            return self.get_or_save(row, rt.models.accounting.Journal, **kw)
        self.logger.warning("Ignore journal %s because voucher_type is none", row)

    def load_dbf(self, tableName, row2obj=None):
        fn = self.dbpath
        if self.archive_name is not None:
            if tableName in self.archived_tables:
                fn /= self.archive_name
        fn /= (tableName + dd.plugins.tim2lino.dbf_table_ext)
        mtime = fn.stat().st_mtime
        if self.last_import_time and mtime < self.last_import_time:
            self.logger.info("No need to import %s (%r is less than %r)",
                             fn, mtime, self.last_import_time)
            return
        if row2obj is None:
            row2obj = getattr(self, 'load_' + tableName[-3:].lower())
        count = 0
        if dd.plugins.tim2lino.use_dbf_py:
            self.logger.info("Loading %s...", fn)
            import dbf  # http://pypi.python.org/pypi/dbf/
            # table = dbf.Table(fn)
            table = dbf.Table(fn, codepage=self.codepage)
            # table.use_deleted = False
            table.open()
            # print table.structure()
            self.logger.info(
                "Loading %d records from %s (%s)...", len(table), fn, table.codepage)
            for record in table:
                if not dbf.is_deleted(record):
                    try:
                        yield row2obj(record)
                        count += 1
                    except Exception as e:
                        traceback.print_exc()
                        self.logger.warning(
                            "Failed to load record %s from %s : %s", record,
                            tableName, e)

                    # i = row2obj(record)
                    # if i is not None:
                    #     yield settings.TIM2LINO_LOCAL(tableName, i)
            table.close()
        elif dd.plugins.tim2lino.use_dbfread:
            self.logger.info("Loading readonly %s...", fn)
            from dbfread import DBF
            dbf = DBF(fn)
            for record in dbf:
                d = {f.name.lower(): record[f.name] for f in dbf.fields}
                d = AttrDict(d)
                try:
                    yield row2obj(d)
                    count += 1
                except Exception as e:
                    self.logger.warning("Failed to load record %s from %s : %s",
                                        record, tableName, e)

        else:
            f = dbfreader.DBFFile(str(fn), codepage="cp850")
            self.logger.info("Loading %d records from %s...", len(f), fn)
            f.open(deleted=True)
            # must set deleted=True and then filter them out myself
            # because big tables can raise
            # RuntimeError: maximum recursion depth exceeded in cmp
            for dbfrow in f:
                if not dbfrow.deleted():
                    try:
                        i = row2obj(dbfrow)
                        if i is not None:
                            yield settings.TIM2LINO_LOCAL(tableName, i)
                            count += 1
                    except Exception as e:
                        traceback.print_exc()
                        self.logger.warning("Failed to load record %s : %s",
                                            dbfrow, e)
            f.close()

        self.logger.info("{} rows have been loaded from {}.".format(count, fn))
        self.after_load(tableName)

    def after_load(self, tableName):
        for tableName2, func in dd.plugins.tim2lino.load_listeners:
            if tableName2 == tableName:
                func(self)

    def expand(self, obj):
        if obj is None:
            pass  # ignore None values
        elif isinstance(obj, models.Model):
            yield obj
        elif hasattr(obj, '__iter__'):
            for o in obj:
                for so in self.expand(o):
                    yield so
        else:
            self.logger.warning("Ignored unknown object %r", obj)

    def objects(self):
        "Override this by subclasses."
        return []

    @ classmethod
    def run(cls):
        """To be used when running this loader from a run script.

        Usage example::

            from lino_xl.lib.tim2lino.spzloader2 import TimLoader
            TimLoader.run()

        """
        self = cls(dd.plugins.tim2lino.tim_data_path)
        counts = {}
        for o in self.expand(self.objects()):
            c = counts.setdefault(o.__class__, [0, 0])
            try:
                o.full_clean()
                o.save()
                c[0] += 1
            except Exception as e:
                c[1] += 1
                self.logger.warning("Failed to save %s : %s", dd.obj2str(o), e)

            # temporary:
            # self.logger.info("Saved %s", dd.obj2str(o))
        self.finalize()
        if counts:
            for m in sorted(counts.keys()):
                c = counts[m]
                self.logger.info("%s : %d success, %d failed.", m, c[0], c[1])
        else:
            self.logger.info("No objects have been imported.")

# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Import legacy data from TIM (basic version).

Usage:

- Add ``'tim2lino'`` to your :attr:`demo_fixtures <lino.core.site.Site.demo_fixtures>`

- Run :cmd:`pm prep` to import first time

- Optionally run :cmd:`pm loaddata tim2lino` to update.

"""

from decimal import Decimal, InvalidOperation
import datetime
from django.utils.timezone import make_aware
from django.core.exceptions import ValidationError
from django.conf import settings

from lino.api import dd, rt
from lino.core.utils import is_valid_email
from lino.core.utils import obj2str
from lino_xl.lib.vat.choicelists import VatClasses, VatRegimes
from lino_xl.lib.tim2lino.utils import TimLoader, datevalue
# from lino_xl.lib.accounting.utils import myround
from lino_xl.lib.accounting.utils import ZERO
from lino_xl.lib.sheets.choicelists import CommonItems
from lino.mixins import Created
from lino.utils import dpy

GET_THEM_ALL = True

# from lino.utils.quantities import Duration


# Activity = dd.resolve_model('pcsw.Activity')
Country = dd.resolve_model('countries.Country')
Place = dd.resolve_model('countries.Place')
Person = dd.resolve_model("contacts.Person")
Company = dd.resolve_model("contacts.Company")
Account = rt.models.accounting.Account
StoredYear = rt.models.periods.StoredYear
StoredPeriod = rt.models.periods.StoredPeriod
# Group = dd.resolve_model('accounts.Group')
Journal = dd.resolve_model('accounting.Journal')
Movement = dd.resolve_model('accounting.Movement')
PaymentTerm = dd.resolve_model('accounting.PaymentTerm')
# potentially UnresolvedModel:
Household = dd.resolve_model('households.Household')
List = dd.resolve_model('lists.List')

if True:
    users = dd.resolve_app('users')
    households = dd.resolve_app('households')
    vat = dd.resolve_app('vat')
    trading = dd.resolve_app('trading')
    accounting = dd.resolve_app('accounting')
    products = dd.resolve_app('products')
    contacts = dd.resolve_app('contacts')
    finan = dd.resolve_app('finan')
    sepa = dd.resolve_app('sepa')
    lists = dd.resolve_app('lists')

CAR_BRANDS = dict()
for ln in """
ALF|Alfa Romeo
ANH|Anhänger
AUD|Audi
BMW|BMW
CHE|Chevrolet
CHR|Chrysler
CIT|Citroën
DAE|Daewoo
DAC|Dacia
DAI|Daihatsu
DOD|Dodge
FIA|Fiat
EBI|E-Bike
FOR|Ford
HON|Honda
HYU|Hyundai
ISU|Isuzu
IVE|Iveco
JAG|Jaguar
JEE|Jeep
KIA|Kia
LAD|Lada
LAN|Lancia
LIN|Linhai
LRO|Land Rover
MAZ|Mazda
MER|Mercedes-Benz
MGG|MG
MIN|Mini
MIT|Mitsubishi
NIS|Nissan
OPE|Opel
PEU|Peugeot
PLY|Plymouth
PON|Pontiac
POR|Porsche
REM|Remorque
REN|Renault
ROV|Rover
SAB|Saab
SEA|Seat
SKO|Skoda
SMA|Smart
SSA|Ssangyong
SUB|Subaru
SUZ|Suzuki
TOY|Toyota
VOL|Volvo
VWA|VW
""".splitlines():
    if ln:
        k, v = ln.split('|')
        CAR_BRANDS[k.strip()] = v.strip()


# if dd.is_installed('vat'):
#     VatRule = rt.models.vat.VatRule

# def convert_username(name):
# return name.lower()

# def d2p(date):
#     return StoredPeriod.get_or_create_from_date(date)


def layout2pt(layout):
    # V|Verkauf
    # R|Reparatur Verkauf
    # E|Einkauf
    # K|Kosten (intern)
    # I|Interer Einkauf/Verkauf
    if layout == "V":
        return "car_sale"
    return "letter"


def tax2vat(idtax):
    idtax = idtax.strip()
    normal = VatClasses.goods
    if idtax in {'D20', 'D21', 'N21', 'D18', '21', 'IM', 'IS', 'XS', 'A'}:
        return normal
    elif idtax in {'0', 'A0', "NIM"}:
        return VatClasses.exempt
    elif idtax in {'6', 'D6', 'A6', 'IM6', '12', 'D12'}:
        return VatClasses.reduced
    elif idtax in {'C'}:
        return None
    else:
        return None
    #     return normal
    raise Exception("Unknown VNl->IdTax %r" % idtax)


def vat_regime(idreg):
    if idreg == 'A':
        return VatRegimes.subject
    elif idreg == 'P':
        return VatRegimes.private
    elif idreg == 'C':
        return VatRegimes.cocontractor
    elif idreg == 'I':
        return VatRegimes.intracom
    elif idreg == 'S':
        return VatRegimes.intracom
    elif idreg == 'X':
        return VatRegimes.outside
    elif idreg == 'M':
        return VatRegimes.margin
    elif idreg == '0':
        return VatRegimes.exempt
    elif idreg == 'D':
        return VatRegimes.de
    elif idreg == 'L':
        return VatRegimes.lu


def pcmn2type(idgen):
    if idgen[0] == '6':
        return CommonItems.expenses
    if idgen[0] == '7':
        return CommonItems.incomes
    if idgen[0] == '4':
        return CommonItems.liabilities
    return CommonItems.assets


def tim2bool(x):
    if not x.strip():
        return False
    return True


def convert_gender(v):
    if v in ('W', 'F'):
        return 'F'
    if v == 'M':
        return 'M'
    return None


def mton(s, default=None, decpos=2):  # PriceField
    s = s.strip()
    if not s:
        return default
    if s != "GRATIS":
        # TIM accepted an (erroneous) amount '36535..23' as 36535
        # (omitting the part after the duplicated ".")
        i = s.find('..')
        if i != -1:
            s = s[:i]
        try:
            return round(Decimal(s), decpos)
        except InvalidOperation:
            raise Exception(f"Invalid value {s} for mton()")
    return Decimal()


def mtonu(s, default=None):
    return mton(s, default, decpos=dd.plugins.vat.unit_price_decpos)


def qton(s):  # QuantityField
    return s.strip()
    # s = s.strip()
    # if s:
    # if ':' in s: return Duration(s)
    # if s.endswith('%'):
    # return Decimal(s[:-1]) / 100
    # return Decimal(s)
    # return None


def isolang(x):
    if x == 'K':
        return 'et'
    if x == 'E':
        return 'en'
    if x == 'D':
        return 'de'
    if x == 'F':
        return 'fr'
    # if x == 'N' : return 'nl'


def try_full_clean(i):
    while True:
        try:
            i.full_clean()
        except ValidationError as e:
            if not hasattr(e, 'message_dict'):
                raise
            for k in e.message_dict.keys():
                fld = i._meta.get_field(k)
                v = getattr(i, k)
                setattr(i, k, fld.default)
                self.logger.warning("%s : ignoring value %r for %s : %s",
                                    obj2str(i), v, k, e)
        return


class TimLoader(TimLoader):

    sales_gen2art = dict()
    """A dict that maps a `GEN->IdGen` to a product instance or id.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_invoice_line = None

    def get_customer(self, pk):
        pk = pk.strip()
        if not pk:
            return None
        pk = self.par_pk(pk)
        try:
            return contacts.Partner.objects.get(pk=pk)
        except contacts.Partner.DoesNotExist:
            return None

    def par_pk(self, pk):
        if not pk.strip():
            return None
        if pk.startswith('T'):
            return 3000 + int(pk[1:]) - 256
        else:
            return int(pk)
            # try:
            #     return int(pk)
            # except ValueError:
            #     print(f"20250422 Invalid value {pk} for par_pk()")

    def store(self, kw, **d):
        for k, v in d.items():
            if v is not None:
                if isinstance(v, str):
                    v = self.decode_string(v).strip()
            # if v:
                kw[k] = v

    def row_to_payment_term(self, row):
        idmfc = row.idmfc.strip()
        if not idmfc:
            return

    def row2jnl(self, row):
        idjnl = row.idjnl.strip()
        if idjnl in dd.plugins.tim2lino.ignore_journals:
            return None, None, None, None
        try:
            jnl = Journal.objects.get(ref=idjnl)
        except Journal.DoesNotExist:
            return None, None, None, None

        iyear = 2000 + int(row.iddoc[:2])
        if iyear < dd.plugins.periods.start_year:
            return None, None, None, None
        year = StoredYear.get_or_create_from_date(datetime.date(iyear, 1, 1))

        if hasattr(row, 'periode'):
            month = int(row.periode[-2:])
            sep = rt.models.periods.YEAR_PERIOD_SEP
            ref = year.ref + sep + "{:0>2}".format(month)
            period = StoredPeriod.get_by_ref(ref, None)
            if period is None:
                date = datetime.date(iyear, month, 1)
                sd, ed = StoredPeriod.get_range_for_date(date)
                period = self.get_or_save(
                    row, StoredPeriod, ref=ref, start_date=sd, end_date=ed)
        else:
            period = None

        num = int(row.iddoc[2:])

        # if year < 2002:
        #     # Don't import vouchers before 2002. TODO: make this
        #     # configurable
        #     return None, None, None
        return jnl, year, period, num

    def short2iso(self, s):
        if s == 'B':
            return 'BE'
        if s == 'D':
            return 'DE'
        if s == 'F':
            return 'FR'
        if s == 'L':
            return 'LU'
        if s == 'E':
            return 'ES'
        if s == 'H':
            return 'HU'
        if s == 'I':
            return 'IT'
        if s == 'USA':
            return 'US'
        if s == 'A':
            return 'AT'
        if s == 'AU':
            return 'AT'
        if s == 'AUS':
            return 'AU'
        if s == 'BEN':
            return 'BJ'
        if s == 'ANG':
            return 'AO'
        if s in {'TUN', 'TU'}:
            return 'TN'
        if s == 'EST':
            return 'EE'
        if s == 'SLO':
            return 'SK'
        if s == 'S':
            return 'SE'
        if s == 'D-':
            return 'DE'
        if s == 'COL':
            return 'CO'
        if s == 'CAM':
            return 'CM'
        if s == 'SF':
            return 'FI'
        if s == 'BRA':
            return 'BR'
        if s == 'LET':
            return 'LV'
        if s == 'VIE':
            return 'VN'
        if s == 'BOS':
            return 'BA'
        if s == 'ALG':
            return 'AL'
        if s == 'MAL':
            return 'MT'
        if s == 'KAS':
            return 'KZ'
        if s == 'JU':
            return 'VG'
        if s == 'BUR':
            return 'BF'
        if s == 'KRO':
            return 'KRO'
        if s == 'TOG':
            return 'TG'
        if s == 'KOS':
            return 'XK'
        if s == 'WEI':
            return 'BY'
        if s == 'ABI':
            return 'ABI'
        if s == 'LIB':
            return 'LB'
        if s == 'NOR':
            return 'NO'
        return s
        # if s == 'AU': return 'AU'
        # if s == 'NL': return 'NL'
        # raise Exception("Unknown short country code %r" % s)

    def load_gen2group(self, row, **kw):
        idgen = row.idgen.strip()
        if not idgen:
            return
        if len(idgen) < self.LEN_IDGEN:
            # dclsel = row.dclsel.strip()
            kw.update(ref=idgen)
            # if dd.is_installed('sheets'):
            #     kw.update(sheet_item=pcmn2type(idgen))
            self.babel2kw('libell', 'name', row, kw)
            # def names2kw(kw,*names):
            # names = [n.strip() for n in names]
            # kw.update(name=names[0])
            # names2kw(kw,row.libell1,row.libell2,row.libell3,row.libell4)
            # """TIM accepts empty GEN->Libell fields. In that
            # case we take the ref as name.
            # """
            # kw.setdefault('name', idgen)
            # ag = accounts.Group(**kw)
            # self.GROUPS[idgen] = ag
            # yield ag

    def load_gen2account(self, row, **kw):
        idgen = row.idgen.strip()
        if not idgen:
            return
        if len(idgen) == self.LEN_IDGEN:
            # ag = None
            # for length in range(len(idgen), 0, -1):
            #     # print idgen[:length]
            #     ag = self.GROUPS.get(idgen[:length])
            #     if ag is not None:
            #         break
            # dclsel = row.dclsel.strip()
            kw.update(ref=idgen)
            # kw.update(group=ag)
            # if dd.is_installed('sheets'):
            #     kw.update(sheet_item=pcmn2type(idgen))
            self.babel2kw('libell', 'name', row, kw)
            kw.update(purchases_allowed=True)
            kw.update(sales_allowed=True)
            if 'name' not in kw:
                kw['name'] = idgen
            # def names2kw(kw,*names):
            # names = [n.strip() for n in names]
            # kw.update(name=names[0])
            # names2kw(kw,row.libell1,row.libell2,row.libell3,row.libell4)
            yield self.get_or_save(row, Account, **kw)
            # obj = Account(**kw)
            # if idgen == "612410":
            # raise Exception(20131116)
            # self.logger.info("20131116 %s",dd.obj2str(obj))
            # self.logger.info("20131116 ACCOUNT %s ",obj)
            # yield obj

    def get_account(self, idgen):
        idgen = idgen.strip()
        if not idgen:
            return None
        try:
            return accounting.Account.objects.get(ref=idgen)
        except accounting.Account.DoesNotExist:
            return None

    def load_fin(self, row, **kw):
        jnl, year, period, number = self.row2jnl(row)
        if period is None:
            return
        if jnl is None:
            self.logger.info("No journal %s (%s)", row.idjnl, row)
            return
        assert year == period.year
        kw.update(fiscal_year=year)
        kw.update(accounting_period=period)
        kw.update(number=number)
        kw.update(journal=jnl)
        # kw.update(id=pk)
        kw.update(entry_date=datevalue(row.date))
        kw.update(voucher_date=datevalue(row.date))
        kw.update(user=self.get_user())
        model = jnl.get_doc_model()
        if model is rt.models.finan.BankStatement:
            kw.update(balance1=mton(row.mont1, ZERO))
            kw.update(balance2=mton(row.mont2, ZERO))
        elif model is rt.models.finan.PaymentOrder:
            kw.update(total=mton(row.mont2, ZERO))
        doc = self.get_or_save(row, model, **kw)
        # doc = jnl.create_voucher(**kw)
        # self.FINDICT[(jnl.ref, year.ref, number)] = doc
        # print row.etat
        if row.etat == self.etat_registered:
            self.must_register.append((doc, {}))
        return doc

    def load_fnl(self, row, **kw):
        jnl, year, period, number = self.row2jnl(row)
        if year is None:
            return
        assert period is None
        if jnl is None:
            self.logger.info("No journal %s (%s)", row.idjnl, row)
            return
        # doc = self.FINDICT.get((jnl.ref, year.ref, number))
        # if doc is None:
        #     msg = f"FNL {jnl.ref} without document {number} in {year.ref}"
        #     # raise Exception(msg)
        #     self.logger.warning(msg)
        #     return
        try:
            doc = jnl.get_voucher(year, number)
        except jnl.get_doc_model().DoesNotExist:
            msg = f"FNL {jnl.ref} without document {number} in {year.ref}"
            self.logger.warning(msg)
            return
        try:
            kw.update(seqno=int(row.line.strip()))
        except ValueError:
            pass  # some lines contain "***"
        if row.date:
            kw.update(date=datevalue(row.date))
        try:
            if row.idctr == ('V'):
                kw.update(partner_id=self.par_pk(row.idcpt.strip()))
                kw.update(account=vat.TradeTypes.sales.get_main_account())
            elif row.idctr == ('E'):
                kw.update(partner_id=self.par_pk(row.idcpt.strip()))
                kw.update(account=vat.TradeTypes.purchases.get_main_account())
            elif row.idctr == ('G'):
                kw.update(partner_id=self.par_pk(row.idcpt.strip()))
                kw.update(account=vat.TradeTypes.wages.get_main_account())
            elif row.idctr == ('S'):
                kw.update(partner_id=self.par_pk(row.idcpt.strip()))
                kw.update(account=vat.TradeTypes.clearings.get_main_account())
            else:
                a = Account.objects.get(ref=row.idcpt.strip())
                kw.update(account=a)
            dc = self.dc2lino(row.dc)
            kw.update(amount=dc.normalized_amount(mton(row.mont, ZERO)))
        except Exception as e:
            self.logger.warning("Failed to load FNL line %s from %s : %s", row,
                                kw, e)
            raise
        try:
            kw.update(match=row.match.strip())
            item = doc.add_voucher_item(**kw)
            # match = row.match.strip()
            # if match:
            #     lst = self.must_match.setdefault(match, [])
            #     lst.append((doc, item))
            #     # self.must_match.append((doc, item, match))
            return item
        except Exception as e:
            self.logger.warning("Failed to load FNL line %s from %s : %s", row,
                                kw, e)

    def load_ven(self, row, **kw):
        jnl, year, period, number = self.row2jnl(row)
        if period is None:
            return
        if jnl is None:
            self.logger.info("No journal %s (%s)", row.idjnl, row)
            return
        assert period.year == year
        kw.update(fiscal_year=period.year)
        kw.update(accounting_period=period)
        kw.update(journal=jnl)
        kw.update(number=number)
        kw.update(vat_regime=vat_regime(row.idreg.strip()))

        idmfc = row.idmfc.strip()
        if idmfc:
            pt = PaymentTerm.get_by_ref(idmfc, None)
            if pt is None:
                pt = PaymentTerm(ref=idmfc, name=idmfc)
                yield pt
            kw.update(payment_term=pt)

        # kw.update(id=pk)
        partner = self.get_customer(row.idpar)
        if partner is None:
            self.logger.warning("No partner id {0} in {1}".format(row.idpar, row))
            return
        else:
            kw.update(partner=partner)
        if jnl.trade_type.name == 'sales':
            # kw.update(imode=self.DIM)
            if (layout := getattr(row, 'layout', '').strip()):
                pt = trading.PaperType.objects.get(ref=layout2pt(layout))
                kw.update(paper_type=pt)
            if row.remise and row.remise.isdigit():
                kw.update(default_discount=qton(row.remise.strip()))
                # self.logger.warning("Ignoring discount %s in %s", row.remise, row)
                # kw.update(discount=mton(row.remise))
        elif jnl.trade_type.name == 'purchases':
            pass
            # kw.update(partner=contacts.Partner.objects.get(
            #     pk=self.par_pk(row.idpar)))
            # partner=contacts.Partner.objects.get(pk=self.par_pk(row.idpar))
        else:
            raise Exception("Unknown TradeType %r" % jnl.trade_type)
        if (model := dd.get_plugin_setting('accounting', 'project_model', None)):
            if (idprj := row.idprj.strip()):
                idprj = int(idprj)
                if model.objects.filter(pk=idprj).exists():
                    kw.update(project_id=int(idprj))
                else:
                    self.logger.warning("Invalid IdPrj %s in %s", idprj, row)
                # TypeError: Problem installing fixture 'tim2lino.py': VatProductInvoice() got unexpected keyword arguments: 'project_id'
        kw.update(entry_date=datevalue(row.date))
        kw.update(voucher_date=datevalue(row.date))
        kw.update(user=self.get_user(row.auteur))
        kw.update(total_base=mton(row.montr))
        kw.update(total_vat=mton(row.montt))
        kw.update(match=row.match.strip())
        model = jnl.get_doc_model()
        doc = self.get_or_save(row, model, **kw)
        # doc = jnl.create_voucher(**kw)
        # doc.partner = partner
        # doc.full_clean()
        # doc.save()
        # self.VENDICT[(jnl.ref, year.ref, number)] = doc
        if row.etat == self.etat_registered:
            checkdict = {k: kw[k] for k in ('total_base', 'total_vat')}
            self.must_register.append((doc, checkdict))
        # match = row.match.strip()
        # if match:
        #     lst = self.must_match.setdefault(match, [])
        #     lst.append((doc, doc))
        #     # self.must_match.append((doc, doc, match))
        return doc

    def load_vnl(self, row, **kw):
        jnl, year, period, number = self.row2jnl(row)
        assert period is None
        if jnl is None:
            return
        if year is None:
            return
        try:
            doc = jnl.get_voucher(year, number)
        except jnl.get_doc_model().DoesNotExist:
            msg = f"VNL {jnl.ref} without document {number} in {year.ref}"
            self.logger.warning(msg)
            return
        kw.update(seqno=int(row.line.strip()))
        idart = row.idart.strip()
        if isinstance(doc, trading.VatProductInvoice):
            if (plaque := getattr(row, 'plaque', '').strip()):
                PartnerAsset = rt.models.assets.PartnerAsset
                ass = PartnerAsset.objects.filter(
                    name=plaque, partner=doc.partner).first()
                if ass is None:
                    ass = PartnerAsset(partner=doc.partner, name=plaque)
                    ass.full_clean()
                    ass.save()
                kw.update(invoiceable=ass)
            if row.code in {'A', 'F'}:
                kw.update(product=products.Product.get_by_ref(idart))
            elif row.code == 'G':
                a = self.vnlg2product(row)
                if a is not None:
                    kw.update(product=a)
                else:
                    msg = f"Ignore invalid account {row.idart} in {row}"
                    self.logger.warning(msg)
            elif row.code == 'T':
                prd = products.Product.get_by_ref(idart)
                if not prd.subtotal:
                    prd.subtotal = True
                    prd.full_clean()
                    prd.save()
                kw.update(product=prd)
            elif row.code == 'R':
                pass
            else:
                msg = f"Ignore invalid code {row.code} in {row}"
                self.logger.warning(msg)
            try:
                kw.update(unit_price=mtonu(row.prixu))
            except Exception:
                msg = "VNL {} ignore invalid unit_price {}".format(
                    [jnl.ref, year.ref, number], row.prixu)
                self.logger.warning(msg)
            qty = qton(row.qte)
            # fld = doc.items.model._meta.get_field('qty')
            qty_fld = trading.InvoiceItem._meta.get_field('qty')
            try:
                qty = qty_fld.to_python(qty)
                kw.update(qty=qty)
            except Exception:
                msg = "VNL {} ignore invalid qty {}".format(
                    [jnl.ref, year.ref, number], qty)
                self.logger.warning(msg)
        elif isinstance(doc, vat.VatAccountInvoice):
            if row.code == 'G':
                kw.update(account=self.get_or_save(row, Account, ref=idart))
        kw.update(title=row.desig.strip())
        vc = tax2vat(row.idtax)
        kw.update(vat_class=vc)
        mb = mtonu(row.cmont)
        mv = mtonu(row.montt)
        kw.update(total_base=mb)
        kw.update(total_vat=mv)
        if mb is not None and mv is not None:
            kw.update(total_incl=mb + mv)
        # kw.update(qty=row.idtax.strip())
        # kw.update(qty=row.montt.strip())
        # kw.update(qty=row.attrib.strip())
        # kw.update(date=row.date)

        # check whether we need a vat rule
        # if mv and mb:
        #     vatrule = dict(vat_class=vc, vat_regime=doc.vat_regime)
        #     vatrule.update(
        #         country=doc.partner.country or
        #         dd.plugins.countries.get_my_country())
        #     try:
        #         VatRule.objects.get(**vatrule)
        #     except VatRule.DoesNotExist:
        #         vatrule.update(rate=myround(mv / mb))
        #         yield VatRule(**vatrule)
        model = doc.__class__.items.rel.related_model
        if model is trading.InvoiceItem and not kw.get('qty', None):
            if (total_incl := kw.get('total_incl', None)):
                if kw['title'] == "Rabatt" and total_incl < 0:
                    if (obj := self.last_invoice_line) is not None:
                        if obj.voucher == doc and obj.product == kw.get('product', None):
                            obj.discount_amount = -round(total_incl, 2)
                            obj.total_incl += total_incl
                            obj.total_base += kw['total_base']
                            obj.total_vat += kw['total_vat']
                            # obj.discount_amount_changed()
                            yield obj
                            return

        try:
            kw.update(voucher=doc)
            obj = self.get_or_save(row, model, **kw)
            # obj = doc.add_voucher_item(**kw)
            self.last_invoice_line = obj
            yield obj

        except Exception as e:
            self.logger.warning("Failed to load VNL line %s from %s : %s", row,
                                kw, e)

    def vnlg2product(self, row):
        idart = row.idart.strip()
        p = self.sales_gen2art.get(idart)
        if p is None:
            qs = products.Product.objects.filter(sales_account__ref=idart)
            if qs.count() == 1:
                p = qs.first()
            else:
                acc = accounting.Account.get_by_ref(idart)
                p = products.Product(name=idart, sales_account=acc)
                p.full_clean()
                p.save()
            self.sales_gen2art[idart] = p
        return p

    # Countries already exist after initial_data, but their short_code is
    # needed as lookup field for Places.
    def load_nat(self, row):
        if not row['isocode'].strip():
            return
        try:
            country = Country.objects.get(isocode=row['isocode'].strip())
        except Country.DoesNotExist:
            country = Country(isocode=row['isocode'].strip())
            country.name = row['name'].strip()
        if row['idnat'].strip():
            country.short_code = row['idnat'].strip()
        return country

    def load_plz(self, row):
        pk = row.pays.strip()
        if not pk:
            return
        name = row.nom.strip() or row.cp.strip()
        if not name:
            return

        if False:  # severe
            country = Country.objects.get(isocode=self.short2iso(pk))
            # country = Country.objects.get(short_code=pk)
        else:
            try:
                country = Country.objects.get(isocode=self.short2iso(pk))
                # country = Country.objects.get(short_code=pk)
            except Country.DoesNotExist:
                self.logger.warning("Ignored PLZ %s (with invalid country %s)",
                                    row, pk)
                return
        zip_code = row['cp'].strip()
        # if Place.objects.filter(zip_code=zip_code, country=country).exists():
        #     self.logger.warning("Ignored PLZ %s (duplicate zip code %s-%s)", row,
        #                         country.isocode, zip_code)
        #     return

        kw = dict(
            zip_code=zip_code,
            name=name,
            country=country,
        )
        return self.get_or_save(row, Place, **kw)

    def load_par(self, row):
        kw = {}
        # kw.update(
        #     street2kw(join_words(
        #         row['RUE'],
        #         row['RUENUM'],
        #         row['RUEBTE'])))

        # the following code needs the top-level (possibly abstract)
        # models:
        from lino_xl.lib.contacts.models import Person, Company
        partner_models = (Person, Company)
        if dd.is_installed('households'):
            from lino_xl.lib.households.models import Household
            partner_models = (Person, Company, Household)

        pk = self.par_pk(row.idpar)
        if pk is None:
            self.logger.warning(
                "Ignore PAR record with invalid IdPar %r", row.idpar)
            return
        # self.logger.warning("20250424 IdPar is %r", row.idpar)

        self.store(kw, id=pk)

        cl = self.par_class(row)

        if cl is None:
            self.logger.warning("Ignored PAR record %s (IdPrt %r)" %
                                (row.idpar, row.idprt))
            return

        if issubclass(cl, partner_models):
            email = row.get('email', '').strip()
            if email and is_valid_email(email):
                self.store(kw, email=email)

        # if 'idreg' in row:
        if row.idreg:
            self.store(kw, vat_regime=vat_regime(row.idreg.strip()))

        # if 'idgen' in row:
        if row.idgen:
            self.store(kw, purchase_account=self.get_account(row.idgen))

        isocode = self.short2iso(row.pays.strip())

        if issubclass(cl, rt.models.contacts.Partner):
            language = isolang(row['langue'])

            if settings.SITE.get_language_info(language):
                self.store(kw, language=language)

            # if 'memo' in row:
            if row.memo:
                self.store(kw, remarks=self.dbfmemo(row.get('memo') or ''))

            if isocode:
                try:
                    country = Country.objects.get(isocode=isocode)
                except Country.DoesNotExist:
                    country = self.get_or_save(
                        row, Country, isocode=isocode, name=isocode)
                    # country.save()
                kw.update(country=country)

                zip_code = row['cp'].strip()
                if zip_code:
                    kw.update(zip_code=zip_code)
                    qs = Place.objects.filter(
                        country=country,
                        zip_code__exact=zip_code,
                    )
                    if qs.count() == 0:
                        city = self.get_or_save(
                            row, Place, zip_code=zip_code,
                            name=zip_code, country=country)
                        # city.save()
                        kw.update(city=city)
                    else:
                        kw.update(city=qs.first())
                        s = self.duplicate_zip_codes.get(country, set([]))
                        s.add(zip_code)

            self.store(
                kw,
                phone=row['tel'].strip(),
                fax=row['fax'].strip(),
                street=row['rue'].strip(),
                street_no=row['ruenum'],
                street_box=row['ruebte'].strip(),
            )

            # kw.update(street2kw(join_words(row['RUE'],
            # row['RUENUM'],row['RUEBTE'])))

        if dd.is_installed('peppol'):
            if dd.plugins.tim2lino.send_peppol_attr in row['attrib']:
                self.store(kw, send_peppol=True)

        if issubclass(cl, Company):
            # cl = Company
            self.store(
                kw,
                prefix=row['allo'].strip(),
                name=row.firme.strip() + ' ' + row.vorname,
            )
            # if isocode == "BE" and dd.is_installed('peppol'):
            #     self.store(kw, send_peppol=True)
            if dd.is_installed('vat'):
                # 20250420 The vat modules of stdnum don't have a format() function
                # vat_id = row['notva']
                # if (country := kw.get('country', None)) is None:
                #     self.logger.info(
                #         f"Ignore VAT id {vat_id} in unknown country for {row}")
                # elif (mod := country.get_stdnum_module('vat')) is not None:
                #     if mod.is_valid(vat_id):
                #         self.store(kw, vat_id=mod.format(vat_id))
                #     else:
                #         self.logger.info(f"Ignore invalid VAT id {vat_id} for {row}")
                # else:
                #     self.logger.info(f"No stdnum module for {country} in {row}")
                tmp = Company(
                    vat_id=row['notva'], country=kw.get('country', None))
                try:
                    tmp.vid_manager.sanitize()
                    self.store(kw, vat_id=tmp.vat_id)
                except ValidationError:
                    self.logger.info(
                        f"Ignoring invalid VAT id {row['notva']} for {row}")

                # from lino_xl.lib.vat.utils import is_valid_id
                # vat_id = row['notva']
                # if is_valid_id(vat_id):

        if issubclass(cl, Person):
            # self.store(kw, prefix=row.allo)
            # kw.update(**name2kw(self.decode_string(row.firme)))
            last_name = row.firme.strip()
            if row.name2.strip():
                last_name += '-' + row.name2.strip()
            self.store(
                kw,
                first_name=row['vorname'].strip(),
                last_name=last_name,
                # birth_date=row['gebdat'],
                title=row['allo'].strip(),
            )
            assert kw['first_name'] or kw['last_name']
            # depends on which dbf module is being used:
            # if 'sex' in row:
            if hasattr(row, 'sex'):
                # sex = row.get('sex', None)
                sex = row.sex
                self.store(kw, gender=convert_gender(sex))
        if dd.is_installed('households'):
            if issubclass(cl, Household):
                self.store(kw,
                           name=row.firme.strip() + ' ' + row.vorname.strip())
        if dd.is_installed('lists') and issubclass(cl, List):
            self.store(kw, designation=row.firme)

        if issubclass(cl, Created):
            if 'datcrea' in row:
                created = row.get('datcrea', None)
                if created:
                    created = datetime.datetime.combine(
                        created, datetime.time(0, 0, 0))
                    if settings.USE_TZ:
                        created = make_aware(created)
                    kw.update(created=created)

        try:
            obj = self.get_or_save(row, cl, **kw)
        except Exception:
            self.logger.warning("Failed to instantiate %s from %s", cl, kw)
            raise
        yield obj

        def compte2iban(s, **kw):
            a = s.split(':')
            if len(a) == 1:
                kw.update(iban=s)
            elif len(a) == 2:
                kw.update(bic=a[0])
                kw.update(iban=a[1])
            else:
                kw.update(iban=s)
            return kw

        if not dd.is_installed('sepa'):
            return

        compte1 = row['compte1'].strip()
        if compte1:
            obj.full_clean()
            obj.save()
            kw = compte2iban(compte1, partner=obj, primary=True)
            if kw['iban']:
                try:
                    yield self.get_or_save(row, sepa.Account, **kw)
                except ValidationError:
                    self.logger.warning("Ignored invalid PAR->Compte1 %r",
                                        compte1)

    def load_prj(self, row, **kw):
        pk = int(row.idprj.strip())
        kw.update(id=pk)
        model = dd.get_plugin_setting('accounting', 'project_model', None)
        if dd.is_installed('cars') and model.__name__ == 'Car':
            if not (brandref := row.marke.strip()):
                return
            Car = rt.models.cars.Car
            Brand = rt.models.cars.Brand
            # kw.update(designation=row.name.strip())
            if (brand := Brand.get_by_ref(brandref, None)) is None:
                brandname = CAR_BRANDS.get(brandref, brandref)
                brand = Brand(name=brandname, ref=brandref)
                brand.full_clean()
                brand.save()
            kw.update(pk=pk)
            kw.update(partner=self.get_customer(row.idpar))
            kw.update(model=row.modell.strip())
            kw.update(brand=brand)
            kw.update(license_plate=row.kennz.strip())
            return Car(**kw)
        raise Exception(f"20250707 Cannot import {row}")
        # if row.parent.strip():
        #     kw.update(parent_id=int(row.parent))
        # kw.update(name=row.name1.strip())
        # # if row.idpar.strip():
        # #     kw.update(partner_id=self.par_pk(row.idpar.strip()))
        #
        # kw.update(ref=row.seq.strip())
        # # kw.update(user=self.get_user(None))
        # desc = self.dbfmemo(row.abstract).strip() + '\n\n' + self.dbfmemo(
        #     row.body)
        # # kw.update(summary=self.dbfmemo(row.abstract))
        # kw.update(description=desc)
        # return tickets.Project(**kw)

    def load_pin(self, row, **kw):
        pk = int(row.idpin)
        kw.update(id=pk)
        if row.idprj.strip():
            kw.update(project_id=int(row.idprj))
            # kw.update(partner_id=PRJPAR.get(int(row.idprj),None))
        kw.update(summary=row.short.strip())
        kw.update(description=self.dbfmemo(row.memo))
        kw.update(state=ticket_state(row.idpns))
        kw.update(closed=row.closed)
        kw.update(created=row['date'])
        kw.update(modified=datetime.datetime.now())
        kw.update(reporter=self.get_user(row.idusr))
        return tickets.Ticket(**kw)
        # if row.idpar.strip():
        #     kw = dict(project=obj)
        #     kw.update(partner_id=self.par_pk(row.idpar))
        #     yield tickets.Sponsorship(**kw)

    def load_art(self, row, **kw):
        # try:
        #     pk = int(row.idart)
        # except ValueError as e:
        #     self.logger.warning("Ignored %s: %s", row, e)
        #     # return
        idart = row.idart.strip()
        if not idart:
            self.logger.warning("Ignored %s: ART->IdArt is empty", row)
            return
        kw.update(ref=idart)
        # if pk == 0:
        #     pk = 1000  # mysql doesn't accept value 0
        # kw.update(id=pk)
        self.babel2kw('name', 'name', row, kw)
        # self.logger.info("20140823 product %s", kw)
        kw.setdefault('name', idart)
        idcat = row.idcat.strip()
        if idcat == "A":
            kw.update(vat_class=VatClasses.reduced)
        elif idcat == "0":
            kw.update(vat_class=VatClasses.exempt)
        if (idgen := row.idgen.strip()):
            kw.update(sales_account=Account.get_by_ref(idgen, None))
        if dd.get_plugin_setting('accounting', 'has_purchases', False):
            if (idgen := row.idgene.strip()):
                kw.update(purchases_account=Account.get_by_ref(idgen, None))
        return self.get_or_save(row, products.Product, **kw)

    def create_users(self):
        self.ROOT = users.User.objects.filter(username="tim").first()
        if self.ROOT is None:
            self.ROOT = self.get_or_save(
                None, users.User, username='tim', first_name='tim', id=1,
                user_type=users.UserTypes.admin)
            self.ROOT.set_password(dd.plugins.users.demo_password)
            # if isinstance(self.ROOT, rt.models.contacts.Partner):
            #     self.ROOT.name = "tim"
            yield self.ROOT

    def get_user(self, idusr=None):
        return self.ROOT

    def objects(tim):

        self = tim

        yield self.create_users()

        # settings.SITE.loading_from_dump = True

        if False:
            self.DIM = trading.InvoicingMode(name='Default')
            yield self.DIM

        # yield trading.Invoice.create_journal('sales',
        #    chart=self.CHART,name="Verkaufsrechnungen",ref="VKR")
        # yield accounting.AccountInvoice.create_journal('purchases',
        #    chart=self.CHART,name="Einkaufsrechnungen",ref="EKR")
        # from lino.modlib.users import models as users
        # ROOT = users.User.objects.get(username='root')
        # DIM = trading.InvoicingMode.objects.get(name='Default')
        # yield tim.load_dbf('GEN', self.load_gen2group)

        yield tim.load_dbf('GEN', self.load_gen2account)

        yield dpy.FlushDeferredObjects

        self.after_gen_load()

        yield tim.load_dbf('ART')
        yield tim.load_dbf('JNL')

        yield dpy.FlushDeferredObjects

        self.after_jnl_load()

        # yield tim.load_dbf('NAT')
        yield tim.load_dbf('PLZ')
        yield tim.load_dbf('PAR')

        self.after_par_load()

        # from lino_xl.lib.vat.fixtures import euvatrates
        # yield euvatrates.objects()

        if dd.get_plugin_setting('accounting', 'project_model', None):
            settings.SITE.loading_from_dump = True
            yield tim.load_dbf('PRJ')
            yield dpy.FlushDeferredObjects
            settings.SITE.loading_from_dump = False

        if True:  # GET_THEM_ALL:

            yield tim.load_dbf('VEN')
            yield tim.load_dbf('VNL')

        if dd.plugins.tim2lino.import_finan:
            yield tim.load_dbf('FIN')
            yield tim.load_dbf('FNL')

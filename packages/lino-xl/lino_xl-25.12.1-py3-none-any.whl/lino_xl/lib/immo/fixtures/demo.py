# -*- coding: UTF-8 -*-
# Copyright 2024-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from commondata.demonames.streets import STREETS_IN_TALLINN
from lino.modlib.publisher.choicelists import PublishingStates, SpecialPages
from lino.utils.instantiator import make_if_needed
from lino.utils.mldbc import babel_named as named
from lino.utils.soup import MORE_MARKER
from lino import logger
from lino.api import dd, rt, _
from lino.utils import Cycler
from lorem import get_paragraph, get_sentence
from lino.modlib.uploads.mixins import make_uploaded_file
# from lino.modlib.publisher.models import create_special_pages

try:
    from lino_book import DEMO_DATA
except ImportError:
    DEMO_DATA = None


User = rt.models.users.User
Place = rt.models.countries.Place
PlaceTypes = rt.models.countries.PlaceTypes
Entry = rt.models.immo.Entry
EntryType = rt.models.immo.EntryType
DeedTypes = rt.models.immo.DeedTypes
Upload = rt.models.uploads.Upload
# if dd.plugins.publisher.with_trees:
#     Tree = rt.models.publisher.Tree
Page = rt.models.publisher.Page
Topic = rt.models.topics.Topic
Tag = rt.models.topics.Tag
Group = rt.models.groups.Group
Company = rt.models.contacts.Company
Album = rt.models.albums.Album
AlbumItem = rt.models.albums.AlbumItem


def entry_type(name):
    return EntryType(**dd.str2kw('designation', name))


def plain2rich(s):
    s = s.strip()
    if s.startswith("<"):
        return s
    s = "".join(["<p>{}</p>".format(p) for p in s.split("\n\n")])
    # return s.replace("\n", "<br/>")
    return s


THESES = []


def add(title_en, title_et, title_ru, body_en, body_et, body_ru):
    kwargs = dd.babelkw('title', en=title_en, et=title_et, ru=title_ru)
    kwargs.update(
        dd.babelkw('body', en=plain2rich(body_en), et=plain2rich(body_et), ru=plain2rich(body_ru)))
    THESES.append(kwargs)


add("Beautiful house in old town",
    "Ilus maja vanalinnas",
    "Красивый дом в старом городе",
    """Really beautiful.
""", """Tõesti ilus.
""", """Действительно красиво.
""")


LOREMS = []

for i in range(50):
    kwargs = dict(title=get_sentence(word_range=(3, 5)))
    kwargs.update(body=get_paragraph(count=5, sep="</p><p>"))
    LOREMS.append(kwargs)


TITLES = Cycler([
    "A silly title for this image.",
    "The quick brown fox jumps over the lazy dog.",
    "Ceci n'est pas une image.",
])

BEDROOMS = Cycler([1, 1, 2, 2, 3, 33, 4, 5])
BATHROOMS = Cycler([1, 1, 2, 1])
LIVABLE_SPACE = Cycler([20, 30, 43, 51])
PRICES = Cycler([79, 81, 95, 125, 230, 450])


def update(obj, **kwargs):
    for k, v in kwargs.items():
        setattr(obj, k, v)
    return obj


USERS = Cycler(User.objects.all())
# if dd.plugins.publisher.with_trees:
#     TREES = Cycler(Tree.objects.all())
persons = rt.models.contacts.Person.objects.all()
MENTORS = Cycler(persons[:2])
AUTHORS = Cycler(persons[2:])
assert len(MENTORS) > 0

STREETS = Cycler(STREETS_IN_TALLINN)


def objects():

    if DEMO_DATA is None:
        logger.info("No demo data because lino_book is not installed")
        return
    immo_uploads = []
    # "melancholy_house.jpg"
    for i, fn in enumerate([
        "1024px-Appartment_Typ_I_rot.jpeg",
        "Cottage_at_Stoke_Tye,_Suffolk_-_geograph.org.uk_-_230113.jpeg",
        "1024px-Modern_Appartment_Building_-_panoramio.jpeg",
        "1024px-Parsons_Kansas_-_Kitchen_before.jpeg",
        "512px-Luxury_Appartment_(30427940702).jpeg"
    ]):
        src = DEMO_DATA / "images" / fn
        file = make_uploaded_file(fn, src, dd.today(-i*2))
        obj = Upload(file=file, description=fn.replace('_', ' '))
        yield obj
        immo_uploads.append(obj)
    UPLOADS = Cycler(immo_uploads)

    yield (house := entry_type(_("House")))
    yield entry_type(_("Appartment"))
    yield entry_type(_("Land"))
    yield entry_type(_("Garage"))
    yield entry_type(_("Business"))

    ENTRYTYPES = Cycler(EntryType.objects.all())

    # for grp in Group.objects.exclude(ref=''):
    #     yield Tree(private=False, group=grp, ref=grp.ref)

    tallinn = Place.objects.get(name="Tallinn")
    harjumaa = Place.objects.get(name="Harju", type=PlaceTypes.county)

    def make_entry_and_co(**kwargs):
        user = USERS.pop()
        alb = Album(title=kw['title'], user=user)
        yield alb
        for j in range(alb.id % 4 + 1):
            yield AlbumItem(
                album=alb, upload=UPLOADS.pop(), title=TITLES.pop(), seqno=j)
        kwargs.update(deed_type=DeedTypes.sale)
        kwargs.update(user=user)
        street, linnaosa = STREETS.pop()
        kwargs.update(region=harjumaa)
        kwargs.update(city=tallinn)
        if linnaosa:
            try:
                kwargs.update(city=Place.objects.get(name=linnaosa, parent=tallinn))
            except (Place.DoesNotExist, Place.MultipleObjectsReturned):
                pass
        kwargs.update(street=street)
        kwargs.update(publishing_state=PublishingStates.published)
        kwargs.update(pub_date=dd.today(alb.id-50))
        kwargs.update(album=alb)
        kwargs.update(livable_space=LIVABLE_SPACE.pop())
        kwargs.update(bedrooms=BEDROOMS.pop())
        kwargs.update(bathrooms=BATHROOMS.pop())
        kwargs.update(sale_price=PRICES.pop())
        yield Entry(**kwargs)

    for kw in LOREMS:
        yield make_entry_and_co(entry_type=ENTRYTYPES.pop(), **kw)

    for kw in THESES:
        yield make_entry_and_co(entry_type=house, **kw)

    for pg in Page.objects.filter(special_page=SpecialPages.home):
        pg.body += "\n\n[show immo.LatestEntries]\n"
        yield pg

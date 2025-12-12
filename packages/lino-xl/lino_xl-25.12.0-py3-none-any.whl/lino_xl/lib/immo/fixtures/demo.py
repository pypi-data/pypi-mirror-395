# -*- coding: UTF-8 -*-
# Copyright 2024-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.modlib.publisher.choicelists import PublishingStates, SpecialPages
from lino.utils.instantiator import make_if_needed
from lino.utils.mldbc import babel_named as named
from lino.utils.soup import MORE_MARKER
from lino.api import dd, rt, _
from lino.utils import Cycler
from lorem import get_paragraph, get_sentence
# from lino.modlib.publisher.models import create_special_pages


User = rt.models.users.User
Place = rt.models.countries.Place
PlaceTypes = rt.models.countries.PlaceTypes
Entry = rt.models.immo.Entry
EntryType = rt.models.immo.EntryType
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


def add(title_et, title_en, title_ru, body_et, body_en, body_ru):
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
    kwargs = dict(title=get_sentence())
    kwargs.update(body=get_paragraph(count=5, sep="</p><p>"))
    LOREMS.append(kwargs)


TITLES = Cycler([
    "A silly title for this image.",
    "The quick brown fox jumps over the lazy dog.",
    "Ceci n'est pas une image.",
])


def update(obj, **kwargs):
    for k, v in kwargs.items():
        setattr(obj, k, v)
    return obj


USERS = Cycler(User.objects.all())
# if dd.plugins.publisher.with_trees:
#     TREES = Cycler(Tree.objects.all())
UPLOADS = Cycler(Upload.objects.filter(mimetype__endswith='jpg'))
persons = rt.models.contacts.Person.objects.all()
MENTORS = Cycler(persons[:2])
AUTHORS = Cycler(persons[2:])
assert len(MENTORS) > 0
if len(UPLOADS) == 0:
    mimetypes = {o.mimetype for o in Upload.objects.all()}
    raise Exception(f"20250929 No jpg uploads found {mimetypes}")


def objects():

    yield (house := entry_type(_("House")))
    yield entry_type(_("Appartment"))
    yield entry_type(_("Land"))
    yield entry_type(_("Garage"))
    yield entry_type(_("Business"))

    ENTRYTYPES = Cycler(EntryType.objects.all())

    # for grp in Group.objects.exclude(ref=''):
    #     yield Tree(private=False, group=grp, ref=grp.ref)

    def make_entry_and_co(**kwargs):
        e = Entry(**kwargs)
        user = USERS.pop()
        alb = Album(title=e.title, user=user)
        yield alb
        for j in range(alb.id % 4 + 1):
            yield AlbumItem(
                album=alb, upload=UPLOADS.pop(), title=TITLES.pop())

        e.user = user
        e.publishing_state = PublishingStates.published
        e.pub_date = dd.today(alb.id-50)
        e.album = alb
        yield e

    for kw in LOREMS:
        yield make_entry_and_co(entry_type=ENTRYTYPES.pop(), **kw)

    for kw in THESES:
        yield make_entry_and_co(entry_type=house, **kw)

    for pg in Page.objects.filter(special_page=SpecialPages.home):
        pg.body += "[show immo.LatestEntries]\n"
        yield pg

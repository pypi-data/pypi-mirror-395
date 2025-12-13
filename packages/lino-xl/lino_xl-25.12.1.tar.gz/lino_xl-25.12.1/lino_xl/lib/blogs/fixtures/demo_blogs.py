# -*- coding: UTF-8 -*-
# Copyright 2021-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime as dt
from pathlib import Path

from django.conf import settings
from django.utils import translation

from lino.api import rt, dd, _
from lino.core.gfks import gfk2lookup
from lino.utils.cycler import Cycler
from lino.modlib.uploads.mixins import make_uploaded_file

imgpath = Path(__file__).parent / "images"


def objects():
    # Entries = rt.models.blogs.Entries
    Entry = rt.models.blogs.Entry
    File = rt.models.uploads.Upload
    # Page = rt.models.publisher.Page
    Place = rt.models.countries.Place
    Country = rt.models.countries.Country
    Source = rt.models.sources.Source
    Author = rt.models.sources.Author
    License = rt.models.sources.License
    # PublishingStates = rt.models.publisher.PublishingStates

    # blog_body = _("This page is our blog.")
    # # for lng in settings.SITE.languages:
    # #     with translation.override(lng.django_code):
    # # blogger_roots[lng.django_code] = obj
    #
    # with translation.override('en'):
    #     kwargs = dict(title=_("Blog"))
    #     kwargs.update(body=blog_body)
    #     kwargs.update(parent=Page.objects.get(language="en", ref="index"))
    #     kwargs.update(filler='blogs.LatestEntries')
    #     kwargs.update(language="en")
    #     # kwargs.update(child_node_depth=1)
    #     if dd.is_installed("publisher"):
    #         kwargs.update(publishing_state='published')
    #     obj = Page(**kwargs)
    #     yield obj
    # # blog_root = obj

    # ar = rt.login(username='robin')
    # ar = Entries.create_request(parent=ar)
    # demo_date = settings.SITE.the_demo_date
    today = settings.SITE.today

    def make_file(name, description, source):
        file_made = make_uploaded_file(name, imgpath / name, today(-3))
        return File(file=file_made, description=description, source=source)

    # Group = rt.models.groups.Group
    # groups = Group.objects.all()
    # GROUPS = Cycler(groups)
    # if dd.plugins.publisher.with_trees:
    #     trees = rt.models.publisher.Tree.objects.all()
    #     TREES = Cycler(trees)
    #     if len(TREES) == 0:
    #         raise Exception("20250828 no trees")

    # USERS = {
    #     tree: Cycler([m.user for m in tree.group.members.all()])
    #     for tree in trees
    # }
    USERS = Cycler(rt.models.users.User.objects.all())

    def prepare_entry(**kwargs):
        if dd.is_installed("publisher"):
            kwargs.update(publishing_state='published')
        # if dd.plugins.publisher.with_trees:
        #     kwargs.update(publisher_tree=TREES.pop())
        # kwargs.update(parent=blog_root)
        # if dd.is_installed('groups'):
        #     grp = GROUPS.pop()
        #     kwargs.update(group=grp)
        # kwargs.update(user=USERS[tree].pop())
        kwargs.update(user=USERS.pop())
        return Entry(**kwargs)
        # obj = Entries.create_instance(ar, **kwargs)
        # Entries.after_create_instance(obj, ar)
        # obj.before_ui_save(ar, None)
        # return obj

    title = "Hello world"
    body = "<p>This is my first blog entry. It is really short.</p>"
    yield prepare_entry(title=title, body=body, pub_date=today(-4))

    ccbysa = License.objects.get(designation="Creative Commons BY SA")

    yield (johnstone := Author(last_name="Johnstone", first_name="Christine"))
    yield (source := Source(
        title="Crossroads, Kilham West Field",
        author=johnstone,
        license=ccbysa,
        url="https://commons.wikimedia.org/wiki/File:Crossroads,_Kilham_West_Field_-_geograph.org.uk_-_2097672.jpg"))

    img = make_file("crossroads.jpg",
                    "Crossroads, Kilham West Field - geograph.org.uk - 2097672", source)
    yield img

    title = "At the fork of the cross roads"
    cmd = '[include upload:{}]'.format(img.pk)
    body = """<div><p>{}Let's choose one or the other of the either roads (or NOT)!</p><p>And the hesitation, does it comes rarely(?), Nooo!, we are very frequently and suddenly put to situations where we must choose between roads.</p><p>Of course, how to choose and what to choose are the questions. But did we ever ask 'why?' But of course it depends on the context, let's not give it a context, let's talk abstract. 'Why?' is the question. Maybe to be like a stoic or something, not sure!</p><p>The advice from a stoic would be to not choose but just hang around at the fork and not think about it at all, just try to be at peace, the hesitations aside.</p><p>But no we have to make a choice, why? because, the world isn't going to wait for us! We have to make a choice and move along with the world, fast forward. We can deal with whatever comes.</p><p>OTOH! sometimes it's not worth moving along, sometimes we can just sit at the fork and think through things, cars, engines, birds, rocket ships or the stars, really, anything at all, because it doesn't matter what about, anything will do, why not! thinking is fun, just living the fantasy that we forgot to live, the fantasies that engulped us when we were children, make a peace out of the fork, build a house on the fork, a house of fantasies, a house of the colors from the river on the night sky, a house of wind and the smell of dirt or grass, a house on no where, wouldn't that be fun!</p><p>Here again comes the 'but', the other 'but', that is, you start to hear a calling from one of the roads, it's a call for you to continue along and at this point even though you are sure of the choice you need to make, it's not really a choice anymore, it has become the destiny, this is the path of your life, but you cannot make the choice, you cannot leave the fork, the house of no where! You have already fallen in love with the fork and the house, so why bother!</p><p>This clinging nature to things is going to be the end of you. You wanted to be free, to live a life of a free spirit, and you always forget to be free, you always forget to think, you always forget to keep the fantasy alive, you always forget that wherever you are you can wrap yourself around with the house, because the house is of nowhere and you are always at the nowhere unless you make it a somewhere. Remember the difference between a nowhere and a somewhere, only then you will be able to not forget.</p><p>On the path of becoming a stoic.</p></div>""".format(
        cmd)

    yield prepare_entry(title=title, body=body, pub_date=today())

    yield (harper := Author(last_name="Harper", first_name="Derek"))
    yield (source := Source(
        author=harper,
        license=ccbysa,
        title="Haunted House - geograph.org.uk - 6141456",
        url="https://commons.wikimedia.org/wiki/File:Haunted_House_-_geograph.org.uk_-_6141456.jpg"))

    img = make_file("melancholy_house.jpg", "The House", source)
    yield img
    cmd = '[include upload:{}]'.format(img.pk)
    title = "Melancholy House"
    body = """<div><p>{}It was cursed and the occupant knew about the unholy nature of it. They wanted to get away from it but it never did allow them to do so until they were consumed by the unholy spirit of it. When they got out, all that remained of them was an empty shell. Sometimes you can heaeit screaming as it devours of the occupant, i think it wants to become the occupant, it's a jealous beast, and the scream comes from the fact that - as the beast grows from the occupant it also grows in melancholy radiated from the occupant.</p></div>""".format(
        cmd)

    melancholy_house = prepare_entry(title=title,
                                     body=body,
                                     pub_date=today(-1))
    yield melancholy_house
    # melancholy_house.after_ui_save(ar, None)

    us = Country.objects.get(isocode="US")
    yield (portland := Place(name="Portland, Oregon", country=us))
    yield (bohlman := Author(last_name="Bohlman",
                             first_name="Herman Theodore", birth_date="15.04.1872",
                             birth_place=portland, death_place=portland))
    yield (source := Source(
        title="People talking (3945337913).jpg",
        url="https://commons.wikimedia.org/wiki/File:People_talking_(3945337913).jpg",
        license=ccbysa,
        author=bohlman))
    # "2017 Gerd Altmann (pixabay.com user@geralt)"
    img = make_file("bleeding_words.jpg", "Bleeding Words", source)
    yield img
    cmd = '[include upload:{}]'.format(img.pk)
    title = "A little too much to talk"
    body = """<div><p>{}We want to be quiet. Say to mine-self, let's be quiet
and try to be quiet. But does that ever stops us from talking. It seems
there's a little too many ways of talking. So, the talking never stops. Now
a days everybody's talking and everybody's listening. Now we ask mine-self,
what does that has to do with us(?)! in wonder!!!! So what everybody's
talking! Let them talk but let us be quiet! But the thought, it just a
thought, like so many other thoughts, one thought among unimaginably many
thoughts, so it remains a thought, and we never really stop from being
talking. Because this thought of being quiet has no significance at all
among all those uncountably many thoughts. So, the world is living inside of
us it seems, the whole universe is living inside of us. We cannot ignore the
resemblence that this living universe has with the universe outside. They
are both the same. Yogic or Stoic, where are the happinesses has gone where
have the peace gone. It's all just empty words, empty thoughts, non of it
has any significance. There's no peace on the inside nor on the outside to
have the courage to give any weight to these thoughts or the words. We don't
buy words anymore, we only buy junks because we all have become junkies. We
have it all and at the same time nothing at all.</p><p>What are
you spreading, happiness or sadness? Why do you ask? Why should it matter
what I am spreading? You might say for the betterment of the human race. Oh
okay! Then what happened to the junkies(?), is my
question.</p><p>Yes, the peace, it has come only to disappear
again. Now the eyes are shining bright only to become dry again. It a
terbulant universe, the one on the inside, and the bandwidth of the spectras
seems infinite, so many colors and the terbulance, every instance is a new
color, only there's the lack of a single color that you might stare into in
admire.</p><p>Also, they never end.</p></div>""".format(cmd)

    yield prepare_entry(title=title, body=body, pub_date=today(-2))

    yield (source := Source(url="https://en.wikipedia.org/wiki/History_of_PDF"))
    img = make_file("History_of_PDF.pdf", "History of PDF", source)
    yield img
    cmd = "[include upload:{}]".format(img.pk)
    title = "A PDF file"
    body = """<p>Here is a PDF file : {}</p>
    <p>It was exported from the Wikipedia article about the
    <a href="https://en.wikipedia.org/wiki/History_of_PDF">History of PDF</a>.
    </p>""".format(cmd)
    yield prepare_entry(title=title, body=body, pub_date=today(-3))

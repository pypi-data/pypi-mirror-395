# -*- coding: UTF-8 -*-
# Copyright 2013-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from lino.utils.choosers import check_for_chooser

from etgen import html as xghtml
from django.db import models
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.contrib.contenttypes.models import ContentType

from lino.core.gfks import gfk2lookup
from lino.core import constants
from lino.utils.html import E
from lino.api import dd, rt, gettext
from lino.utils import join_elems
from lino.core.fields import TableRow
from lino.modlib.users.mixins import My
from lino.modlib.gfks.fields import GenericForeignKeyIdField

from .roles import PollsUser, PollsStaff
from .utils import PollStates

# Whether to use the new feature. When the feature will work, we'll remove this
# option again. As long as it does not work we use the old behaviour when
# running the test suite.
USE_GFK_CHOICE = False


class ChoiceSets(dd.Table):
    required_roles = dd.login_required(PollsStaff)
    model = 'polls.ChoiceSet'
    detail_layout = """
    name choice_type
    ChoicesBySet
    """
    # insert_layout = """
    # id
    # name
    # """


class Choices(dd.Table):
    model = 'polls.Choice'
    required_roles = dd.login_required(PollsStaff)


class ChoicesBySet(Choices):
    master_key = 'choiceset'
    # required_roles = dd.login_required()


class PollDetail(dd.DetailLayout):
    main = "general results"

    general = dd.Panel("""
    ref title workflow_buttons
    details
    default_choiceset default_multiple_choices
    polls.QuestionsByPoll
    """, label=_("General"))

    results = dd.Panel("""
    id user created modified state
    polls.ResponsesByPoll
    # result
    PollResult
    """, label=_("Results"))


class Polls(dd.Table):
    required_roles = dd.login_required(PollsUser)
    model = 'polls.Poll'
    column_names = 'ref title user state *'
    detail_layout = PollDetail()
    insert_layout = dd.InsertLayout("""
    ref title
    default_choiceset default_multiple_choices
    questions_to_add
    """, window_size=(60, 15))


class AllPolls(Polls):
    required_roles = dd.login_required(PollsStaff)
    column_names = 'id ref title user state *'


class MyPolls(My, Polls):
    """Show all polls whose author I am."""
    column_names = 'ref title state *'


class Questions(dd.Table):
    required_roles = dd.login_required(PollsStaff)
    model = 'polls.Question'
    column_names = "seqno poll number title choiceset is_heading *"
    detail_layout = """
    poll number is_heading choiceset multiple_choices
    title
    details
    AnswersByQuestion
    """
    order_by = ['poll', 'seqno']


class QuestionsByPoll(Questions):
    required_roles = dd.login_required(PollsUser)
    master_key = 'poll'
    column_names = 'seqno number title:50 is_heading *'
    auto_fit_column_widths = True
    stay_in_grid = True


class ResponseDetail(dd.DetailLayout):
    main = "answers more preview"
    answers = dd.Panel("""
    poll partner date workflow_buttons
    polls.AnswersByResponseEditor
    """,
                       label=_("General"))
    more = dd.Panel("""
    user state
    remark
    """, label=_("More"))
    preview = dd.Panel("""
    polls.AnswersByResponsePrint
    """,
                       label=_("Preview"))


class Responses(dd.Table):
    required_roles = dd.login_required(PollsUser)
    model = 'polls.Response'
    detail_layout = ResponseDetail()
    insert_layout = """
    user date
    poll
    """


class AllResponses(Responses):
    required_roles = dd.login_required(PollsStaff)


class MyResponses(My, Responses):
    column_names = 'detail_link date state remark *'


class ResponsesByPoll(Responses):
    master_key = 'poll'
    column_names = 'date user state partner remark *'


class ResponsesByPartner(Responses):
    master_key = 'partner'
    column_names = 'date user state remark *'
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}

    @classmethod
    def get_table_summary(self, ar):
        obj = ar.master_instance
        if obj is None:
            return

        Poll = rt.models.polls.Poll
        Response = rt.models.polls.Response

        visible_polls = Poll.objects.filter(
            state__in=(PollStates.active, PollStates.closed)).order_by('ref')

        qs = Response.objects.filter(partner=obj).order_by('date')
        polls_responses = {}
        for resp in qs:
            polls_responses.setdefault(resp.poll.pk, []).append(resp)

        items = []
        for poll in visible_polls:
            iar = self.insert_action.request_from(ar,
                                                  obj,
                                                  known_values=dict(poll=poll))
            elems = [str(poll), ' : ']
            responses = polls_responses.get(poll.pk, [])
            elems += join_elems(
                [ar.obj2html(r, dd.fds(r.date)) for r in responses], sep=', ')
            if poll.state == PollStates.active:
                elems += [' ', iar.ar2button()]
                # elems += [' ', iar.insert_button()]
            items.append(E.li(*elems))
        return E.div(E.ul(*items))


class AnswerChoices(dd.Table):
    required_roles = dd.login_required(PollsStaff)
    model = 'polls.AnswerChoice'


class AnswerChoicesByResponse(AnswerChoices):
    master_key = "response"
    column_names = "question choice_type choice_id *"


class AnswerRemarks(dd.Table):
    required_roles = dd.login_required(PollsUser)
    model = 'polls.AnswerRemark'

    detail_layout = dd.DetailLayout("""
    remark
    response question
    """, window_size=(60, 10))

    insert_layout = dd.InsertLayout("""
    remark
    response question
    """, window_size=(60, 10), hidden_elements={'response', 'question'})

    stay_in_grid = True

    # def disabled_fields(self, ar):
    #     return super().disabled_fields(ar) | {'response', 'question'}


class AnswerRemarksByAnswer(AnswerRemarks):
    use_as_default_table = False
    hide_top_toolbar = True
    hide_navigator = True


class AllAnswerRemarks(AnswerRemarks):
    required_roles = dd.login_required(PollsStaff)


class AnswerRemarkField(dd.VirtualField):
    editable = True

    def __init__(self):
        t = models.TextField(_("My remark"), blank=True)
        # dd.VirtualField.__init__(self, t, None)
        super().__init__(t, None)

    def set_value_in_object(self, ar, obj, value):
        # ~ e = self.get_entry_from_answer(obj)
        if not isinstance(obj, AnswersByResponseRow):
            raise Exception("{} is not AnswersByResponseRow".format(
                obj.__class__))
        obj.remark.remark = value
        obj.remark.save()

    def value_from_object(self, obj, ar):
        if not isinstance(obj, AnswersByResponseRow):
            raise Exception("{} is not AnswersByResponseRow".format(
                obj.__class__))
        # ~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        # ~ e = self.get_entry_from_answer(obj)
        return obj.remark.remark


class AnswerChoiceField(dd.VirtualField):
    # used only when USE_GFK_CHOICE
    editable = True

    def __init__(self, type_field):
        t = GenericForeignKeyIdField(type_field, verbose_name=_("Answer"))
        super().__init__(t, None)

    def set_value_in_object(self, ar, obj, value):
        ac, _ = rt.models.polls.AnswerChoice.objects.get_or_create(
            question=obj.question, response=obj.response)
        ac.choice_id = value
        ac.save()

    def value_from_object(self, obj, ar=None):
        return getattr(obj.choices.first(), "choice", None)


class AnswersByResponseRow(TableRow):

    FORWARD_TO_QUESTION = ("full_clean", "after_ui_save", "disable_delete",
                           "save_new_instance", "save_watched_instance",
                           "delete_instance")

    def __init__(self, response, question):
        AnswerRemark = rt.models.polls.AnswerRemark
        AnswerChoice = rt.models.polls.AnswerChoice

        self.response = response
        self.question = question
        # if question is None or question.choiceset is None:
        #     self.choice_type = None
        # else:
        #     self.choice_type = question.choiceset.choice_type
        # Needed by AnswersByResponse.get_row_by_pk
        self.pk = self.id = question.pk
        try:
            self.remark = AnswerRemark.objects.get(question=question,
                                                   response=response)
        except AnswerRemark.DoesNotExist:
            self.remark = AnswerRemark(question=question, response=response)

        self.choices = AnswerChoice.objects.filter(question=question,
                                                   response=response)
        for k in self.FORWARD_TO_QUESTION:
            setattr(self, k, getattr(question, k))
            # setattr(self, k, getattr(self.remark, k))

    def __str__(self):
        if self.choices.count() == 0:
            return str(_("N/A"))
        return ', '.join([str(ac.choice) for ac in self.choices])

    def as_summary_item(self, ar, text=None):
        # needed by detail_link
        return str(self)

    def get_question_html(obj, ar):
        if obj.question.number:
            txt = obj.question.NUMBERED_TITLE_FORMAT % (obj.question.number,
                                                        obj.question.title)
        else:
            txt = obj.question.title

        attrs = {}
        if obj.question.details:
            attrs.update(title=obj.question.details)
        if obj.question.is_heading:
            txt = E.b(txt, **attrs)
        return E.span(txt, **attrs)


class AnswersByResponseBase(dd.VirtualTable):
    master = 'polls.Response'
    model = AnswersByResponseRow

    @classmethod
    def get_data_rows(self, ar):
        response = ar.master_instance
        if response is None:
            return
        for q in rt.models.polls.Question.objects.filter(poll=response.poll):
            yield AnswersByResponseRow(response, q)

    @classmethod
    def get_pk_field(self):
        return rt.models.polls.Question._meta.pk

    @classmethod
    def get_row_by_pk(self, ar, pk):
        response = ar.master_instance
        # ~ if response is None: return
        q = rt.models.polls.Question.objects.get(pk=pk)
        return AnswersByResponseRow(response, q)

    @classmethod
    def disable_delete(self, obj, ar):
        return "Not deletable"

    @dd.displayfield(_("ID"))
    def question_id(self, obj, ar):
        return obj.question.pk

    @dd.displayfield(_("Question"))
    def question(self, obj, ar):
        return ar.html_text(obj.get_question_html(ar))


class AnswersByResponseEditor(AnswersByResponseBase):
    label = _("Answers")
    variable_row_height = True
    auto_fit_column_widths = True
    editable = True

    # column_names = 'question:30 answer_buttons:20 answer:20 remark:20 *'
    answer = AnswerChoiceField('choice_type')

    if USE_GFK_CHOICE:
        column_names = 'question:40 answer:30 remark:20 *'
        # answer = AnswerChoiceField('choice_type')
    else:
        allow_create = False
        allow_delete = False
        column_names = 'question:40 answer_buttons:30 *'
        default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}

    remark = AnswerRemarkField()

    @dd.chooser()
    def answer_choices(cls, question_id):
        if question_id is None:
            # print("20250511 question is None")
            return rt.models.polls.Choice.objects.none()
            # return [[0, "20250511 question is None"]]
        question = rt.models.polls.Question.objects.get(pk=question_id)
        # print(f"20250511 question is {repr(question)}")
        cs = question.get_choiceset()
        ct = cs.choice_type
        if ct is None or ct.model_class() is rt.models.polls.Choice:
            return rt.models.polls.Choice.objects.filter(choiceset=cs)
        return ct.model_class().objects.all()

    @classmethod
    def get_table_summary(self, ar):
        response = ar.master_instance
        if response is None:
            return
        if response.poll_id is None:
            return
        AnswerRemarks = rt.models.polls.AnswerRemarksByAnswer
        all_responses = rt.models.polls.Response.objects.filter(
            poll=response.poll).order_by('date')
        if response.partner:
            all_responses = all_responses.filter(partner=response.partner)
        else:
            all_responses = all_responses.filter(user=response.user)
        ht = xghtml.Table()
        ht.attrib.update(cellspacing="5px", bgcolor="#ffffff", width="100%")
        cellattrs = dict(align="left", valign="top", bgcolor="#eeeeee")
        headers = [str(_("Question"))]
        if all_responses.count() == 1:
            headers.append(gettext("Answer"))
        else:
            for r in all_responses:
                if r == response:
                    headers.append(dd.fds(r.date))
                else:
                    headers.append(ar.obj2html(r, dd.fds(r.date)))
        ht.add_header_row(*headers, **cellattrs)
        ar.master_instance = response  # must set it because
        # get_data_rows() needs it.
        # 20151211
        # editable = Responses.update_action.request_from(ar).get_permission(
        #     response)
        sar = Responses.update_action.request_from(ar)
        sar.selected_rows = [response]
        editable = sar.get_permission()
        # editable = insert.get_permission(response)
        kv = dict(response=response)
        insert = AnswerRemarks.insert_action.request_from(ar, known_values=kv)
        detail = AnswerRemarks.detail_action.request_from(ar)
        for answer in self.get_data_rows(ar):
            cells = [self.question.value_from_object(answer, ar)]
            for r in all_responses:
                if editable and r == response:
                    items = [self.answer_buttons.value_from_object(answer, ar)]
                    if answer.remark.remark:
                        items += [E.br(), answer.remark.remark]
                    # if answer.remark.pk:
                    #     detail.clear_cached_status()
                    #     detail.known_values.update(question=answer.question)
                    #     items += [
                    #         ' ',
                    #         detail.ar2button(answer.remark,
                    #                          _("Remark"),
                    #                          icon_name=None)
                    #     ]
                    #     # ar.obj2html(answer.remark, _("Remark"))]
                    # else:
                    #     insert.clear_cached_status()
                    #     insert.known_values.update(question=answer.question)
                    #     btn = insert.ar2button(answer.remark,
                    #                            _("Remark"),
                    #                            icon_name=None)
                    #     # sar = RemarksByAnswer.request_from(ar, answer)
                    #     # btn = sar.insert_button(_("Remark"), icon_name=None)
                    #     items += [" (", btn, ")"]

                else:
                    other_answer = AnswersByResponseRow(r, answer.question)
                    items = [str(other_answer)]
                    if other_answer.remark.remark:
                        items += [E.br(), answer.remark.remark]
                cells.append(E.p(*items))
            ht.add_body_row(*cells, **cellattrs)

        return ar.html_text(ht.as_element())

    @dd.htmlbox(_("Choose answer"))
    def answer_combo(self, obj, ar):
        # Experimental approach, not finished.
        # Choice = rt.models.polls.Choice
        cs = obj.question.get_choiceset()
        if cs is None:
            return None
        if cs.choice_type is None:
            ModelClass = rt.models.polls.Choice
        else:
            ModelClass = cs.choice_type.model_class()
        tbl = ModelClass.get_default_table()
        # if ModelClass == Choice:
        #     qs = cs.choices.all()
        # else:
        #     preview_limit = tbl.preview_limit
        #     qs = ModelClass.objects.all()[:preview_limit]
        input = E.input(id=f"choice_choiceset_{cs.pk}", list=f"choiceset_{cs.pk}",
                        onfocus=f"onChoiceSetInputFocus({cs.pk}, '{tbl.actor_id}')",
                        onchange=f"onChoiceSetInputChange(event, {cs.pk}, '{tbl.actor_id}')")
        # options = [E.option(str(obj), value=str(obj.pk)) for obj in qs]
        # datalist = E.datalist(*options, id=f"choiceset_{cs.pk}")
        datalist = E.datalist(id=f"choiceset_{cs.pk}")
        return E.span(input, datalist)

    @dd.displayfield(_("My answer"))
    def answer_buttons(self, obj, ar):
        # assert isinstance(obj, rt.models.polls.Answer)
        # print(20250724, obj.__class__)
        cs = obj.question.get_choiceset()
        if cs is None:
            return ''

        elems = []
        toggle_choice = obj.response.toggle_choice.request_from(ar)
        set_answer = obj.response.set_answer.request_from(ar)
        # print(20170731, sar.is_on_main_actor)
        if not toggle_choice.get_permission():
            return str(obj)

        AnswerChoice = rt.models.polls.AnswerChoice
        Choice = rt.models.polls.Choice

        if cs.choice_type is None or cs.choice_type.model_class() == Choice:
            pv = dict(question=obj.question)
            for c in cs.choices.all():
                # pv.update()
                text = str(c)
                qs = AnswerChoice.objects.filter(
                    response=obj.response,
                    **pv, **gfk2lookup(AnswerChoice.choice, c))
                if qs.count() == 1:
                    text = [E.b('[', text, ']')]
                elif qs.count() == 0:
                    pass
                else:
                    raise Exception("Oops: %s returned %d rows." %
                                    (qs.query, qs.count()))
                toggle_choice.set_action_param_values(
                    choice_id=c.id,
                    choice_type=ContentType.objects.get_for_model(Choice), **pv)
                e = toggle_choice.ar2button(
                    obj.response, text, style="text-decoration:none")
                elems.append(e)
        else:
            for ac in AnswerChoice.objects.filter(
                    question=obj.question, response=obj.response):
                # print(20250724, ac.choice)
                elems.append(str(ac.choice))

        pv = dict(question=obj.question, choice_type=cs.choice_type)
        set_answer.set_action_param_values(**pv)
        text = f"({gettext('Remark')})"
        e = set_answer.ar2button(
            obj.response, text, style="text-decoration:none")
        elems.append(e)

        return ar.html_text(E.span(*join_elems(elems)))


class AnswersByResponsePrint(AnswersByResponseBase):
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    column_names = 'question *'

    @classmethod
    def get_table_summary(self, ar):
        response = ar.master_instance
        if response is None:
            return
        if response.poll_id is None:
            return
        items = []
        for obj in self.get_data_rows(ar):
            if len(obj.remark.remark) == 0 and obj.choices.count() == 0:
                continue
            chunks = [obj.get_question_html(ar), " — "]  # unicode em dash
            chunks += [str(ac.choice) for ac in obj.choices]
            if obj.remark.remark:
                chunks.append(" {}".format(obj.remark.remark))
            items.append(E.li(*chunks))

        return E.ul(*items)


class AnswersByQuestionRow(TableRow):
    FORWARD_TO_RESPONSE = tuple(
        "full_clean after_ui_save disable_delete as_summary_item".split())

    def __init__(self, response, question):
        AnswerRemark = rt.models.polls.AnswerRemark
        AnswerChoice = rt.models.polls.AnswerChoice
        self.response = response
        self.question = question
        # Needed by AnswersByQuestion.get_row_by_pk
        self.pk = self.id = response.pk
        try:
            self.remark = AnswerRemark.objects.get(question=question,
                                                   response=response).remark
        except AnswerRemark.DoesNotExist:
            self.remark = ''

        self.choices = AnswerChoice.objects.filter(question=question,
                                                   response=response)
        for k in self.FORWARD_TO_RESPONSE:
            setattr(self, k, getattr(question, k))

    def __str__(self):
        if self.choices.count() == 0:
            return str(_("N/A"))
        return ', '.join([str(ac.choice) for ac in self.choices])


class AnswersByQuestion(dd.VirtualTable):
    label = _("Answers")
    master = 'polls.Question'
    column_names = 'response:40 answer:30 remark:20 *'
    variable_row_height = True
    auto_fit_column_widths = True

    @classmethod
    def get_data_rows(self, ar):
        question = ar.master_instance
        if question is None:
            return
        for r in rt.models.polls.Response.objects.filter(poll=question.poll):
            yield AnswersByQuestionRow(r, question)

    @dd.displayfield(_("Response"))
    def response(self, obj, ar):
        return ar.obj2html(obj.response)

    @dd.displayfield(_("Remark"))
    def remark(self, obj, ar):
        return obj.remark

    @dd.displayfield(_("Answer"))
    def answer(self, obj, ar):
        return str(obj)


class PollResult(Questions):
    master_key = 'poll'
    column_names = "question choiceset answers a1"

    # @classmethod
    # def get_data_rows(self, ar):
    #     poll = ar.master_instance
    #     if poll is None:
    #         return
    #     for obj in super(PollResult, self).get_request_queryset(ar):
    #         yield obj

    @dd.virtualfield(dd.ForeignKey('polls.Question'))
    def question(self, obj, ar):
        return obj

    @dd.requestfield(_("#Answers"))
    def answers(self, obj, ar):
        # ~ return ar.spawn(Answer.objects.filter(question=obj))
        return AnswerChoices.create_request(known_values=dict(question=obj))

    @dd.requestfield(_("A1"))
    def a1(self, obj, ar):
        if (cs := obj.get_choiceset()) is None:
            return
        if (ch := next(iter(cs.choices.all()), None)) is None:
            return
        return AnswerChoices.create_request(
            known_values=dict(
                question=obj, **gfk2lookup(
                    rt.models.polls.AnswerChoice.choice, ch)))


def assert_chooser():
    fld = AnswersByResponseEditor.answer
    settings.SITE.register_virtual_field(fld)
    fld.name = "answer"
    fld.return_type.name = "answer"
    check_for_chooser(AnswersByResponseRow, fld, fld.name)


assert_chooser()

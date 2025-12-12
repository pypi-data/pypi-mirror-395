# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.contrib.contenttypes.models import ContentType

from lino.api import _, dd, rt
from lino.modlib.gfks.fields import GenericForeignKey, GenericForeignKeyIdField


class ToggleChoice(dd.Action):
    readonly = False
    show_in_toolbar = False
    parameters = dict(
        question=dd.ForeignKey("polls.Question"),
        choice_type=dd.ForeignKey(ContentType),
        choice_id=dd.PositiveIntegerField(),
    )
    no_params_window = True
    params_layout = 'question\nchoice_type choice_id'

    # We specify params_layout although no_params_window is True because
    # otherwise e.g. lino.api.doctest.get_fields() would display them in
    # arbitrary order

    def run_from_ui(self, ar, **kw):
        assert len(ar.selected_rows) == 1
        response = ar.selected_rows[0]
        if response is None:
            return
        AnswerChoice = rt.models.polls.AnswerChoice
        pv = ar.action_param_values
        qs = AnswerChoice.objects.filter(response=response, **pv)
        if qs.count() == 1:
            qs[0].delete()
        elif qs.count() == 0:
            if not pv.question.multiple_choices:
                # Delete any other choice that might exist
                qs = AnswerChoice.objects.filter(response=response,
                                                 question=pv.question)
                qs.delete()
            obj = AnswerChoice(response=response, **pv)
            obj.full_clean()
            obj.save()
        else:
            raise Exception("Oops, %s returned %d rows." %
                            (qs.query, qs.count()))
        ar.success(refresh=True, refresh_delayed_value=True)
        # dd.logger.info("20140930 %s", obj)


class SetAnswer(dd.Action):

    label = _("Set answer")
    icon_name = None
    show_in_toolbar = False
    params_layout = """
    choice_id
    remark
    question choice_type
    """
    # hidden_elements = {"question"}
    hidden_elements = {"question", "choice_type"}

    def get_action_permission(self, ar, obj, state):
        return not ar.get_user().is_anonymous

    def setup_parameters(self, params):
        choice_type = dd.ForeignKey(ContentType)
        params.update(
            question=dd.ForeignKey("polls.Question"),
            choice_type=choice_type,
            choice_id=GenericForeignKeyIdField(choice_type),
            # choice=GenericForeignKey(
            #     "choice_type", "choice_id", verbose_name=_("My answer")),
            remark=dd.RichTextField(_("Remark"), blank=True, format="plain"))

    @dd.chooser()
    def choice_id_choices(cls, question):
        if question is None:
            # print("20250511 question is None")
            return rt.models.polls.Choice.objects.none()
            # return [[0, "20250511 question is None"]]
        # print(f"20250724 question is {repr(question)}")
        cs = question.get_choiceset()
        ct = cs.choice_type
        if ct is None or ct.model_class() is rt.models.polls.Choice:
            return rt.models.polls.Choice.objects.filter(choiceset=cs)
        return ct.model_class().objects.all()

    def run_from_ui(self, ar, **kw):
        assert len(ar.selected_rows) == 1
        response = ar.selected_rows[0]
        if response is None:
            return
        AnswerChoice = rt.models.polls.AnswerChoice
        AnswerRemark = rt.models.polls.AnswerRemark
        pv = ar.action_param_values
        flt = dict(response=response, question=pv.question)
        qs = AnswerRemark.objects.filter(**flt)
        if qs.count() == 1:
            obj = qs[0]
            if pv.remark:
                obj.remark = pv.remark
                obj.full_clean()
                obj.save()
            else:
                obj.delete()
        elif qs.count() == 0:
            obj = AnswerRemark(**flt)
            obj.full_clean()
            obj.save()
        else:
            raise Exception("Oops, %s returned %d rows." %
                            (qs.query, qs.count()))

        qs = AnswerChoice.objects.filter(**flt)
        if qs.count() == 1:
            qs[0].choice_id = pv.choice_id
            obj.full_clean()
            obj.save()
        elif qs.count() == 0:
            obj = AnswerChoice(choice_id=pv.choice_id, **flt)
            obj.full_clean()
            obj.save()
        else:
            raise Exception("Oops, %s returned %d rows." %
                            (qs.query, qs.count()))
        ar.success(refresh=True)
        # dd.logger.info("20140930 %s", obj)

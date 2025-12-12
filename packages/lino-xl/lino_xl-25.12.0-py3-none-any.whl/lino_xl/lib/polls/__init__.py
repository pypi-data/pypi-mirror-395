# Copyright 2013-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Provides database models and functionality for managing polls.

See also :doc:`/projects/polly` and :doc:`/specs/polls`.

.. autosummary::
   :toctree:

    fixtures.bible
    fixtures.feedback
    fixtures.compass

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    # See :doc:`/dev/plugins`

    verbose_name = _("Polls")
    needs_plugins = ['lino_xl.lib.xl']

    def get_head_lines(cls, site, request):
        yield """
        <script>
        window.Lino = window.Lino || {};
        const Lino = window.Lino;
        Lino.choiceset = {};
        function fetchChoiceSetItems(choicesetId, actorId, query="") {
            window.fetch(`choices/${actorId.split('.').join('/')}?choiceset=${choicesetId}&query=${query}`)
                .then(resp => resp.json())
                .then(data => {
                    const datalist = document.getElementById(`choiceset_${choicesetId}`);
                    Lino.choiceset[choicesetId].rows = data.rows;
                    const choices = {};
                    data.rows.forEach(row => choices[row.text] = row.value);
                    Lino.choiceset[choicesetId].data = choices;
                    const options = [];
                    data.rows.forEach(row => {
                        const option = document.createElement('option', value=row.text);
                        option.setAttribute("data-value", row.value);
                        option.innerText = row.text;
                        options.push(option);
                    });
                    datalist.replaceChildren(...options);
                });
        }
        function onChoiceSetInputFocus(choicesetId, actorId) {  // choicesetId: number, actorId: string
            if (!window.fetch) return;
            if (!(choicesetId in Lino.choiceset)) {
                Lino.choiceset[choicesetId] = {};
                fetchChoiceSetItems(choicesetId, actorId);
            }
            console.log(Lino.choiceset);
        }
        function onChoiceSetInputChange(event, choicesetId, actorId) {
            if (!window.fetch) return;
            const text = event.target.value;
            if (text in Lino.choiceset[choicesetId].data) {
                // TODO: DO SUBMIT
            } else {
                fetchChoiceSetItems(choicesetId, actorId, text);
            }
        }
        </script>
        """

    def setup_main_menu(self, site, user_type, m, ar=None):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('polls.MyPolls')
        m.add_action('polls.MyResponses')

    def setup_config_menu(self, site, user_type, m, ar=None):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('polls.ChoiceSets')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('polls.AllPolls')
        m.add_action('polls.Questions')
        m.add_action('polls.Choices')
        m.add_action('polls.AllResponses')
        m.add_action('polls.AnswerChoices')
        m.add_action('polls.AllAnswerRemarks')
        # ~ m.add_action('polls.Answers')

    def get_dashboard_items(self, user):
        yield self.site.models.polls.MyResponses

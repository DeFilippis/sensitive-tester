from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Sorter
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import translation


class TransMixin:
    def get_current_language(self):
        return self.subsession.get_current_language()

    def get_context_data(self, **context):
        user_language = self.get_current_language()
        translation.activate(user_language)
        return super().get_context_data(**context)


class oTreePage(TransMixin, Page):
    def get_progress(self):
        totpages = self.participant._max_page_index
        curpage = self.participant._index_in_pages
        totsorters = Sorter.objects.filter(s__owner=self.participant).exclude(
            f='relative_importance')
        unsubmitted_qs = totsorters.filter(submitted=True).count()

        return f"{(curpage + unsubmitted_qs) / (totpages + totsorters.count()) * 100:.0f}"


class UnFailedPage(oTreePage):
    def get(self):
        if self.player.total_attempts_failed >= Constants.MAX_ATTENTION_FAILURES:
            self._increment_index_in_pages()
            return self._redirect_to_page_the_user_should_be_on()
        return super().get()

    def get_context_data(self, *args, **kwargs):
        c = super().get_context_data(*args, **kwargs)
        c['attentionError'] = json.loads(json.dumps(Constants.attention_error, cls=DjangoJSONEncoder))
        return c


class GenPage(UnFailedPage):

    def get_context_data(self, *args, **kwargs):
        c = super().get_context_data(*args, **kwargs)

        c['field'] = Constants.fields[self.round_number - 1]
        c['field_desc'] = Constants.leads[c['field']][self.get_current_language()]
        c['field_range'] = [(i, j) for i,j in enumerate(c['field_desc']['range'])]
        return c


class DistributionPage(UnFailedPage):
    def is_displayed(self):
        if self.round_number <= len(Constants.fields):
            curfield = Constants.fields[self.round_number - 1]
            return curfield == 'average_attitude'
        return False

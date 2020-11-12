from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Sorter
from django.db.models import Q


class oTreePage(Page):
    def get_progress(self):
        totpages = self.participant._max_page_index
        curpage = self.participant._index_in_pages
        totsorters = Sorter.objects.filter(s__owner=self.participant).exclude(
            f='relative_importance')
        unsubmitted_qs = totsorters.filter(submitted=True).count()

        return f"{(curpage + unsubmitted_qs) / (totpages + totsorters.count()) * 100:.0f}"


class GenPage(oTreePage):

    def get_context_data(self, *args, **kwargs):
        c = super().get_context_data(*args, **kwargs)
        c['field'] = Constants.fields[self.round_number - 1]
        c['field_desc'] = Constants.leads[c['field']]
        return c


class DistributionPage(oTreePage):
    def is_displayed(self):
        if self.round_number <= len(Constants.fields):
            curfield = Constants.fields[self.round_number - 1]
            return curfield == 'average_attitude'
        return False

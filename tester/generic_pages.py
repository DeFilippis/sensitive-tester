from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class GenPage(Page):
    def get_context_data(self, *args, **kwargs):
        c = super().get_context_data(*args, **kwargs)
        # not the best way, really ugly, Think later. TODO:
        c['field'] = list(Constants.leads.keys())[self.round_number - 1]
        c['field_desc'] = Constants.leads[c['field']]
        return c

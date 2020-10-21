from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Q(Page):
    live_method = 'get_next_q'




page_sequence = [Q]

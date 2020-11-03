from otree.api import Currency as c, currency_range
from ._builtin import WaitPage, Page as oTreePage
from .generic_pages import GenPage as Page
from .models import Constants


class Distribution(Page):
    def is_displayed(self):
        return self.round_number == 1

    live_method = 'get_next_q_for_distribution'


class QIntro(Page):
    def is_displayed(self):
        return self.round_number < Constants.num_rounds

    """
    Here we introduce the forthcoming set of questions
    """


class Q(Page):
    """
    Here we show the set of questions (:
    personal attitude,
    average attitude,
    likelyhood of friendship,
    personal (aka absolute) Importance,
    distribution of averages
    """

    def is_displayed(self):
        return self.round_number < Constants.num_rounds

    live_method = 'get_next_q'


class RelIntro(oTreePage):
    """
    Introducing relative importance question
    """

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class RelImportance(oTreePage):
    """
    A bit particular page for ranking questions by their relative importance.
    Doesnt' make sense to reuse previous app because it's just too different
    """

    def post(self):
        """VERY UGLY WAY. SHOULD FIX IT LATER!!!"""
        for k, v in self.request.POST.dict().items():
            try:
                i = self.participant.sqs.get(label=k)
                i.relative_importance = v
                i.save()
            except Exception as e:
                print(e)
        return super().post()

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Distribution,
    QIntro,
    Q,
    RelIntro,
    RelImportance,
]

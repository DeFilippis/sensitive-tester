from otree.api import Currency as c, currency_range
from ._builtin import WaitPage
from .generic_pages import GenPage as Page, DistributionPage,oTreePage
from .models import Constants




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
    likelihood of friendship,
    personal (aka absolute) Importance,
    distribution of averages
    """

    def is_displayed(self):
        #print(self.player.get_next_q())
        return self.round_number < Constants.num_rounds

    def vars_for_template(self):
        pass
        #return(
            #dict{
            #    field = self.player.get_next_q
            #}
        #)

    live_method = 'get_next_q'


class DistributionIntro(DistributionPage):
    """
    Introducing distribution question
    """


class Distribution(DistributionPage):
    live_method = 'get_next_q_for_distribution'


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
    QIntro,
    Q,
    DistributionIntro,
    Distribution,
    RelIntro,
    RelImportance,
]

from .generic_pages import GenPage as Page, DistributionPage, oTreePage, UnFailedPage
from .models import Constants


class Intro(Page):
    """First page - consent form etc."""
    def is_displayed(self):
        return self.round_number == 1


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
        return self.round_number < Constants.num_rounds

    live_method = 'get_next_q'


class DistributionIntro(DistributionPage):
    """
    Introducing distribution question
    """


class Distribution(DistributionPage):
    live_method = 'get_next_q_for_distribution'

    def js_vars(self):
        return dict(
            distribution_explication=str(Constants.distribution_explication),
            distribution_obj=str(Constants.distribution_obj))


class RelIntro(UnFailedPage):
    """
    Introducing relative importance question
    """

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class RelImportance(UnFailedPage):
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

    def js_vars(self):
        return dict(
            rank_obj=str(Constants.rank_obj),
        )


class TooManyFailures(oTreePage):
    def is_displayed(self):
        return self.player.total_attempts_failed >= Constants.MAX_ATTENTION_FAILURES


page_sequence = [
    Intro,
    QIntro,
    Q,
    DistributionIntro,
    Distribution,
    RelIntro,
    RelImportance,
    TooManyFailures,
]

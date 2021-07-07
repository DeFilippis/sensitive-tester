from .generic_pages import GenPage as Page, DistributionPage, oTreePage, UnFailedPage
from .models import Constants
import logging

logger = logging.getLogger(__name__)
from django_user_agents.utils import get_user_agent


class Intro(Page):
    def get(self, *args, **kwargs):
        user_agent = get_user_agent(self.request)
        self.player.useragent_is_mobile = user_agent.is_mobile
        self.player.useragent_is_bot = user_agent.is_bot
        self.player.useragent_browser_family = user_agent.browser.family
        self.player.useragent_os_family = user_agent.os.family
        self.player.useragent_device_family = user_agent.device.family
        return super().get()

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
            if k != 'csrfmiddlewaretoken':
                try:
                    i = self.participant.sqs.get(label=k)
                    i.relative_importance = v
                    i.save()
                except Exception as e:
                    logger.warning(e)

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

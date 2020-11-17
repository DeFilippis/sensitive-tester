from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.utils.translation import gettext_lazy as _


class Constants(BaseConstants):
    name_in_url = 'endline'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    sex = models.StringField(
        choices=['Male', 'Female'],
        verbose_name="What is your biological sex?",
        widget=widgets.RadioSelect)

    birth = models.IntegerField(
        min=1930,
        max=2002,
        verbose_name=_("What year were you born?")
    )

    education = models.StringField(
        verbose_name=_('What is the highest level of education that you have achieved?'),
        choices=[
            _('Less than High School'),
            _('H.S. Graduate'),
            _('Some College'),
            _('Associate\'s Degree'),
            _('College Graduate'),
            _('Master\'s Degree'),
            _('Professional Degree (JD/MD)'),
            _('PhD')
        ],
        widget=widgets.RadioSelect)

    income = models.StringField(
        verbose_name=_("Which of the following best represents your household income last year before taxes?"),
        choices=[
            "Less than $10,000",
            "$10,000 to $19,999",
            "$20,000 to $29,999",
            "$30,000 to $39,999",
            "$40,000 to $49,999", "$50,000 to $59,999", "$60,000 to $69,999", "$70,000 to $79,999", \
            "$80,000 to $89,999", "$90,000 to $99,999", "$100,000 to $149,999", "$150,000 or more"],
        widget=widgets.RadioSelect)

    religion = models.StringField(
        verbose_name=_("Which of these labels best matches your religious views?"),
        choices=[_('Atheist'), _('Agnostic'), _('Spiritual but not religious'), _('Christian'), _('Muslim'), _('Hindu'),
                 _('Buddhist'),
                 _('Sikh'), _('Jewish'), _('Another religion not mentioned here')],
        widget=widgets.RadioSelect)

    religious_attendance = models.StringField(
        verbose_name=_("How frequently do you attend religious services?"),
        choices=[
            _('At least once a week'),
            _('Once or twice a month / A few times a year'),
            _('Seldom / never')
        ],
        widget=widgets.RadioSelect)

    feedback = models.LongStringField(
        verbose_name=_("Do you have any feedback for us?  Did you enjoy the experiment?  Any complaints?"))

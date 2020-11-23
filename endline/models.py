from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.utils.translation import gettext_lazy as _


class Constants(BaseConstants):
    name_in_url = 'endline'
    players_per_group = None
    num_rounds = 1
    EDUCATION_CHOICES = [
        [1, _('Primary education/Middle school')],
        [2, _('Secondary or vocational education')],
        [3, _('A-levels/Uncompleted university degree')],
        [4, _('Bachelor/Master')],
        [5, _('PhD')],
    ]
    INCOME_CHOICES = [
        [1, _('Not enough money even for food')],
        [2, _('Enough for food, but not enough to buy clothes and shoes')],
        [3, _('Enough for clothes and shoes, but not enough for the purchase of small household appliances')],
        [4,
         _("Enough money for small purchases, but buying expensive things (a computer, "
         "washing machine, refrigerator) requires savings or credit."
           )],
        [5,
         _(
             "There is enough money to buy for a house, but to buy a car, a summer "
             "residence, an apartment you need to save or take a loan")],
        [6, _("We can afford any purchases without restrictions and loans")]
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sex = models.StringField(
        choices=[_('Male'), _('Female')],
        verbose_name=_("Please indicate your gender"),
        widget=widgets.RadioSelect)

    birth = models.IntegerField(
        min=18,
        max=102,
        verbose_name=_("How old are you?")
    )

    education = models.StringField(
        verbose_name=_('What is the highest level of education that you have achieved?'),
        choices=Constants.EDUCATION_CHOICES,
        widget=widgets.RadioSelect)

    income = models.StringField(
        label=_("""Which statement most accurately describes your family’s financial situation?"""),
        choices=Constants.INCOME_CHOICES,
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

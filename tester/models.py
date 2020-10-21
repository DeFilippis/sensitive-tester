from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from django.db import models as djmodels

author = 'Chapkovski, De Filippis, Henig-Schmidt'

doc = """
App testing for the most controversial questions for the conformity project
"""


class Constants(BaseConstants):
    name_in_url = 'tester'
    players_per_group = None
    num_rounds = 1
    LIKERT = range(0, 11)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

class ProtoQ(djmodels.Model):
    body = models.StringField()

class SensitiveQ(djmodels.Model):
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name="sqs")
    prototype = djmodels.ForeignKey(to=ProtoQ, on_delete=djmodels.CASCADE, related_name="sqs")
    attitude = models.IntegerField(choices=Constants.LIKERT, widget=widgets.RadioSelectHorizontal)
    average_attitude = models.IntegerField(choices=Constants.LIKERT, widget=widgets.RadioSelectHorizontal)
    """
    The block of the following questions is to elicit info about distribution shape.
    We may think about something more complex later on. 
    """
    first = models.IntegerField(min=0, max=100)
    second = models.IntegerField(min=0, max=100)
    third = models.IntegerField(min=0, max=100)
from django.db.models.signals import post_migrate,class_prepared
def my_callback(sender, **kwargs):
    print('migration complete')
    pass
post_migrate.connect(my_callback)
class_prepared.connect(my_callback)
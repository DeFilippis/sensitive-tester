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
import csv
import itertools

author = 'Chapkovski, De Filippis, Henig-Schmidt'

doc = """
App testing for the most controversial questions for the conformity project
"""


class Constants(BaseConstants):
    name_in_url = 'tester'
    players_per_group = None
    num_rounds = 1
    LIKERT = range(0, 11)

    with open('./data/q.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        bodies = [i[0] for i in csv_reader]


class Subsession(BaseSubsession):
    def creating_session(self):
        ps = self.player_set.all()
        sqs = [SensitiveQ(owner=p, body=t) for p, t in itertools.product(ps, Constants.bodies)]
        SensitiveQ.objects.bulk_create(sqs)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class ProtoQ(djmodels.Model):
    body = models.StringField()


class SensitiveQ(djmodels.Model):
    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name="sqs")
    body = models.StringField()
    attitude = models.IntegerField(choices=Constants.LIKERT, widget=widgets.RadioSelectHorizontal)
    average_attitude = models.IntegerField(choices=Constants.LIKERT, widget=widgets.RadioSelectHorizontal)
    """
    The block of the following questions is to elicit info about distribution shape.
    We may think about something more complex later on. 
    """
    first = models.IntegerField(min=0, max=100)
    second = models.IntegerField(min=0, max=100)
    third = models.IntegerField(min=0, max=100)
    """Friendship answer. Do we want them to be likert as well?"""
    friend = models.IntegerField(choices=Constants.LIKERT)

    def __str__(self):
        return f'Q: "{self.body}" for participant {self.owner.participant.code}'

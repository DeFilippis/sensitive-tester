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
import logging

logger = logging.getLogger(__name__)
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
    def get_next_q(self, data):
        logger.info(data)
        qid = data.get('qid')
        field = data.get('field')
        value = data.get('value')
        next_q = self.next_q()
        r = {self.id_in_group: next_q}
        if data.get('info_request'):
            return r

        if data.get('answer') and qid and field and value:
            q = SensitiveQ.objects.get(id=qid)
            setattr(q, field, value)
            q.save()
        r = {self.id_in_group: self.next_q()}  # we update the req
        return r

    def next_q(self):
        """
        We figure out the next unanswered question and return it
        we do it the following way:
        we first check if there are unanswered individual questions, if there are any we return the first one
        check if there are unanswered average questions
        then we return if there are unsanswered questions about distribution
        and then we return the questions about friendship

        """
        checking_order = ['attitude', 'average_attitude', 'first', 'friend']
        for i in checking_order:
            d = {f'{i}__isnull': True}
            unanswered = self.sqs.filter(**d)
            if unanswered.exists():
                q = unanswered.first()
                return dict(body=q.body, field=i, id=q.id)
            else:
                continue
        return dict(no_q_left=True)


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

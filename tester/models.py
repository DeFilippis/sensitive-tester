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
import yaml
from otree.models import Participant

logger = logging.getLogger(__name__)
author = 'Chapkovski, De Filippis, Henig-Schmidt'

doc = """
App testing for the most controversial questions for the conformity project
"""


class Constants(BaseConstants):
    name_in_url = 'tester'
    players_per_group = None

    LIKERT = range(0, 11)

    with open(r'./data/qleads.yaml') as file:
        leads = yaml.load(file, Loader=yaml.FullLoader)
    fields = list(leads.keys())  # again, not the best one, but will work for now. TODO?

    num_rounds = len(fields) + 1  # we ask one extra question (about relative importance).
    with open(r'./data/q.yaml') as file:
        qs = yaml.load(file, Loader=yaml.FullLoader)

    bodies = [q.get('statement') for q in qs]
    for_ranking = [{'label': q.get('for_ranking')} for q in qs]


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            ps = self.session.get_participants()
            sqs = [SensitiveQ(owner=p, body=t.get('statement'), label=t.get('for_ranking'))
                   for p, t in itertools.product(ps, Constants.qs)]
            SensitiveQ.objects.bulk_create(sqs)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def _next_q_for_dist(self):
        unanswered = self.participant.sqs.filter(first__isnull=True)

        if unanswered.exists():
            q = unanswered.first()
            return dict(body=q.body, id=q.id)
        else:
            return dict(no_q_left=True)

    def get_next_q_for_distribution(self, data):
        logger.info('message received from distribution')
        logger.info(data)
        if data.get('info_request'):
            r = {self.id_in_group: self._next_q_for_dist()}
            return r

        qid = data.get('qid')
        distribution = data.get('distribution')
        if qid and distribution:
            q = SensitiveQ.objects.get(id=qid)
            for k, v in distribution.items():
                setattr(q, k, v)
            q.save()
            return {self.id_in_group: self._next_q_for_dist()}  # we update the req

    def get_next_q(self, data):
        logger.info(data)
        qid = data.get('qid')
        field = data.get('field')
        value = data.get('value')
        next_q = self.next_q()
        r = {self.id_in_group: next_q}
        if data.get('info_request'):
            return r

        if data.get('answer') and qid and field and value is not None:
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
        field = Constants.fields[self.round_number - 1]

        d = {f'{field}__isnull': True}
        unanswered = self.participant.sqs.filter(**d)
        print('FIELD', field, unanswered, self.round_number)
        if unanswered.exists():
            q = unanswered.first()
            return dict(body=q.body, field=field, id=q.id)
        else:
            return dict(no_q_left=True)


class SensitiveQ(djmodels.Model):
    owner = djmodels.ForeignKey(to=Participant, on_delete=djmodels.CASCADE, related_name="sqs")
    body = models.StringField()
    label = models.StringField()
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
    # Block of importance questions
    absolute_importance = models.IntegerField(choices=Constants.LIKERT)
    relative_importance = models.IntegerField()

    def __str__(self):
        return f'Q: "{self.body}" for participant {self.owner.code}'


def custom_export(players):
    yield ['code', 'body', 'label', 'attitude', 'average_attitude', 'first', 'second', 'third', 'friendship',
           'absolute_importance', 'relative_importance']
    for q in SensitiveQ.objects.order_by('id'):
        participant = q.owner
        yield [participant.code, q.body, q.label, q.attitude, q.average_attitude, q.first, q.second, q.third, q.friend,
               q.absolute_importance, q.relative_importance]

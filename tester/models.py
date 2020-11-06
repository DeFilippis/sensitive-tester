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
import random
from django.db.models import Q, Max, FloatField

logger = logging.getLogger(__name__)
author = 'Chapkovski, De Filippis, Henig-Schmidt'

doc = """
App testing for the most controversial questions for the conformity project
"""


class Constants(BaseConstants):
    name_in_url = 'tester'
    players_per_group = None
    distributions = [[0, 33, 66, 100], [0, 50, 50, 100]]
    LIKERT = range(0, 11)
    bonus_amount_average = 50  # amount in cents to be bonus participants for guessing second-order beliefs correctly
    bonus_amount_distribution = 50  # amount in cents to bonus participants for guessing distributions correctly

    with open(r'./data/qleads.yaml') as file:
        leads = yaml.load(file, Loader=yaml.FullLoader)
    fields = list(leads.keys())  # again, not the best one, but will work for now. TODO?
    sortable_fields = fields + ['first',
                                'relative_importance']  # we use this for creating custom sorting for each field
    num_rounds = len(fields) + 1  # we ask one extra question (about relative importance).
    with open(r'./data/q.yaml') as file:
        qs = yaml.load(file, Loader=yaml.FullLoader)

    bodies = [q.get('statement') for q in qs]
    for_ranking = [{'label': q.get('for_ranking')} for q in qs]


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.initial_distribution = p.id_in_group % 2
        if self.round_number == 1:
            ps = self.session.get_participants()
            sqs = [SensitiveQ(owner=p, body=t.get('statement'), label=t.get('for_ranking'), order_r=random.random())
                   for p, t in itertools.product(ps, Constants.qs)]
            SensitiveQ.objects.bulk_create(sqs)
            for p in ps:
                for s in p.sqs.all():
                    for f in Constants.sortable_fields:
                        Sorter.objects.create(s=s, f=f, r=random.random())


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    initial_distribution = models.IntegerField()

    def get_ranking_titles(self):
        sqs = self.participant.sqs.all()

        sqs = sqs.annotate(s=Max('sorters__r', filter=Q(sorters__f='relative_importance'), output_field=FloatField()),
                           ).order_by('s').values_list('label', flat=True)

        return [{'label': q} for q in sqs]

    def get_distribution(self):
        return Constants.distributions[self.initial_distribution]

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
        qid = data.get('qid')
        distribution = data.get('distribution')
        if data.get('slider_movement_counter') and qid:
            q = SensitiveQ.objects.get(id=qid)
            q.slider_movement_counter += 1
            q.save()
            return
        if data.get('info_request'):
            r = {self.id_in_group: self._next_q_for_dist()}
            return r

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
        if field in Constants.sortable_fields:
            unanswered = unanswered.annotate(s=Max('sorters__r', filter=Q(sorters__f=field), output_field=FloatField()),
                                             ).order_by('s')

        print('FIELD', field, unanswered, self.round_number)
        if unanswered.exists():
            q = unanswered.first()
            return dict(body=q.body, field=field, id=q.id)
        else:
            return dict(no_q_left=True)


class SensitiveQ(djmodels.Model):
    class Meta:
        ordering = ['order_r']

    owner = djmodels.ForeignKey(to=Participant, on_delete=djmodels.CASCADE, related_name="sqs")
    body = models.StringField()
    label = models.StringField()
    attitude = models.IntegerField(choices=Constants.LIKERT, widget=widgets.RadioSelectHorizontal)
    average_attitude = models.IntegerField(choices=Constants.LIKERT, widget=widgets.RadioSelectHorizontal)
    slider_movement_counter = models.IntegerField(default=0)
    order_r = models.FloatField()
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


class Sorter(djmodels.Model):
    s = djmodels.ForeignKey(to=SensitiveQ, on_delete=djmodels.CASCADE, related_name='sorters')
    r = models.FloatField()
    f = models.StringField()

    def __str__(self):
        return f'sorter for {self.s.body}: field {self.f}, r: {self.r}'


def custom_export(players):
    yield ['code', 'body', 'label', 'attitude', 'average_attitude', 'first', 'second', 'third', 'friendship',
           'absolute_importance', 'relative_importance', 'slider_movement_counter', 'order_r']
    for q in SensitiveQ.objects.order_by('id'):
        participant = q.owner
        yield [participant.code, q.body, q.label, q.attitude, q.average_attitude, q.first, q.second, q.third, q.friend,
               q.absolute_importance, q.relative_importance, q.slider_movement_counter, q.order_r]

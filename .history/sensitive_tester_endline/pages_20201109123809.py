from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants

import re
import csv
import random


class Endline(Page):
    form_model = 'player'
    form_fields = ['sex', 'birth', 'race', 'education', 'income', 'feedback', 'feedback']


            
page_sequence = [
        Endline,
]




                   
            
            
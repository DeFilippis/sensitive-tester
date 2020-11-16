from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import pandas as pd


class Constants(BaseConstants):
    name_in_url = 'sensitive_tester_endline'
    players_per_group = None
    num_rounds = 1
        

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
        sex = models.StringField(
                choices=['Male', 'Female'],
                verbose_name = "What is your biological sex?",
                widget=widgets.RadioSelect)

        birth = models.IntegerField(
                min = 1930, 
                max = 2002, 
                verbose_name = "What year were you born?")

        race = models.StringField(
                verbose_name = 'What race do you most identify with?',
                choices=['White', 'Black or African American', 'Asian', 'American Indian or Alaska Native', 'Native Hawaiian or Pacific Islander'],
                widget=widgets.RadioSelect)

        education = models.StringField(
                verbose_name = 'What is the highest level of education that you have achieved?',
                choices= ['Less than High School', 'H.S. Graduate', 'Some College', 'Associate\'s Degree', 'College Graduate', 'Master\'s Degree', 'Professional Degree (JD/MD), PhD'],
                widget=widgets.RadioSelect)

        income = models.StringField(
                verbose_name = "Which of the following best represents your household income last year before taxes?",
                choices= ["Less than $10,000", "$10,000 to $19,999", "$20,000 to $29,999", "$30,000 to $39,999", \
                                "$40,000 to $49,999", "$50,000 to $59,999", "$60,000 to $69,999", "$70,000 to $79,999", \
                                "$80,000 to $89,999", "$90,000 to $99,999", "$100,000 to $149,999", "$150,000 or more"],
                widget=widgets.RadioSelect)


        religion = models.StringField(
                verbose_name = "Which of these labels best matches your religious views?", 
                choices = ['Atheist', 'Agnostic', 'Spiritual but not religious', 'Christian', 'Muslim', 'Hindu', 'Buddhist', 'Sikh', 'Jewish', 'Another religion not mentioned here'],
                widget=widgets.RadioSelect)

        religious_attendance = models.StringField(
                verbose_name = "How frequently do you attend religious services?"
                choices = ['At least once a week', 'Once or twice a month / A few times a year', 'Seldom / never'],
                widget=widgets.RadioSelect)      

        feedback = models.LongStringField(
                verbose_name = "Do you have any feedback for us?  Did you enjoy the experiment?  Any complaints?")
    
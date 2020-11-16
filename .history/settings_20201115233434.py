from os import environ
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SESSION_CONFIGS = [
    dict(
       name='tester',
       display_name="tester",
       num_demo_participants=1,
       app_sequence=['tester']
    ),
    dict(
       name='tester2',
       display_name="tester for 2",
       num_demo_participants=2,
       app_sequence=['tester']
    ),

    dict(
       name='endline',
       display_name="endline_test",
       num_demo_participants=1,
       app_sequence=['sensitive_tester_endline']
    ),


]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '&7hh8&8q=8ifh$)0&kzlh^)!tqas&4s4w6dofyup+!n4=i)7m)'

# if an app is included in SESSION_CONFIGS, you don't need to list it here

INSTALLED_APPS = [
    'otree',
    'webpack_loader',
]

WEBPACK_LOADER = {
    'DEFAULT': {
        # 'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'vue/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'front', 'webpack-stats.json'),
        'POLL_INTERVAL': 0.3,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map']
    }
}
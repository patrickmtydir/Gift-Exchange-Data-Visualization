from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=0.04, participation_fee=7)
SESSION_CONFIGS = [dict(name='my_session', num_demo_participants=5, app_sequence=['Gift_Exchange_Baseline'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []
ROOMS = [dict(name='XSFS', display_name='Experimental Social Sciences Laboratory at Florida State University'),]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
DEBUG = 0


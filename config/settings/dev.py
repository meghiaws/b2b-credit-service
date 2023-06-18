from .base import *

# add django-debug-toolbar if the environment is "dev"
from config.settings.debug_toolbar.settings import *
from config.settings.debug_toolbar.setup import DebugToolbarSetup

INSTALLED_APPS, MIDDLEWARE = DebugToolbarSetup.do_settings(INSTALLED_APPS, MIDDLEWARE)

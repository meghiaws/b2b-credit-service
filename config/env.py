import os
import environ
from django.core.exceptions import ImproperlyConfigured

env = environ.Env()

BASE_DIR = environ.Path(__file__) - 2

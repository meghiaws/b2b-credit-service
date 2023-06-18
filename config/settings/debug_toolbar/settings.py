from config.env import env

DEBUG_TOOLBAR_ENABLED = False if env.bool("ENVIRONMENT") == "prod" else True
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "config.settings.debug_toolbar.setup.show_toolbar"
}

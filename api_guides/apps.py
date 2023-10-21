from django.apps import AppConfig
from FirebaseUtil.FirebaseGuideSyncer import synced_with_local_db
from utils.Logger import log
import sys


class ApiGuidesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_guides'

    def ready(self):
        if ("migrate" in sys.argv) or ("makemigrations" in sys.argv) or ("collectstatic" in sys.argv):
            log.debug("Skipping firebase listeners")
            return
        log.debug("Initializing APiGuide app config...")
        synced_with_local_db()

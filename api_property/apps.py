from django.apps import AppConfig
from FirebaseUtil.FirebasePropertySyncer import synced_with_local_db
from utils.Logger import log
import sys


class ApiPropertyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_property'

    def ready(self):
        if ("migrate" in sys.argv) or ("makemigrations" in sys.argv) or ("collectstatic" in sys.argv):
            log.debug("Skipping firebase listeners")
            return
        log.debug("Initializing APIProperty app config...")
        # synced_with_local_db()

from django.apps import AppConfig
from utils.Logger import log
from FirebaseUtil.firebaseConf import FirebaseConf
from mongoUtils.ActivitiesUtils import sync_activity_with_firebase


class ApiActivitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_activities'

    def ready(self):
        log.debug("Initializing ApiActivities app config...")
        FirebaseConf.get_activity_collection().on_snapshot(sync_activity_with_firebase)

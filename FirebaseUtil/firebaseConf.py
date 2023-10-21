from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from django.conf import settings
from utils.Logger import log

FIREBASE_CREDENTIALS_PATH = settings.RES_DIR / "hellohere-firebase-adminsdk.json"


class __FirebaseRef:
    def __init__(self):
        log.debug("Creating firebase config object...")
        self.__firestore_client = None
        self.__guide_collection = None
        self.__property_collection = None
        self.__property_req_collection = None
        self.__location_collection = None
        self.__account_collection = None
        self.__subscriber_collection = None
        self.__activity_collection = None
        self.__agents_collection = None
        self.__ready_content_collection = None
        self.__initialize_fs_client()

    def __initialize_fs_client(self):
        cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
        self.__firestore_client = firestore.client()

    def get_firestore_client(self):
        if not self.__firestore_client:
            self.__initialize_fs_client()
        return self.__firestore_client

    def get_guide_collection(self):
        if not self.__guide_collection:
            log.debug("Initializing guide collection...")
            self.__guide_collection = self.__firestore_client.collection(u"guides")
        return self.__guide_collection

    def get_property_collection(self):
        if not self.__property_collection:
            log.debug("Initializing property collection...")
            self.__property_collection = self.__firestore_client.collection(u"properties")
        return self.__property_collection

    def get_property_request_collection(self):
        if not self.__property_req_collection:
            log.debug("Initializing property request collection...")
            self.__property_req_collection = self.__firestore_client.collection(u"mallorcamagic_property_request")
        return self.__property_req_collection

    def get_location_collection(self):
        if not self.__location_collection:
            log.debug("Initializing location collection...")
            self.__location_collection = self.__firestore_client.collection(u"locations")
        return self.__location_collection

    def get_account_collection(self):
        if not self.__account_collection:
            log.debug("Initializing account collection...")
            self.__account_collection = self.__firestore_client.collection(u"mallorcamagic_accounts")
        return self.__account_collection

    def get_subscriber_collection(self):
        if not self.__subscriber_collection:
            log.debug("Initializing subscriber collection...")
            self.__subscriber_collection = self.__firestore_client.collection(u"mallorcamagic_subscribers")
        return self.__subscriber_collection

    def get_activity_collection(self):
        if not self.__activity_collection:
            log.debug("Initializing activity collection...")
            self.__activity_collection = self.__firestore_client.collection(u"affiliate_products")
        return self.__activity_collection

    def get_agent_collection(self):
        if not self.__agents_collection:
            log.debug("Initializing agent collection...")
            self.__agents_collection = self.__firestore_client.collection(u"extern_user")
        return self.__agents_collection

    def get_ready_content_collection(self):
        if not self.__ready_content_collection:
            log.debug("Initializing ready content collection...")
            self.__ready_content_collection = self.__firestore_client.collection(u"readycontent")
        return self.__ready_content_collection


# Create singleton instance
FirebaseConf = __FirebaseRef()

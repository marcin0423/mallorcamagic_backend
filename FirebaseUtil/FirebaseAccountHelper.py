from firebase_admin import firestore
from FirebaseUtil.firebaseConf import FirebaseConf
from utils.Logger import log


def __get_user_with_email(email):
    account_ref = FirebaseConf.get_account_collection()
    query = account_ref.where(u"email", u"==", email).get()

    user = None
    for doc_ref in query:
        user = doc_ref
        break
    return user


def __add_new_user(data):
    account_ref = FirebaseConf.get_account_collection()
    data['timestamp'] = firestore.SERVER_TIMESTAMP
    doc_ref = account_ref.add(data)
    return doc_ref[1].get().to_dict()


def save_or_update_user(data):
    try:
        user = __get_user_with_email(data['email'])
        if not user:
            __add_new_user(data)
        else:
            user._reference.update(data)
    except Exception as e:
        log.error("Unable to save user to firebase: " + str(e))


def subscribe_user(email):
    collection_ref = FirebaseConf.get_subscriber_collection()

    # Check if already exists
    query = collection_ref.where(u"email", u"==", email).get()
    for doc_ref in query:
        log.error("subscriber already exists")
        return doc_ref.to_dict()

    # subscribe
    data = {'email': email, "timestamp": firestore.SERVER_TIMESTAMP }
    doc_ref = collection_ref.add(data)
    return doc_ref[1].get().to_dict()

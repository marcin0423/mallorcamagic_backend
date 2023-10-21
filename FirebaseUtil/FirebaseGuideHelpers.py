from firebase_admin import firestore
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from FirebaseUtil.firebaseConf import FirebaseConf
from utils.Logger import log


def get_latest_guides(limit=10, start=""):
    start_cursor = None
    if len(start) > 0:
        try:
            start_cursor = DatetimeWithNanoseconds.from_rfc3339(start)
        except:
            start_cursor = None

    # Query
    guide_ref = FirebaseConf.get_guide_collection()
    if start_cursor:
        query = guide_ref.order_by(u"timestamp", direction=firestore.Query.DESCENDING)\
            .start_after({u"timestamp": start_cursor}).limit(limit).stream()
    else:
        query = guide_ref.order_by(u"timestamp", direction=firestore.Query.DESCENDING).limit(limit).stream()

    # Convert to dict
    guides = []
    for doc_ref in query:
        doc = doc_ref.to_dict()
        doc['id'] = doc_ref.id
        guides.append(doc)

    log.debug("Fetched total: " + str(len(guides)))
    return guides, len(guides) >= limit


def get_single_guide(slug):
    guide_ref = FirebaseConf.get_guide_collection()
    query = guide_ref.where(u"slug", u"==", slug).get()

    selected_guide = None
    for doc_ref in query:
        selected_guide = doc_ref.to_dict()
        break
    return selected_guide

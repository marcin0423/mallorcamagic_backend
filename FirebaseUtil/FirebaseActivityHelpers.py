from firebase_admin import firestore
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from FirebaseUtil.firebaseConf import FirebaseConf
from utils.Logger import log


def get_top_activities(limit=10, start=0.0, product_code="", tag=""):
    # Query
    query = FirebaseConf.get_activity_collection()
    if len(tag) > 0 and tag != "All Activities":
        tag = tag.replace(" ", '-')
        tag = tag.lower()
        query = query.where(u'details.tag', u'==', tag)

    if start > 0.0:
        query = query.order_by(u"rating.normalized", direction=firestore.Query.DESCENDING)\
            .order_by(u"productCode")\
            .start_after({u"rating.normalized": start, u"productCode": product_code}).limit(limit).stream()
    else:
        query = query.order_by(u"rating.normalized", direction=firestore.Query.DESCENDING)\
            .order_by(u"productCode").limit(limit).stream()

    # Convert to dict
    activities = []
    for doc_ref in query:
        doc = doc_ref.to_dict()
        doc['id'] = doc_ref.id
        activities.append(doc)

    log.debug("Fetched total: " + str(len(activities)))
    return activities, len(activities) >= limit


def get_single_activity(slug):
    activity_ref = FirebaseConf.get_activity_collection()
    query = activity_ref.where(u"slug", u"==", slug).get()

    selected_guide = None
    for doc_ref in query:
        selected_guide = doc_ref.to_dict()
        break
    return selected_guide

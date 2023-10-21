from firebase_admin import firestore
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from FirebaseUtil.firebaseConf import FirebaseConf
from utils.Logger import log


def __format_content(content):
    data = {}
    data['id'] = content["shortcode"]
    data['is_video'] = content['is_video']
    data['media'] = content['storage_url']
    data['author'] = content['author_username']
    data['timestamp'] = content['timestamp']

    # TODO: add language filter
    data['title'] = content['title'][0]
    data['description'] = content['short_desc'][0]

    return data


def get_ready_contents(limit=10):
    ready_col = FirebaseConf.get_ready_content_collection()
    contents = ready_col.order_by(u"timestamp", direction=firestore.Query.DESCENDING).limit(limit).get()
    formatted_contents = []
    for content in contents:
        formatted_contents.append(__format_content(content.to_dict()))
    log.debug("Fetched total: " + str(len(formatted_contents)))
    return formatted_contents

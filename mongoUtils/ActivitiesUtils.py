import pymongo
from .mongoConf import db
from .PropertiesUtils import __replace_object_id
from utils.Logger import log


activity_collection = db['affiliate_products']


def get_top_activities(limit=10, start=0, product_code="", tag=""):
    query = {}
    if len(tag) > 0 and tag != "All Activities":
        tag = tag.replace(" ", '-')
        tag = tag.lower()
        query['details.tag'] = tag

    activities = activity_collection.find(query).sort("rating.normalized", pymongo.DESCENDING).skip(start).limit(limit)
    activities = list(activities)
    for activity in activities:
        __replace_object_id(activity)

    log.debug("Fetched total: " + str(len(activities)))
    return activities, len(activities) >= limit


# TODO: Add filter for languages also
def get_single_activity(slug):
    activity = activity_collection.find_one({"slug": slug})
    if activity:
        __replace_object_id(activity)
        return activity
    return None


def __insert_activity(data):
    activity_collection.insert_one(data)


def __update_activity(slug, data):
    activity_collection.find_one_and_update({"slug": slug}, {"$set": data})


def __remove_activity(slug):
    activity_collection.find_one_and_delete({"slug": slug})


def sync_activity_with_firebase(col_snapshot, changes, read_time):
    for change in changes:
        data = change.document.to_dict()
        if not ("slug" in data.keys()): continue

        if change.type.name == 'ADDED' or change.type.name == 'MODIFIED':
            if not get_single_activity(data['slug']):
                __insert_activity(data)
            else:
                __update_activity(data['slug'], data)
        elif change.type.name == 'REMOVED':
            __remove_activity(data['slug'])

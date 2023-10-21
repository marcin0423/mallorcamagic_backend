import pymongo
from .mongoConf import db
from .PropertiesUtils import __replace_object_id
from utils.Logger import log
import re


guide_collection = db["guides"]


def get_latest_guides(limit=10, start=0):
    guides = guide_collection.find({}).sort("timestamp", pymongo.DESCENDING).skip(start).limit(limit)
    guides = list(guides)
    for guide in guides:
        __replace_object_id(guide)
    log.debug("Fetched total: " + str(len(guides)))
    return guides, len(guides) >= limit


def get_single_guide(slug):
    guide = guide_collection.find_one({"slug": slug})
    if guide:
        __replace_object_id(guide)
        return guide
    return None


def search_guides_with_cat(cat, limit, start=0):
    guides = guide_collection.find({"details.category": re.compile(f"^{cat}$", re.IGNORECASE)})\
        .sort().skip(start).limit(limit)
    guides = list(guides)
    for guide in guides:
        __replace_object_id(guide)
    log.debug("Fetched total: " + str(len(guides)))
    return guides, len(guides) >= limit


def __insert_guide(data):
    guide_collection.insert_one(data)


def __update_guide(slug, data):
    guide_collection.find_one_and_update({"slug": slug}, {"$set": data})


def __remove_guide(slug):
    guide_collection.find_one_and_delete({"slug": slug})


def sync_guide_with_firebase(change):
    data = change.document.to_dict()
    if not ("slug" in data.keys()): return

    if change.type.name == 'ADDED' or change.type.name == 'MODIFIED':
        if not get_single_guide(data['slug']):
            __insert_guide(data)
        else:
            __update_guide(data['slug'], data)
    elif change.type.name == 'REMOVED':
        __remove_guide(data['slug'])

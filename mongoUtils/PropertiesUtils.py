import pymongo
import re
import random
import math
from .mongoConf import db
from utils.Logger import log


slugs = [u'slug', u'slug_es', u'slug_de']
property_collection = db['properties']


def __replace_object_id(item):
    # lists
    if isinstance(item, list):
        for obj in item:
            __replace_object_id(obj)
        return

    # base case
    if not isinstance(item, dict) or not item:
        return

    # find all the objectId fields
    updates = []
    nans = []
    for key in item.keys():
        if isinstance(item[key], pymongo.collection.ObjectId):
            updates.append(key)
        elif isinstance(item[key], float) and math.isnan(item[key]):
            nans.append(key)
        else:
            __replace_object_id(item[key])

    # Replace with str
    for key in updates:
        item[key] = str(item[key])

    # Replace NaNs with 0
    for key in nans:
        item[key] = 0


def __get_list_from_query(query):
    items = list(query)
    for item in items:
        __replace_object_id(item)
    return items


def __format_suggestion_properties(cur_prop, lang_id=0):
    data = {}
    if lang_id == 0:
        data['slug'] = cur_prop["slug"]
    elif lang_id == 1:
        data['slug'] = cur_prop["slug_es"]
    else:
        data['slug'] = cur_prop["slug_de"]

    data['title'] = cur_prop["details"]["title"][lang_id]
    if "thumbnail_sm" in cur_prop.keys():
        data['thumbnail'] = cur_prop["thumbnail_sm"]
    elif len(cur_prop['thumbnail']) > 0:
        data['thumbnail'] = cur_prop["thumbnail"][0]
    else:
        data['thumbnail'] = ""
    data["price"] = cur_prop["details"]["price_unit"] + cur_prop["details"]["price_amount"]

    data['bathrooms'] = cur_prop["details"]["bathrooms"]
    data['bedrooms'] = cur_prop["details"]["bedrooms"]
    data['area'] = cur_prop['details']['size_plot']
    return data


def search_property(limit, start, from_price, to_price, area, prop_for, prop_type, sort):
    # Query the firebase
    query = {
        "details.is_enabled": True,
        "details.price_int": {
            "$gte": from_price,
            "$lt": to_price
        }
    }

    # Filter area if exists
    if len(area) > 0:
        query["details.loc_city"] = area

    # sale/rent
    if len(prop_for) > 0:
        query["details.category"] = prop_for

    # type
    if len(prop_type) > 0:
        query["details.type"] = prop_type

    properties = property_collection.find(query).sort(sort["by"], sort["order"]).skip(start).limit(limit)
    total = property_collection.count_documents(query)
    properties = __get_list_from_query(properties)
    return properties, total


def get_enabled_property_count():
    return property_collection.count_documents({"details.is_enabled": True})


def get_gallery_properties():
    properties = []
    try:
        ranges = [[500_000, 1_000_000], [1_000_000, 1_500_000], [1_500_000, 2_500_000], [2_500_000, 10_500_000]]
        for rng in ranges:
            props = property_collection.aggregate([
                    { "$match": { "details.price_int": { "$gte": rng[0], "$lt": rng[1]} } },
                    { "$sample": { "size": 1 } }
                ])
            properties.append(__get_list_from_query(props)[0])
    except Exception as e:
        log.error("Gallery Property error: " + str(e))
    return properties


# Top properties shown in the home page
# Randomly select proeprties for now
# TODO: Add too property selection in the external dashboard and show those properties here
def get_top_properties(limit=10):
    properties = []
    try:
        props = property_collection.aggregate([
                { "$match": { "details.is_enabled": True } },
                { "$sample": { "size": limit } }
            ])
        properties = __get_list_from_query(props)
    except Exception as e:
        log.error("Top Property error: " + str(e))
    return properties


def get_latest_properties(limit=10):
    query = property_collection.find({"details.is_enabled": True}).sort("timestamp", pymongo.DESCENDING).limit(limit)
    properties = __get_list_from_query(query)
    log.debug("Fetched total: " + str(len(properties)))
    return properties


def get_property(slug, lang):
    prop = property_collection.find_one({slugs[lang]: slug, "details.is_enabled": True})
    if not prop:
        return None
    __replace_object_id(prop)
    return prop


def get_neighbours(location, slug, lang):
    properties = property_collection.find({
        "details.loc_city": re.compile(location, re.IGNORECASE),
        slugs[lang]: {"$ne": slug},
        "details.is_enabled": True
    })
    properties = list(properties)
    selected_neighbours = random.sample(properties, k=min(4, len(properties)))
    for i in range(len(selected_neighbours)):
        __replace_object_id(selected_neighbours[i])
        selected_neighbours[i] = __format_suggestion_properties(selected_neighbours[i], lang)
    log.debug("Total neighbors of: " + slug + " = " + str(len(selected_neighbours)))
    return selected_neighbours


def get_may_likes_properties(category, slug, lang):
    properties = property_collection.find({
        "details.type": re.compile(category, re.IGNORECASE),
        slugs[lang]: {"$ne": slug},
        "details.is_enabled": True
    })
    properties = list(properties)
    selected_properties = random.sample(properties, k=min(4, len(properties)))
    for i in range(len(selected_properties)):
        __replace_object_id(selected_properties[i])
        selected_properties[i] = __format_suggestion_properties(selected_properties[i], lang)
    log.debug("Total neighbors of: " + slug + " = " + str(len(selected_properties)))
    return selected_properties


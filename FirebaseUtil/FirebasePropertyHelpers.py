from firebase_admin import firestore
from FirebaseUtil.firebaseConf import FirebaseConf
from utils.Logger import log
import random


slugs = [u'slug', u'slug_es', u'slug_de']


# Convert to dict
def __get_dict_from_query(query):
    properties = []
    for doc_ref in query:
        doc = doc_ref.to_dict()
        doc['id'] = doc_ref.id
        properties.append(doc)
    return properties


def __get_all_approved_agents():
    query = FirebaseConf.get_agent_collection().where(u"approved", u"==", True).get()
    agents = []
    for doc in query:
        doc = doc.to_dict()
        agents.append(doc['email'])
    return agents


def get_latest_properties(limit=10):
    # Query
    property_ref = FirebaseConf.get_property_collection()
    query = property_ref.order_by(u"timestamp", direction=firestore.Query.DESCENDING).limit(limit).stream()
    properties = __get_dict_from_query(query)
    log.debug("Fetched total: " + str(len(properties)))
    return properties


def search_property(limit, start, from_price, to_price, area, prop_for, prop_type):
    # Query the firebase
    property_ref = FirebaseConf.get_property_collection()
    query = property_ref.order_by(u"details.price_int")
    query = query.where(u"details.is_enabled", u"==", True)
    query = query.where(u"details.price_int", u">=", from_price)
    query = query.where(u"details.price_int", u"<=", to_price)

    # Filter area if exists
    if len(area) > 0:
        query = query.where(u"details.loc_city", u"==", area)

    # sale/rent
    if len(prop_for) > 0:
        query = query.where(u"details.category", u"==", prop_for)

    # type
    if len(prop_type) > 0:
        query = query.where(u"details.type", u"==", prop_type)

    query = query.start_after({u"details.price_int": start}).limit(limit).stream()
    properties = __get_dict_from_query(query)
    log.debug("Fetched total: " + str(len(properties)))
    return properties


def search_property_with_agents(limit, start, from_price, to_price, area, prop_for, prop_type):
    # Query the firebase
    property_ref = FirebaseConf.get_property_collection()
    query = property_ref.order_by(u"details.price_int")
    query = query.where(u"details.is_enabled", u"==", True)
    query = query.where(u"details.price_int", u">=", from_price)
    query = query.where(u"details.price_int", u"<=", to_price)

    # Filter area if exists
    if len(area) > 0:
        query = query.where(u"details.loc_city", u"==", area)

    # sale/rent
    if len(prop_for) > 0:
        query = query.where(u"details.category", u"==", prop_for)

    # type
    if len(prop_type) > 0:
        query = query.where(u"details.type", u"==", prop_type)

    # agents filter
    all_properties = []
    for agent in __get_all_approved_agents():
        q = query.where(u"partner_email", u"==", agent)
        docs = q.start_after({u"details.price_int": start}).limit(limit).stream()
        all_properties += __get_dict_from_query(docs)

    #randomly select limit properties
    properties = random.sample(all_properties, k=min(limit, len(all_properties)))
    log.debug("Fetched total: " + str(len(properties)))
    return sorted(properties, key=lambda x: x['details']['price_int'])


def get_property(slug, lang):
    # Query the firebase
    property_ref = FirebaseConf.get_property_collection()
    query = property_ref.where(slugs[lang], u"==", slug).get()

    properties = __get_dict_from_query(query)
    log.debug("Fetched total: " + str(len(properties)))
    if len(properties) >= 1:
        return properties[0]
    return None


def get_locations():
    loc_ref = FirebaseConf.get_location_collection()
    locations = []
    for loc in loc_ref.stream():
        try:
            locations.append(loc.to_dict()["name"])
        except Exception as e:
            log.error(str(e))

    log.debug("Fetched total: " + str(len(locations)))
    return locations


def add_property_request(data):
    prop_req_ref = FirebaseConf.get_property_request_collection()
    prop_req_ref.add(data)
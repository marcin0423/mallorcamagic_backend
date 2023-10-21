from datetime import date, datetime
import pymongo
from .mongoConf import db
from utils.Logger import log
from .PropertiesUtils import property_collection

'''
-------------------------SCHEMA---------------------------
extern_statistics collection
    document: {
        date: datetime.date.today()
        properties: [
            {
                id: property_id,
                agent_id: agent_id
                stats: {
                    views: number,
                    leads: number
                    ...other data
                }
            }
        ]
        agents: [
            {
                id: agent_id,
                stats: {
                    views: number
                }
            }
        ]
'''
statistics_collection = db['extern_statistics']
empty_stat_view = {
    'views': 1,
    'saves': 0,
    'leads': 0
}
empty_stat_save = {
    'views': 0,
    'saves': 1,
    'leads': 0
}
empty_stat_lead = {
    'views': 0,
    'saves': 0,
    'leads': 1
}


def __get_today():
    return datetime.fromordinal(date.today().toordinal())


def __get_todays_document_id():
    doc = statistics_collection.find_one({'date': __get_today()})
    if not doc:
        print("Document not exists. Creating...")
        doc = statistics_collection.insert_one({
            'date': __get_today(),
            'properties': [],
            "agents": []
        })
        return doc.inserted_id
    return doc["_id"]


def __exists_property(doc_id, property_id):
    exists = statistics_collection.find_one(
        {'_id': doc_id, 'properties.property_id': property_id}
    )
    return exists is not None


def __exists_agent(doc_id, agent_id):
    exists = statistics_collection.find_one(
        {'_id': doc_id, 'agents.agent_id': agent_id}
    )
    return exists is not None


def __get_agent_id_from_prop_id(property_id):
    prop = property_collection.find_one({"_id": pymongo.collection.ObjectId(property_id)})
    if prop:
        return str(prop["agent_id"])
    return ""


def stat_increment_view_count(property_id):
    log.debug("Incrementing view: " + str(property_id))
    doc_id = __get_todays_document_id()
    if not __exists_property(doc_id, property_id):
        # insert property stats
        statistics_collection.update_one(
            {'_id': doc_id},
            {'$push': {
                'properties': {
                    'property_id': property_id,
                    "agent_id": __get_agent_id_from_prop_id(property_id),
                    'stats': empty_stat_view
                }
            }}
        )
    else:
        # update property stats
        statistics_collection.update_one(
            {'_id': doc_id, 'properties.property_id': property_id},
            {'$inc': {'properties.$.stats.views': 1}}
        )


def stat_increment_save_count(property_id):
    log.debug("Incrementing saves: " + str(property_id))
    doc_id = __get_todays_document_id()
    if not __exists_property(doc_id, property_id):
        # insert property stats
        statistics_collection.update_one(
            {'_id': doc_id},
            {'$push': {
                'properties': {
                    'property_id': property_id,
                    "agent_id": __get_agent_id_from_prop_id(property_id),
                    'stats': empty_stat_save
                }
            }}
        )
    else:
        # update property stats
        statistics_collection.update_one(
            {'_id': doc_id, 'properties.property_id': property_id},
            {'$inc': {'properties.$.stats.saves': 1}}
        )


def stat_increment_lead_count(property_id):
    log.debug("Incrementing saves: " + str(property_id))
    doc_id = __get_todays_document_id()
    if not __exists_property(doc_id, property_id):
        # insert property stats
        statistics_collection.update_one(
            {'_id': doc_id},
            {'$push': {
                'properties': {
                    'property_id': property_id,
                    "agent_id": __get_agent_id_from_prop_id(property_id),
                    'stats': empty_stat_lead
                }
            }}
        )
    else:
        # update property stats
        statistics_collection.update_one(
            {'_id': doc_id, 'properties.property_id': property_id},
            {'$inc': {'properties.$.stats.leads': 1}}
        )


def stat_increment_agent_view_count(agent_id):
    agent_id = str(agent_id)
    log.debug("Incrementing view: " + agent_id)
    doc_id = __get_todays_document_id()
    if not __exists_agent(doc_id, agent_id):
        # insert agent stats
        statistics_collection.update_one(
            {'_id': doc_id},
            {'$push': {
                'agents': {
                    'agent_id': agent_id,
                    'stats': {
                        "views": 1
                    }
                }
            }}
        )
    else:
        # update property stats
        statistics_collection.update_one(
            {'_id': doc_id, 'agents.agent_id': agent_id},
            {'$inc': {'agents.$.stats.views': 1}}
        )


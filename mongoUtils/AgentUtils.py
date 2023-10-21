import pymongo
from .mongoConf import db
from utils.Logger import log
from bson import ObjectId
from .PropertiesUtils import __replace_object_id, __get_list_from_query, property_collection
import mongoUtils.StatisticsUtils as statUtils


agent_collection = db['extern_user']


def __get_id_from_slug(slug):
    try:
        return slug.split("-")[-1]
    except Exception as e:
        log.error("Agent slug parsing error: " + str(e))


def __create_slug_from_id_name(agent_id, name):
    slug = agent_id
    if name != "":
        slug = f"{name.replace(' ', '-')}-{agent_id}"
    return slug


def __format_agent(agent, total_properties):
    agent_data = {}
    try:
        agent_data["name"] = agent["company"]["name"]
        agent_data["description"] = agent["company"]["description"]
        agent_data["contact"] = agent["contact"]
        agent_data["address"] = agent["address"]
        agent_data["images"] = agent['images']
        agent_data["id"] = agent["_id"]
        agent_data["slug"] = __create_slug_from_id_name(agent["_id"], agent["company"]["name"])
        agent_data["total"] = total_properties
    except: pass
    return agent_data


def get_agent(slug):
    agent_id = __get_id_from_slug(slug)
    return get_agent_with_id(agent_id)


def get_agent_with_id(agent_id):
    try:
        agent = agent_collection.find_one({"_id": ObjectId(agent_id)})
        if not agent:
            return None
        __replace_object_id(agent)
        total_properties = property_collection.count_documents({"details.is_enabled": True, "agent_id": ObjectId(agent["_id"])})
        agent_data = __format_agent(agent, total_properties)
        return agent_data
    except Exception as e:
        log.error(str(e))
        return None


def increment_agent_view_count(agent_id):
    try:
        agent = get_agent_with_id(agent_id)
        if not agent:
            return False
        statUtils.stat_increment_agent_view_count(ObjectId(agent_id))
        return True
    except Exception as e:
        log.error(str(e))
        return False


def get_agent_property(limit, start, sort, agent_id):
    query_dict = {
        "details.is_enabled": True,
        "agent_id": ObjectId(agent_id)
    }
    properties = property_collection.find(query_dict).sort(sort["by"], sort["order"]).skip(start).limit(limit)
    total = property_collection.count_documents(query_dict)
    properties = __get_list_from_query(properties)
    return properties, total

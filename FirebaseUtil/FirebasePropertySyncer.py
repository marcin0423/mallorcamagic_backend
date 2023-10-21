from FirebaseUtil.firebaseConf import FirebaseConf
from utils.Logger import log


def __update_property(propertyDict, prop):
    prop.slug = propertyDict['slug']
    prop.slug_es = propertyDict['slug_es']
    prop.slug_de = propertyDict['slug_de']
    prop.location = propertyDict['details']['loc_city']

    if "type" in propertyDict['details'].keys():
        prop.type = propertyDict['details']['type']
    else:
        prop.type = "apartment"

    if 'thumbnail_sm' in propertyDict.keys():
        prop.thumbnail = propertyDict['thumbnail_sm']
    else:
        prop.thumbnail = propertyDict["thumbnail"][0]

    prop.title = propertyDict['details']['title'][0]
    prop.title_es = propertyDict['details']['title'][1]
    prop.title_de = propertyDict['details']['title'][2]

    prop.description = propertyDict['details']['description'][0]
    prop.description_es = propertyDict['details']['description'][1]
    prop.description_de = propertyDict['details']['description'][2]

    prop.price_unit = propertyDict['details']['price_unit']
    prop.price_amount = propertyDict['details']['price_amount']

    prop.area = propertyDict['details']['size_plot']
    prop.bathrooms = propertyDict['details']['bathrooms']
    prop.bedrooms = propertyDict['details']['bedrooms']
    prop.save()


def __add_or_update_property(prop_dict):
    if not "slug" in prop_dict.keys():
        log.error("No slug...discording...")
        return
    from api_property.models import PropertyModel
    props = PropertyModel.objects.filter(slug=prop_dict['slug'])
    if not props.exists():
        log.debug(f"Adding property {prop_dict['slug']}")
        __update_property(prop_dict, PropertyModel())
    else:
        log.debug(f"Updating property {prop_dict['slug']}")
        __update_property(prop_dict, props.first())


def __delete_property(prop_dict):
    from api_property.models import PropertyModel
    try:
        log.debug(f"Deleting guide {prop_dict['slug']}")
        PropertyModel.objects.filter(slug=prop_dict['slug']).delete()
    except Exception as e:
        log.error("Unable to remove guide: " + str(e))


# Synced guides with local DB
def __on_property_snapshot_listener(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED' or change.type.name == 'MODIFIED':
            # Filter for enabled properties
            doc_dict = change.document.to_dict()
            if 'details' in doc_dict.keys() and "is_enabled" in doc_dict['details'] and doc_dict['details']['is_enabled']:
                __add_or_update_property(change.document.to_dict())
            else:
                __delete_property(change.document.to_dict())
        elif change.type.name == 'REMOVED':
            __delete_property(change.document.to_dict())


def synced_with_local_db():
    log.debug("Adding property snapshot listener....")
    from api_property.models import PropertyModel
    PropertyModel.objects.all().delete()
    FirebaseConf.get_property_collection().on_snapshot(__on_property_snapshot_listener)

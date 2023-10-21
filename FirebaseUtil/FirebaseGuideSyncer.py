from FirebaseUtil.firebaseConf import FirebaseConf
from utils.Logger import log
from mongoUtils.GuideUtils import sync_guide_with_firebase


def __update_guide(guide_dict, guide):
    guide.highlighted = False
    if "highlighted" in guide_dict.keys():
        guide.highlighted = guide_dict["highlighted"]

    guide.slug = guide_dict['slug']
    guide.creator = guide_dict['details']['creator']

    if 'thumbnail_sm' in guide_dict.keys():
        guide.thumbnail = guide_dict['thumbnail_sm']
    else:
        guide.thumbnail = guide_dict['thumbnail'][0]

    guide.category = guide_dict['details']["category"]
    guide.timestamp = guide_dict['timestamp']

    guide.title_en = guide_dict['details']['title'][0]
    guide.title_es = guide_dict['details']['title'][1]
    guide.title_de = guide_dict['details']['title'][2]

    guide.short_desc_en = guide_dict['details']['short_desc'][0]
    guide.short_desc_es = guide_dict['details']['short_desc'][1]
    guide.short_desc_de = guide_dict['details']['short_desc'][2]

    guide.long_desc_en = guide_dict['details']['long_desc'][0]
    guide.long_desc_es = guide_dict['details']['long_desc'][1]
    guide.long_desc_de = guide_dict['details']['long_desc'][2]
    guide.save()


def __add_or_update_guide(guide_dict):
    if not "slug" in guide_dict.keys():
        log.error("No slug...discording...")
        return
    from api_guides.models import GuideModel
    guide = GuideModel.objects.filter(slug=guide_dict['slug'])
    if not guide.exists():
        log.debug(f"Adding guide {guide_dict['slug']}")
        __update_guide(guide_dict, GuideModel())
    else:
        log.debug(f"Updating guide {guide_dict['slug']}")
        __update_guide(guide_dict, guide.first())


def __delete_guide(guide_dict):
    from api_guides.models import GuideModel
    try:
        log.debug(f"Deleting guide {guide_dict['slug']}")
        GuideModel.objects.filter(slug=guide_dict['slug']).delete()
    except Exception as e:
        log.error("Unable to remove guide: " + str(e))


# Synced guides with local DB
def __on_guide_snapshot_listener(col_snapshot, changes, read_time):
    for change in changes:
        sync_guide_with_firebase(change)
        if change.type.name == 'ADDED' or change.type.name == 'MODIFIED':
            __add_or_update_guide(change.document.to_dict())
        elif change.type.name == 'REMOVED':
            __delete_guide(change.document.to_dict())


def synced_with_local_db():
    log.debug("Adding guide snapshot listener....")
    FirebaseConf.get_guide_collection().on_snapshot(__on_guide_snapshot_listener)

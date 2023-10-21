from django.http import JsonResponse, HttpResponseNotFound
from utils.Common import get_limit_from_request
from mongoUtils import ActivitiesUtils as activitiesUtils
from utils.Logger import log
from utils.Common import get_language_idx_from_request


def __add_language_filter(activities, lang_id=0):
    for activity in activities:
        activity['details']['title'] = [activity['details']['title'][lang_id]]
        activity['details']['long_desc'] = [activity['details']['long_desc'][lang_id]]
    return activities


# search activities
def get_activities(request):
    log.debug(request.GET)

    # Parse request params
    language = get_language_idx_from_request(request)
    limit = get_limit_from_request(request)
    start = 0
    productCode = request.GET.get("productCode", "")
    tag = request.GET.get("tag", "")
    try:
        start = int(request.GET.get("start", "0"))
    except:
        pass

    # get data
    activities = activitiesUtils.get_top_activities(limit=limit, start=start, product_code=productCode, tag=tag)

    # Get data from firebase
    response_dict = {"data": __add_language_filter(activities[0], language), "more": activities[1]}
    return JsonResponse(response_dict)


def get_home_activities(request):
    log.debug(request.GET)

    # Parse request params
    language = get_language_idx_from_request(request)
    limit = get_limit_from_request(request)
    start = 0
    productCode = request.GET.get("productCode", "")
    tag = request.GET.get("tag", "")
    try:
        start = int(request.GET.get("start", "0"))
    except:
        pass

    # get data
    activities = activitiesUtils.get_top_activities(limit=limit, start=start, product_code=productCode, tag=tag)
    activities = __add_language_filter(activities[0], language)
    mapped_activities = []
    for activity in activities:
        temp_activity = {
            "details": {
                "title": activity['details']['title'],
                "price_unit": activity['details']['price_unit'],
                "price_amount": activity['details']['price_amount']
            },
            "slug": activity['slug'],
            "rating": {
                "average": activity['rating']['average'],
                "total": activity['rating']['total']
            }
        }

        if "thumbnail_sm" in activity.keys():
            temp_activity['image'] = activity['thumbnail_sm']
        elif len() > 0:
            temp_activity['image'] = activity['thumbnail'][0]
        else:
             temp_activity['image'] = ""
        mapped_activities.append(temp_activity)

    # Get data from firebase
    response_dict = {"data": mapped_activities, "more": activities[1]}
    return JsonResponse(response_dict)


def get_activity_detail(request):
    # Parse request params
    slug = request.GET.get("slug", "")
    language = get_language_idx_from_request(request)
    activity = activitiesUtils.get_single_activity(slug)
    if not activity:
        return HttpResponseNotFound('activity not found with slug: ' + slug)
    return JsonResponse({'item': __add_language_filter([activity], language)[0]})

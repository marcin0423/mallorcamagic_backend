from django.http import JsonResponse, Http404
from rest_framework.decorators import api_view
import mongoUtils.GuideUtils as guideDBUtils
from .models import GuideModel
from saved_data.models import SavedGuide
from utils.Common import get_limit_from_request, get_start_offset_from_request, get_language_idx_from_drf_request, get_language_idx_from_request
from utils.Logger import log
import requests


def __get_limit_from_request(request):
    try:
        return int(request.GET.get("limit", "10"))
    except Exception as e:
        return 10


def __add_saved_flag(guides, user):
    slug_dict = {}
    for saved in SavedGuide.objects.filter(user=user):
        slug_dict[saved.slug] = True

    for guide in guides:
        if guide['slug'] in slug_dict.keys() and slug_dict[guide['slug']]:
            guide['is_saved'] = True
        else:
            guide['is_saved'] = False


def __add_language_filter(guides, lang_id=0):
    lang_postfixes = ['', '_es', '_de']
    ext = lang_postfixes[lang_id]
    for guide in guides:
        guide['details']['title'] = [guide['details']['title'][lang_id]]
        guide['details']['short_desc'] = [guide['details']['short_desc'][lang_id]]
        guide['details']['long_desc'] = [guide['details']['long_desc'][lang_id]]

        # points
        for point in guide['guide_points']:
            try:
                if point['type'] == 'point':
                    point['data'] = point['data' + ext]
                    point['sub_data'] = point['sub_data' + ext]
                    del point['data_es']
                    del point['data_de']
                    del point['sub_data_es']
                    del point['sub_data_de']
                elif point['type'] == 'topic':
                    point['data'] = point['data' + ext]
                    del point['data_es']
                    del point['data_de']
            except Exception as e:
                log.error(str(e))
    return guides


# Single guide detail
def get_guide_with_slug(request):
    log.debug(request.GET)

    language = get_language_idx_from_request(request)
    slug = request.GET.get("slug")
    guide_obj = guideDBUtils.get_single_guide(slug)
    response_dict = {}
    if guide_obj:
        response_dict['status'] = "ok"
        response_dict['data'] = __add_language_filter([guide_obj], language)[0]
        response_dict['error'] = ""
    else:
        raise Http404
    return JsonResponse(response_dict)


# latest guides
@api_view(http_method_names=["GET"])
def get_latest_guides(request):
    log.debug(request.GET)

    # Get data from firebase
    limit = __get_limit_from_request(request)
    try:
        start = int(request.GET.get("start", "0"))
    except:
        start = 0
    guides, hasNext = guideDBUtils.get_latest_guides(limit, start)
    response_dict = {"data": guides, "more": hasNext}

    # add saved flag
    if request.user.is_authenticated:
        __add_saved_flag(guides, request.user)

    return JsonResponse(response_dict)


# search guides
@api_view(http_method_names=["GET"])
def search_guides(request):
    log.debug(request.GET)
    language = get_language_idx_from_drf_request(request)

    # Parse request params
    limit = get_limit_from_request(request)
    start_from = get_start_offset_from_request(request)
    search_q = request.GET.get("q", "")
    search_cat = request.GET.get("cat", "")
    highlighted = request.GET.get("highlighted", "false")

    # Query
    querySet = GuideModel.objects.all().filter(title_en__icontains=search_q).order_by("-timestamp")
    if len(search_cat) > 0:
        querySet = querySet.filter(category__iexact=search_cat)
    
    if highlighted == "true":
        querySet = querySet.filter(highlighted=True)

    # Parse data
    data = []
    for index, obj in enumerate(querySet):
        if index >= start_from+limit: break
        if index >= start_from:
            data.append(obj.to_dtc(language))

    # add saved flag
    if request.user.is_authenticated:
        __add_saved_flag(data, request.user)

    # Get data from firebase
    response_dict = {"data": data, "more": len(data) >= limit}
    return JsonResponse(response_dict)


# Guide suggestion
@api_view(http_method_names=["GET"])
def get_suggested_guides(request):
    language = get_language_idx_from_drf_request(request)
    query = request.GET.get("q", "")
    highlighted = request.GET.get("highlighted", "false")

    querySet = GuideModel.objects.all().filter(title_en__icontains=query).order_by("-timestamp")
    if language == 1: querySet = GuideModel.objects.all().filter(title_es__icontains=query).order_by("-timestamp")
    elif language == 2: querySet = GuideModel.objects.all().filter(title_de__icontains=query).order_by("-timestamp")

    if highlighted == "true":
        querySet = querySet.filter(highlighted=True)

    data = []
    limit = 5
    for index, obj in enumerate(querySet):
        text = obj.title_en
        if language == 1: text = obj.title_es
        elif language == 2: text = obj.title_de
        data.append({"id": obj.slug, "text": text, "img": obj.thumbnail})

    # # add saved flag
    # if request.user.is_authenticated:
    #     __add_saved_flag(data, request.user)

    return JsonResponse({"data": data})


def __send_vboat_request(first_name, last_name, email, phone, sub_id, label, birthday, user_input):
    try:
        url = "https://www.vbt.io/embedcode/submit/76166/"
        payload = {
            'vbout_EmbedForm[field][408614]': first_name,
            'vbout_EmbedForm[field][408615]': last_name,
            'vbout_EmbedForm[field][408616]': email,
            'vbout_EmbedForm[field][408617]': phone,

            'vbout_EmbedForm[field][572979]': sub_id,
            'vbout_EmbedForm[field][572980]': "",
            'vbout_EmbedForm[field][572981]': label,
            'vbout_EmbedForm[field][572982]': birthday,
            'vbout_EmbedForm[field][573954]': user_input,
            'vbout_EmbedForm[field][408628]': "",
            '_format': 'json'
        }
        response = requests.request("POST", url, data=payload)
        log.debug(response.text)
    except Exception as e:
        log.error(str(e))


@api_view(http_method_names=["POST"])
def bot_email_collector_handler(request):
    try:
        data = request.data
        __send_vboat_request(data['first_name'], data['last_name'], data['email'], data['phone_number'], data['psid'],
                             data['labels'], data['birthdate'], str(data['user_input_data']))
    except Exception as e:
        log.error(str(e))
    return JsonResponse({"success": True})

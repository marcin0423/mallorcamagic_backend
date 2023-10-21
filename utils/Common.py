import requests
from django.conf import settings
import pymongo


# Retrieve limit from url search params
def get_limit_from_request(request):
    try:
        return int(request.GET.get("limit", "10"))
    except Exception as e:
        return 10


# Retrieve start offset from url search params
def get_start_offset_from_request(request):
    try:
        return int(request.GET.get("start", "0"))
    except Exception as e:
        return 0


# Verify recaptcha token
def verify_recaptcha_token(token):
    payload = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRETE,
        'response': token
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    return response.json()['success']


# Verify recaptcha token from request
def verify_recaptcha_token_from_request(request):
    if 'recaptcha' in request.data.keys():
        return verify_recaptcha_token(request.data['recaptcha'])
    else:
        return False


def get_language_idx_from_drf_request(request):
    languages = ['en', 'es', 'de']
    lang = request.query_params.get('lang', 'en')
    for idx, ln in enumerate(languages):
        if ln == lang:
            return idx
    return 0


def get_language_idx_from_request(request):
    languages = ['en', 'es', 'de']
    lang = request.GET.get('lang', 'en')
    for idx, ln in enumerate(languages):
        if ln == lang:
            return idx
    return 0


def __get_sorting_field_from_dict(sort_dict):
    SORT_FIELDS = {
        "recent": "timestamp",
        "price": "details.price_int",
        "plot_size": "details.size_plot",
        "bathroom": "details.bathrooms",
        "living_size": "details.size_construction"
    }
    try:
        sort_dict['order'] = pymongo.ASCENDING if sort_dict['order'] == "asc" else pymongo.DESCENDING
        sort_dict["by"] = SORT_FIELDS[sort_dict["by"]]
    except: pass
    return sort_dict


def get_sorting_from_drf_request(request):
    # valid types
    SORT_BY_TYPES = ["recent", "price", "plot_size", "bathroom", "living_size"]
    SORT_ORDER_TYPES = ["desc", "asc"]
    sorting_data = {"by": SORT_BY_TYPES[0], "order": SORT_ORDER_TYPES[0]}

    try:
        sort_by = request.GET.get("sort")
        if sort_by in SORT_BY_TYPES:
            sorting_data["by"] = sort_by

        sort_order = request.GET.get("order", "desc")
        if sort_order in SORT_ORDER_TYPES:
            sorting_data["order"] = sort_order
    except: pass
    return __get_sorting_field_from_dict(sorting_data)


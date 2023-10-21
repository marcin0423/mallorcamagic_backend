from django.http import JsonResponse, Http404, HttpResponsePermanentRedirect
from urllib.parse import urlencode, quote_plus
from django.urls import reverse
from rest_framework.decorators import api_view
import FirebaseUtil.FirebasePropertyHelpers as firebasePropertyDB
import mongoUtils.PropertiesUtils as propertyDBUtils
import AlgoliaUtils.PropertyUtils as algoliaPropertyUtils
import mongoUtils.AgentUtils as agentDBUtils
import mongoUtils.StatisticsUtils as statisticsUtils
from FirebaseUtil.FirebasePropertyHelpers import slugs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from utils.Logger import log
from utils.Common import *
from saved_data.models import SavedProperty
import random
from utils.Common import verify_recaptcha_token_from_request, get_sorting_from_drf_request


def __parse_price(str_price):
    try:
        price = ""
        for c in str_price:
            if ord(c) >= ord("0") and ord(c) <= ord("9"):
                price = price + c
        return int(price)
    except Exception as e:
        log.error("Error parsing price: " + str(e))
    return 0


def __add_saved_flag(properties, user):
    slug_dict = {}
    for saved in SavedProperty.objects.filter(user=user):
        slug_dict[saved.slug] = True

    for prop in properties:
        if prop['slug'] in slug_dict.keys() and slug_dict[prop['slug']]:
            prop['is_saved'] = True
        else:
            prop['is_saved'] = False


def __add_language_filter(properties, lang_id):
    for prop in properties:
        prop['details']['title'] = prop['details']['title'][lang_id]
        prop['details']['description'] = prop['details']['description'][lang_id]

        # slugs
        try:
            prop['slug_en'] = prop['slug']
            prop['slug'] = prop[slugs[lang_id]]
        except Exception as e:
            log.error(str(e))


# latest property
def get_latest_property(request):
    log.debug(request.GET)
    items = propertyDBUtils.get_latest_properties(limit=get_limit_from_request(request))
    __add_language_filter(items, get_language_idx_from_request(request))
    response_dict = {"data": items}
    return JsonResponse(response_dict)


# search property
@api_view(http_method_names=["GET"])
def search_property(request):
    log.debug(request.GET)
    language = get_language_idx_from_drf_request(request)

    # Search params
    limit = get_limit_from_request(request)
    start = __parse_price(request.GET.get("start", "0"))
    sorting = get_sorting_from_drf_request(request)
    price_start = __parse_price(request.GET.get("fromPrice", "0"))
    price_end = __parse_price(request.GET.get("toPrice", "1.500.000.000"))
    if price_end <= 0 or request.GET.get("toPrice", "1.500.000.000") == '> 10.000.000': price_end = 1_500_000_000

    area = request.GET.get("area", "")
    prop_for = request.GET.get("for", "")
    prop_type = request.GET.get("type", "")
    query = request.GET.get("query", "")
    log.debug(f"limit: {limit}, start: {start}, price_start: {price_start}, price_end: {price_end}, area: {area}, for: {prop_for}, type: {prop_type} query: {query}")

    # add saved flag
    items, total = algoliaPropertyUtils.search_property(limit=limit, start=start, from_price=price_start,
                    to_price=price_end, area=area, prop_for=prop_for, prop_type=prop_type, sort=sorting, query=query)
    if request.user.is_authenticated:
        __add_saved_flag(items, request.user)

    __add_language_filter(items, language)
    response_dict = {"data": items, "total": total, "next": min(start+limit, total)}
    response_dict['more'] = len(response_dict['data']) >= limit
    return JsonResponse(response_dict)


def __get_neighbours(location, slug, lang):
    return propertyDBUtils.get_neighbours(location, slug, lang)


def __get_may_likes_properties(category, slug, lang):
    return propertyDBUtils.get_may_likes_properties(category, slug, lang)


# Retrieve single property
@api_view(http_method_names=["GET"])
def get_property_detail(request):
    log.debug(request.GET)
    slug = request.GET.get("slug", "")
    language = get_language_idx_from_drf_request(request)
    prop = propertyDBUtils.get_property(slug, language)

    response = {}
    if not prop:
        # check if it is old url
        if "_" in slug:
            slug = slug.replace("_", "-")
            params = request.GET.dict()
            params['slug'] = slug
            url = reverse("property_detail")
            url += "?" + urlencode(params, quote_via=quote_plus)
            return HttpResponsePermanentRedirect(redirect_to=url)
        else:
            raise Http404
    else:
        # statistics
        statisticsUtils.stat_increment_view_count(prop['_id'])

        neighbours = __get_neighbours(prop['details']['loc_city'], slug, language)
        similars = __get_may_likes_properties(prop['details']['type'], slug, language)

        agent = None
        try:
            agent = agentDBUtils.get_agent_with_id(prop["agent_id"])
        except: pass

        if request.user.is_authenticated:
            __add_saved_flag(neighbours, request.user)
            __add_saved_flag(similars, request.user)
            __add_saved_flag([prop], request.user)

        # language filter
        __add_language_filter([prop], language)
        response = {"success": True, "item": prop, "neighbours": neighbours, "similar": similars, "agent": agent}
    return JsonResponse(response)


# gallery properties
@api_view(http_method_names=["GET"])
def gallery_property(request):
    log.debug(request.GET)
    language = get_language_idx_from_drf_request(request)

    # add saved flag
    items = propertyDBUtils.get_gallery_properties()

    __add_language_filter(items, language)
    response_dict = {"data": items}
    return JsonResponse(response_dict)


# top properties
@api_view(http_method_names=["GET"])
def top_property(request):
    log.debug(request.GET)
    language = get_language_idx_from_drf_request(request)
    limit = get_limit_from_request(request)

    # get properties
    items = propertyDBUtils.get_top_properties(limit=limit)

    __add_language_filter(items, language)
    response_dict = {"data": items}
    return JsonResponse(response_dict)

# Map Properties
@api_view(http_method_names=["GET"])
def map_property(request):
    log.debug(request.GET)
    language = get_language_idx_from_drf_request(request)
    limit = get_limit_from_request(request)

    # Query aprams
    start = __parse_price(request.GET.get("start", "0"))
    sorting = get_sorting_from_drf_request(request)
    price_start = __parse_price(request.GET.get("fromPrice", "0"))
    price_end = __parse_price(request.GET.get("toPrice", "1.500.000.000"))
    if price_end <= 0 or request.GET.get("toPrice", "1.500.000.000") == '> 10.000.000': price_end = 1_500_000_000

    area = request.GET.get("area", "")
    prop_for = request.GET.get("for", "")
    prop_type = request.GET.get("type", "")
    query = request.GET.get("query", "")
    log.debug(f"limit: {limit}, start: {start}, price_start: {price_start}, price_end: {price_end}, area: {area}, for: {prop_for}, type: {prop_type} query: {query}")

    # add saved flag
    items, total = algoliaPropertyUtils.search_property(limit=limit, start=start, from_price=price_start,
                    to_price=price_end, area=area, prop_for=prop_for, prop_type=prop_type, sort=sorting, query=query)
    if request.user.is_authenticated:
        __add_saved_flag(items, request.user)

    __add_language_filter(items, language)

    # Remove unnecessary fields
    properties = []
    for prop in items:
        try:
            temp_property = {
                "_id": prop["_id"],
                "details": {
                    "bathrooms": prop['details']['bathrooms'],
                    "bedrooms": prop['details']['bedrooms'],
                    "loc_lat": prop['details']['loc_lat'],
                    "loc_lng": prop['details']['loc_lng'],
                    "size_construction": prop['details']['size_construction'],
                    "title": prop['details']['title'],
                    "price_display": prop['details']['price_display'],
                    "price_unit": prop['details']['price_unit'],
                    "price_int": prop['details']['price_int']
                },
                "thumbnail": prop['thumbnail'][0],
                "slug": prop["slug"]
            }

            # Add thumbnail if exists
            if "thumbnail_sm" in prop.keys():
                temp_property['thumbnail_sm'] = prop["thumbnail_sm"]
            else:
                temp_property['thumbnail_sm'] = prop['thumbnail'][0]
            properties.append(temp_property)
        except:
            pass

    response_dict = {"data": properties, "total": total, "next": min(start+limit, total)}
    return JsonResponse(response_dict)


# agent detail
@api_view(http_method_names=["GET"])
def agent_details(request):
    log.debug(request.GET)
    slug = request.GET.get("slug", "")
    agent = agentDBUtils.get_agent(slug=slug)
    if not agent:
        raise Http404
    return JsonResponse({"agent": agent})


@api_view(http_method_names=["GET"])
def get_property_count(request):
    return JsonResponse({"total": propertyDBUtils.get_enabled_property_count()})


# agent properties
@api_view(http_method_names=["GET"])
def get_agent_property(request):
    log.debug(request.GET)
    agent_slug = request.GET.get("agent", "")
    agent = agentDBUtils.get_agent(agent_slug)
    if not agent: raise Http404

    # parse params
    language = get_language_idx_from_drf_request(request)
    limit = get_limit_from_request(request)
    start = __parse_price(request.GET.get("start", "0"))
    sorting = get_sorting_from_drf_request(request)

    properties, total = agentDBUtils.get_agent_property(limit, start, sorting, agent["id"])
    __add_language_filter(properties, language)
    response_dict = {"data": properties, "total": total, "next": min(start+limit, total), "more": start+limit < total}
    return JsonResponse(response_dict)


@api_view(http_method_names=["POST"])
def increment_agent_views(request):
    agent_id = ""
    if "agent" in request.data.keys():
        agent_id = request.data["agent"]
    else:
        return JsonResponse({"success": False})
    return JsonResponse({"success": agentDBUtils.increment_agent_view_count(agent_id)})


# Save property contact requests
class SavePropertyContactRequest(APIView):
    parser_classes = (JSONParser, )

    def _send_vboat_property_request(self, title, first_name, last_name, email, phone, message, property_url,
                                     agent_email, agent_name):
        try:
            url = "https://www.vbt.io/embedcode/submit/74939/"
            payload = {
                'vbout_EmbedForm[field][573647]': property_url,
                'vbout_EmbedForm[field][408625]': title,
                'vbout_EmbedForm[field][408614]': first_name,
                'vbout_EmbedForm[field][408615]': last_name,
                'vbout_EmbedForm[field][408616]': email,
                'vbout_EmbedForm[field][408617]': phone,
                'vbout_EmbedForm[field][408629]': message,
                'vbout_EmbedForm[field][573943]': agent_email,
                'vbout_EmbedForm[field][573946]': agent_name,
                '_format': 'json'
            }
            response = requests.request("POST", url, data=payload)
            log.debug(response.text)
        except Exception as e:
            log.error(str(e))

    def _send_vboat_agent_request(self, title, first_name, last_name, email, phone, message, property_url,
                                     agent_email, agent_name):
        try:
            url = "https://www.vbt.io/embedcode/submit/76478/"
            payload = {
                'vbout_EmbedForm[field][573647]': property_url,
                'vbout_EmbedForm[field][408625]': title,
                'vbout_EmbedForm[field][573946]': agent_name,
                'vbout_EmbedForm[field][408616]': agent_email,
                'vbout_EmbedForm[field][408614]': first_name,
                'vbout_EmbedForm[field][408615]': last_name,
                'vbout_EmbedForm[field][408617]': phone,
                'vbout_EmbedForm[field][408629]': message,
                'vbout_EmbedForm[field][573943]': email,
                '_format': 'json'
            }
            response = requests.request("POST", url, data=payload)
            log.debug(response.text)
        except Exception as e:
            log.error(str(e))

    def post(self, request, *args, **kwargs):
        # captcha
        if not verify_recaptcha_token_from_request(request):
            return Response({'error': "Captcha verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        # get guide with slug
        slug = request.data['slug']
        propertyDict = propertyDBUtils.get_property(slug, get_language_idx_from_drf_request(request))
        if not propertyDict:
            return Response({'error': "Property not exists with slug id: " + slug}, status=status.HTTP_400_BAD_REQUEST)

        # statistics
        statisticsUtils.stat_increment_lead_count(propertyDict['_id'])

        # save request to firebase
        data = {
            "property": {
                "title": propertyDict['details']['title'],
                "price": propertyDict['details']['price_amount'],
                "price_unit": propertyDict['details']['price_unit'],
                "slug": slug
            },
            "contact": {
                "first_name": request.data['first_name'],
                "last_name": request.data['last_name'],
                "email": request.data['email'],
                "phone": request.data['phone']
            }
        }

        agent_email = "info@mallorcamagic.es"
        if "partner_email" in propertyDict.keys():
            agent_email = propertyDict['partner_email']
            # agent_email = "info@hellohere.es"       # For development only

        # vbout and firebase
        title = propertyDict['details']['title'][get_language_idx_from_drf_request(request)]
        self._send_vboat_property_request(title, request.data['first_name'],
                    request.data['last_name'], request.data['email'],  request.data['phone'], request.data['message'],
                    request.data['property_url'], agent_email, propertyDict['details']['partner'])
        self._send_vboat_agent_request(title, request.data['first_name'],
                                          request.data['last_name'], request.data['email'], request.data['phone'],
                                          request.data['message'],
                                          request.data['property_url'], agent_email, propertyDict['details']['partner'])
        return Response(data, status=status.HTTP_201_CREATED)


# Retrieve all locations
def get_all_locations(request):
    log.debug(request.GET)
    locations = firebasePropertyDB.get_locations()
    return JsonResponse({"locations": locations})

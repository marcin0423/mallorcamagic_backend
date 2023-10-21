from django.http import JsonResponse
from FirebaseUtil.FirebaseReadyContentHelpers import get_ready_contents
from rest_framework.decorators import api_view
from utils.Common import get_language_idx_from_drf_request, get_limit_from_request
from utils.Logger import log


@api_view(http_method_names=["GET"])
def get_contents(request):
    log.debug(request.GET)
    language = get_language_idx_from_drf_request(request)
    limit = get_limit_from_request(request)
    contents = get_ready_contents(limit)
    response_dict = {
        'items': contents,
        'more': len(contents) >= limit,
        'next_cursor': contents[-1]['timestamp']
    }
    return JsonResponse(response_dict)

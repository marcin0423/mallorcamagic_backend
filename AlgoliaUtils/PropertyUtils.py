from algoliasearch.search_client import SearchClient
import pymongo

ALGOLIA_APP_ID = "KGUDDRGO94"
ALGOLIA_API_KEY = "4f6febfcb22ebf358549301f480f8c8e"
ALGOLIA_INDEX_NAMES_DESC = ["Properties", "properties_price_desc", "properties_bathrooms_desc",
                            "properties_plot_size_desc", "properties_living_size_desc"]
ALGOLIA_INDEX_NAMES_ASC = ["Properties", "properties_price_asc", "properties_bathrooms_asc",
                           "properties_plot_size_asc", "properties_living_size_asc"]
ALGOLIA_SORTING_TYPES = ["timestamp", "details.price_int", "details.bathrooms",
                         "details.size_plot", "details.size_construction"]

# Start the API client
client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)

# initialize indices
algolia_indices = {"desc": {}, "asc": {}}
for idx, val in enumerate(ALGOLIA_INDEX_NAMES_ASC):
    algolia_indices["asc"][ALGOLIA_SORTING_TYPES[idx]] = client.init_index(val)

for idx, val in enumerate(ALGOLIA_INDEX_NAMES_DESC):
    algolia_indices["desc"][ALGOLIA_SORTING_TYPES[idx]] = client.init_index(val)


def __get_index_from_sort_type(sort):
    try:
        attribute = sort["by"]
        order = "asc" if sort["order"] == pymongo.ASCENDING else "desc"
        return algolia_indices[order][attribute]
    except Exception as e:
        print(e)
        return algolia_indices["desc"]["timestamp"]


def __remove_extra_fields(prop):
    try:
        del prop['objectID']
        del prop['_highlightResult']
        del prop['partner_email']
        del prop['source']
        del prop['onOff']
        del prop['blobs']
        prop["_id"] = prop["_id"]["$oid"]
    except:
        pass


def search_property(limit, start, from_price, to_price, area, prop_for, prop_type, sort, query):
    # Filter parameters
    filters = f'''details.is_enabled:true AND details.price_int >= {from_price} AND details.price_int < {to_price}'''

    # Filter area if exists
    if len(area) > 0:
        filters += f''' AND details.loc_city:"{area}"'''

    # filter for sale/rent
    if len(prop_for) > 0:
        filters += f''' AND details.category:{prop_for}'''

    # filter for type
    if len(prop_type) > 0:
        filters += f''' AND details.type:{prop_type}'''

    # Fetch results
    result = __get_index_from_sort_type(sort).search(query, {
        'filters': filters,
        'offset': start,
        'length': limit,
    })

    # Remove extra fields
    properties = []
    for prop in result['hits']:
        __remove_extra_fields(prop)
        properties.append(prop)
    return properties, result['nbHits']


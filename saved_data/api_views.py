from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from FirebaseUtil.FirebaseGuideHelpers import get_single_guide
from mongoUtils.PropertiesUtils import get_property
from mongoUtils.StatisticsUtils import stat_increment_save_count
from .models import SavedGuide, SavedProperty
from .serializers import GuideSerializer, PropertySerializer
from rest_framework.permissions import IsAuthenticated


class SavedGuideEndpoint(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': "Please login first"}, status=status.HTTP_401_UNAUTHORIZED)
        if not ("slug" in request.data.keys()):
            return Response({'error': "No slug id is provided"}, status=status.HTTP_400_BAD_REQUEST)

        # get guide with slug
        slug = request.data['slug']
        guide = get_single_guide(slug)
        if not guide:
            return Response({'error': "guide not exists with slug id: " + slug}, status=status.HTTP_400_BAD_REQUEST)

        # Save the guide
        saved_guide = SavedGuide()
        saved_guide.user = request.user
        saved_guide.slug = slug
        saved_guide.creator = guide['details']['creator']
        saved_guide.thumbnail = guide['thumbnail'][0]

        saved_guide.title_en = guide['details']['title'][0]
        saved_guide.title_es = guide['details']['title'][1]
        saved_guide.title_de = guide['details']['title'][2]

        saved_guide.short_desc_en = guide['details']['short_desc'][0]
        saved_guide.short_desc_es = guide['details']['short_desc'][1]
        saved_guide.short_desc_de = guide['details']['short_desc'][2]

        saved_guide.long_desc_en = guide['details']['long_desc'][0]
        saved_guide.long_desc_es = guide['details']['long_desc'][1]
        saved_guide.long_desc_de = guide['details']['long_desc'][2]
        try:
            saved_guide.save()
        except Exception as e:
            return Response({'error': "Unknown error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GuideSerializer(saved_guide)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': "Please login first"}, status=status.HTTP_401_UNAUTHORIZED)
        if not ("slug" in request.data.keys()) and not ("all" in request.data.keys()):
            return Response({'error': "No slug id is provided"}, status=status.HTTP_400_BAD_REQUEST)

        if "slug" in request.data.keys():
            try:
                instance = SavedGuide.objects.filter(user=request.user, slug=request.data['slug'])
                instance.delete()
            except Exception as e:
                return Response({'error': "Unable to delete: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        elif request.data['all']:
            SavedGuide.objects.filter(user=request.user).delete()
        return Response({}, status=status.HTTP_200_OK)


class SavedPropertyEndpoint(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': "Please login first"}, status=status.HTTP_401_UNAUTHORIZED)
        if not ("slug" in request.data.keys()):
            return Response({'error': "No slug id is provided"}, status=status.HTTP_400_BAD_REQUEST)

        # get guide with slug
        slug = request.data['slug']
        propertyDict = get_property(slug, 0)
        if not propertyDict:
            return Response({'error': "Property not exists with slug id: " + slug}, status=status.HTTP_400_BAD_REQUEST)

        # statistics
        stat_increment_save_count(propertyDict['_id'])

        # Save the guide
        prop = SavedProperty()
        prop.user = request.user
        prop.slug = slug
        prop.partner = propertyDict["details"]["partner"]
        prop.thumbnail = propertyDict["thumbnail"][0]

        prop.title = propertyDict['details']['title'][0]
        prop.description = propertyDict['details']['description'][0]

        prop.price_unit = propertyDict['details']['price_unit']
        prop.price_amount = propertyDict['details']['price_amount']

        prop.area = propertyDict['details']['size_plot']
        prop.bathrooms = propertyDict['details']['bathrooms']
        prop.bedrooms = propertyDict['details']['bedrooms']

        try:
            prop.save()
        except Exception as e:
            return Response({'error': "Unknown error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PropertySerializer(prop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': "Please login first"}, status=status.HTTP_401_UNAUTHORIZED)
        if not ("slug" in request.data.keys()) and not ("all" in request.data.keys()):
            return Response({'error': "No slug id is provided"}, status=status.HTTP_400_BAD_REQUEST)

        if "slug" in request.data.keys():
            try:
                instance = SavedProperty.objects.filter(user=request.user, slug=request.data['slug'])
                instance.delete()
            except Exception as e:
                return Response({'error': "Unable to delete: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        elif request.data['all']:
            SavedProperty.objects.filter(user=request.user).delete()
        return Response({}, status=status.HTTP_200_OK)


class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20
    ordering = "-timestamp"


class SavedGuideList(ListAPIView):
    queryset = SavedGuide.objects.all()
    serializer_class = GuideSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user=self.request.user)


class SavedPropertyList(ListAPIView):
    queryset = SavedProperty.objects.all()
    serializer_class = PropertySerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user=self.request.user)

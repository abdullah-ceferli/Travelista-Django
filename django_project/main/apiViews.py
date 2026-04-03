from main.models import *
from main.serializers import *
from rest_framework import generics, pagination, filters

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class DestinationListAPI(generics.ListAPIView):
    queryset = Destinations.objects.all()
    serializer_class = DestinationSerializer
    pagination_class = StandardResultsSetPagination


class UserContactListAPI(generics.ListAPIView):
    queryset = UserContact.objects.filter(check_box=True).order_by('-pub_date')
    serializer_class = UserContactSerializer
    pagination_class = StandardResultsSetPagination

class HotelsListAPI(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelsSerializer
    pagination_class = StandardResultsSetPagination 

class UserMessageListAPI(generics.ListAPIView):
    queryset = UserMessage.objects.filter(check_box=True).order_by('-pub_date')
    serializer_class = UserMessageSerializer
    pagination_class = StandardResultsSetPagination


class UserDataListAPI(generics.ListAPIView):
    queryset = SignUp.objects.all()
    serializer_class = UserDataSerializer
    pagination_class = StandardResultsSetPagination


class BlogPostListAPI(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-pub_date')
    serializer_class = BlogPostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'tags__name']
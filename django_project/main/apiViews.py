from rest_framework import generics
from main.models import *
from main.serializers import *
from rest_framework import generics, pagination

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class DestinationListAPI(generics.ListAPIView):
    queryset = Destinations.objects.all()
    serializer_class = DestinationSerializer
    pagination_class = StandardResultsSetPagination


class UserContactListAPI(generics.ListAPIView):
    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer
    pagination_class = StandardResultsSetPagination

class HotelsListAPI(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelsSerializer
    pagination_class = StandardResultsSetPagination 

class UserMessageListAPI(generics.ListAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    pagination_class = StandardResultsSetPagination

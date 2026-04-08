from main.models import *
from main.serializers import *
from rest_framework import generics, pagination, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

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


class GetOrCreateThread(APIView):
    def get(self, request, target_user_id):
        try:
            my_session_id = request.session.get('user_id')
            
            if not my_session_id:
                return Response({"error": "Session expired. Please login again."}, status=401)

            me = SignUp.objects.filter(id=my_session_id).first()
            other = SignUp.objects.filter(id=target_user_id).first()

            if not me or not other:
                return Response({"error": "User profiles not found"}, status=404)
            
            thread = Thread.objects.filter(
                (Q(first_person=me) & Q(second_person=other)) |
                (Q(first_person=other) & Q(second_person=me))
            ).first()

            if not thread:
                thread = Thread.objects.create(first_person=me, second_person=other)
            
            return Response({"thread_id": thread.id}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class SendMessageAPI(APIView):
    def post(self, request):
        try:
            my_session_id = request.session.get('user_id')
            me = SignUp.objects.get(id=my_session_id)
            
            thread_id = request.data.get('thread_id')
            text = request.data.get('message')

            ChatMessage.objects.create(
                thread_id=thread_id,
                user=me, 
                message=text
            )
            return Response({"status": "success"}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class MessageListAPI(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    def get_queryset(self):
        return ChatMessage.objects.filter(thread_id=self.kwargs['thread_id']).order_by('timestamp')
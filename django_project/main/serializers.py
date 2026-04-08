from rest_framework import serializers
from main.models import *


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name']


class DestinationAmenitySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='amenity.name')

    class Meta:
        model = DestinationsAmenity
        fields = ['name', 'text']


class DestinationSerializer(serializers.ModelSerializer):
    amenities_detail = DestinationAmenitySerializer(
        source='destinationsamenity_set', many=True, read_only=True)

    class Meta:
        model = Destinations
        fields = ['id', 'name', 'location', 'destinations_img',
                  'price_per_person', 'amenities_detail']


class UserContactSerializer(serializers.ModelSerializer):
    user_img = serializers.ReadOnlyField(source='get_avatar')

    class Meta:
        model = UserContact
        fields = ['id', 'name', 'surname', 'message', 'user_img', 
                  'pub_date', 'check_box', 'email', 'subject', 'stars']


class HotelsAmenitySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='amenity.name')

    class Meta:
        model = HotelAmenity
        fields = ['name']


class HotelsSerializer(serializers.ModelSerializer):
    amenities_detail = HotelsAmenitySerializer(
        source='hotelamenity_set', many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'hotel_img',
                  'price_per_night', 'stars', 'amenities_detail']


class UserMessageSerializer(serializers.ModelSerializer):
    user_img = serializers.ReadOnlyField(source='get_avatar')
    pub_date = serializers.DateTimeField(format="%B %d, %Y")

    class Meta:
        model = UserMessage
        fields = ['id', 'name', 'message', 'user_img', 'pub_date', 
                  'ip_address', 'check_box', 'email', 'subject']


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUp
        fields = [
            'id', 'username', 'email', 'phone', 'pub_date',
            'ip_address', 'name', 'last_name', 'age',
            'location', 'about_me', 'contact_email',
            'profile_img', 'writer'
        ]


class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='get_author_name', read_only=True)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class ImageUrlSerializer(serializers.ModelSerializer):
        class Meta:
            model = BlogPost
            fields = ['id', 'title', 'content', 'author_name', 'pub_date', 'blog_img', 'tags', 'view_count']

    class Meta:
        model = BlogPost
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'user_id', 'username', 'message', 'timestamp']
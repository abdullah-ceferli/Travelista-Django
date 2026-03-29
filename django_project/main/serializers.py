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
    amenities_detail = DestinationAmenitySerializer(source='destinationsamenity_set', many=True, read_only=True)

    class Meta:
        model = Destinations
        fields = ['id', 'name', 'location', 'destinations_img', 'price_per_person', 'amenities_detail']

class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContact
        fields = ['id', 'name', 'surname', 'message', 'user_img', 'pub_date', 'ip_address', 'check_box', 'email', 'subject', 'stars']



class HotelsAmenitySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='amenity.name')

    class Meta:
        model = HotelAmenity
        fields = ['name']

class HotelsSerializer(serializers.ModelSerializer):
    amenities_detail = HotelsAmenitySerializer(source='hotelamenity_set', many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'hotel_img', 'price_per_night', 'stars', 'amenities_detail']


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = ['id', 'name', 'message', 'user_img', 'pub_date', 'ip_address', 'check_box', 'email', 'subject']
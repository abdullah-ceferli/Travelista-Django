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

class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = ['name', 'message', 'user_img', 'pub_date']
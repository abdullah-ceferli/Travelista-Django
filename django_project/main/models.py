import math
from pyexpat import model

from django.db import models

# Create your models here.


class TrashBin(models.Model):
    class Meta:
        managed = False
        verbose_name = "Trash Bin"
        verbose_name_plural = "Trash Bin"






#  hotels model
class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    stars = models.PositiveSmallIntegerField(default=5)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    review_count = models.PositiveIntegerField(default=0)
    hotel_img = models.ImageField(
        upload_to='hotel_images/', null=True, blank=True)

    amenities = models.ManyToManyField(Amenity, through='HotelAmenity', related_name='hotels')

    def __str__(self):
        return self.name


class HotelAmenity(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    is_available = models.BooleanField(
        default=False, verbose_name="Available (Yes/No)")

    def __str__(self):
        return f"{self.hotel.name} - {self.amenity.name}"





# destinations models
class Destinations(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    destinations_img = models.ImageField(
        upload_to='destinations_images/', null=True, blank=True)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)


    amenities = models.ManyToManyField(Amenity, through='DestinationsAmenity', related_name='destinations')

    def __str__(self):
        return self.name
    

class DestinationsAmenity(models.Model):
    destination = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    text = models.CharField(
        max_length=50, default="", verbose_name="Available Text")

    def __str__(self):
        return f"{self.destination.name} - {self.amenity.name}"






# user model
class UserContactManager(models.Manager):
    def get_carousel_data(self):
        messages = self.filter(check_box=True).order_by('-id')[:8]
        count = messages.count()
        
        user_messages_carusel = None
        dot_count = 0

        if count >= 4:
            user_messages_carusel = messages
            dot_count = math.ceil(count / 2)

        return {
            'user_messages_carusel': user_messages_carusel,
            'dot_count': range(dot_count),
        }
    


class UserMessage(models.Model):
    name = models.CharField(max_length=100)

    email = models.EmailField(max_length=150)

    subject = models.CharField(max_length=200)

    message = models.TextField()

    check_box = models.BooleanField(default=False)

    user_img = models.ImageField(
        upload_to='user_images/', null=True, blank=True)

    pub_date = models.DateTimeField('date published', null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.email}), Created at - {self.pub_date}"
    


class UserContact(models.Model):
    name = models.CharField(max_length=100)

    surname = models.CharField(max_length=100)

    email = models.EmailField(max_length=150)

    subject = models.CharField(max_length=200)

    message = models.TextField()

    check_box = models.BooleanField(default=False)

    user_img = models.ImageField(
        upload_to='user_images/', null=True, blank=True)

    stars = models.PositiveSmallIntegerField(default=5)

    pub_date = models.DateTimeField('date published', null=True, blank=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    objects = UserContactManager()

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}"
    

class SignUp(models.Model):
    username = models.CharField(max_length=100)

    email = models.EmailField(max_length=150)

    password = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    pub_date = models.DateTimeField('date published', null=True, blank=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.email})"
    
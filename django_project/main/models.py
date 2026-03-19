from django.db import models

# Create your models here.


class TrashBin(models.Model):
    class Meta:
        managed = False
        verbose_name = "Trash Bin"
        verbose_name_plural = "Trash Bin"


class UserMessage(models.Model):
    name = models.CharField(max_length=100)

    surname = models.CharField(max_length=100)

    email = models.EmailField(max_length=150)

    subject = models.CharField(max_length=200)

    message = models.TextField()

    check_box = models.BooleanField(default=False)

    import_time = models.DateTimeField(auto_now_add=True, null=True)

    user_img = models.ImageField(
        upload_to='user_images/', null=True, blank=True)

    user_ip = models.GenericIPAddressField(null=True, blank=True)

    stars = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}"


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

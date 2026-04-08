from django.templatetags.static import static
from django.db import models
from django.conf import settings

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
class SignUp(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    password = models.CharField()
    phone = models.CharField(max_length=20)
    pub_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    device_type = models.CharField(max_length=50, null=True)     
    os_family = models.CharField(max_length=50, null=True)    
    os_version = models.CharField(max_length=50, null=True) 
    browser_family = models.CharField(max_length=50, null=True) 
    browser_version = models.CharField(max_length=50, null=True)

    name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    
    about_me = models.TextField(null=True, blank=True) 
    contact_email = models.EmailField(max_length=150, null=True, blank=True)
    profile_img = models.ImageField(upload_to='user_images/', default='user-images/default.jpg', null=True, blank=True)

    writer = models.CharField(max_length=100, default="Senior blog writer")

    def __str__(self):
        return f"{self.username} ({self.email})"


class Tag(models.Model): 
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(SignUp, on_delete=models.CASCADE, related_name='blog_posts')
    pub_date = models.DateTimeField(auto_now_add=True)
    blog_img = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='blog_posts', blank=True)
    
    def get_author_name(self):
        if self.author:
            return f"{self.author.name} {self.author.last_name or ''}".strip()
        return f"Guest {self.id}"

    def __str__(self):
        return self.title


class UserMessage(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments')
    user_profile = models.ForeignKey('SignUp', on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    check_box = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True) 
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    user_img = models.ImageField(upload_to='user_images/', null=True, blank=True)

    @property
    def get_avatar(self):
        if self.user_img and hasattr(self.user_img, 'url'):
            return self.user_img.url
        if self.user_profile and self.user_profile.profile_img:
            return self.user_profile.profile_img.url
        return static('img/user-img/default.jpg')
    
    def __str__(self):
        return f"{self.name} ({self.email}), Created at - {self.pub_date}"
    

class UserContact(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    check_box = models.BooleanField(default=False)
    user_img = models.ImageField(upload_to='user_images/', null=True, blank=True)
    stars = models.PositiveSmallIntegerField(default=5)
    pub_date = models.DateTimeField('date published', null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    @property
    def get_avatar(self):
        if self.user_img and hasattr(self.user_img, 'url'):
            try:
                return self.user_img.url
            except:
                return static('img/user-img/default.jpg')
        return static('img/user-img/default.jpg')

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}"
  
    
class Thread(models.Model):
    first_person = models.ForeignKey(SignUp, on_delete=models.CASCADE, related_name='thread_first')
    second_person = models.ForeignKey(SignUp, on_delete=models.CASCADE, related_name='thread_second')
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(SignUp, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
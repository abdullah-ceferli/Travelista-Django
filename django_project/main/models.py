from django.db import models

# Create your models here.


class TrashBin(models.Model):
    class Meta:
        managed = False
        verbose_name = "Trash Bin"
        verbose_name_plural = "Trash Bin"

class UserMessage(models.Model):
    name = models.CharField()

    surname = models.CharField()

    email = models.CharField()

    subject = models.CharField()

    message = models.TextField()

    check_box = models.BooleanField(default=False)

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}"


class ContactInfo(models.Model):
    location = models.CharField(max_length=25)

    location2 = models.CharField(max_length=25)

    phone_number = models.CharField(max_length=20)

    phone_description = models.CharField(max_length=50)

    email = models.EmailField(max_length=50)

    email_description = models.CharField(max_length=50)

    def __str__(self):
        return f"Location: {self.location}, Email: {self.email}"

class ContactInfo(models.Model):
    location = models.CharField(max_length=25)

    location2 = models.CharField(max_length=25)

    phone_number = models.CharField(max_length=20)

    phone_description = models.CharField(max_length=50)

    email = models.EmailField(max_length=50)

    email_description = models.CharField(max_length=50)

    def __str__(self):
        return f"Location: {self.location}, Email: {self.email}"

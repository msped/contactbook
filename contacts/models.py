from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Contacts(models.Model):
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        default="profile_pictures/default.jpg"
    )
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phoneNumber = PhoneNumberField(blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

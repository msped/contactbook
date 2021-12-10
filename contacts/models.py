from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Contacts(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phoneNumber = PhoneNumberField(blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

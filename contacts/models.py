from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Contacts(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phoneNumber = PhoneNumberField(blank=False, null=False, unique=True, max_length=11)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

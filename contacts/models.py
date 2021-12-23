from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Contacts(models.Model):
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        default="profile_pictures/default.jpg"
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class PhoneNumbers(models.Model):

    class Options(models.TextChoices):
        HOME = 'home', 'Home'
        MOBILE = 'mob', 'Mobile'
        WORK = 'work', 'Work'

    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE, related_name="phone_number")
    phonenumber_type = models.CharField(max_length=4, choices=Options.choices, default='1')
    phoneNumber = PhoneNumberField(blank=False, null=False)

    def __str__(self):
        return f'{self.contact.name}: {self.get_phonenumber_type_display()} - {self.phoneNumber}'

class Emails(models.Model):

    class Options(models.TextChoices):
        HOME = 'pers', 'Personal'
        WORK = 'work', 'Work'

    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE, related_name="email")
    email_type = models.CharField(max_length=4, choices=Options.choices, default='1')
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return f'{self.contact.name}: {self.get_email_type_display()} - {self.email}'

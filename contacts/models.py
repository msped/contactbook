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
        HOME = '1', 'Home'
        MOBILE = '2', 'Mobile'
        WORK = '3', 'Work'

    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE, related_name="phone_number")
    phonenumber_type = models.CharField(max_length=4, choices=Options.choices, default='1')
    phoneNumber = PhoneNumberField(blank=False, null=False, unique=True)

    def __str__(self):
        return f'{self.contact.name}: {self.phonenumber_type} - {self.phoneNumber}'

    # def clean(self):
    #     home = PhoneNumbers.objects.get(contact=self.contact, contact_type='')

class Emails(models.Model):

    class Options(models.TextChoices):
        HOME = '1', 'Personal'
        WORK = '2', 'Work'

    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE, related_name="email")
    email_type = models.CharField(max_length=4, choices=Options.choices, default='1')
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return f'{self.contact.name}: {self.email_type} - {self.email}'

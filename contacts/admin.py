from django.contrib import admin
from .models import Contacts, PhoneNumbers, Emails

# Register your models here.

class EmailInline(admin.TabularInline):
    model = Emails

class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumbers

class ContactAdmin(admin.ModelAdmin):
    inlines = [PhoneNumberInline, EmailInline,]

admin.site.register(Contacts, ContactAdmin)
admin.site.register(PhoneNumbers)
admin.site.register(Emails)

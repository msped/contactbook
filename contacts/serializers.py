from rest_framework import serializers
from .models import Contacts, Emails, PhoneNumbers

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumbers
        fields = ['id', 'phonenumber_type', 'phoneNumber']

        def validate(self, data):
            if PhoneNumbers.objects.get(data['phoneNumber']).exists():
                return serializers.ValidationError(
                    f"Contact with phone number {data['phoneNumber']} already exists."
                )
            return data

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields = ['id', 'email_type', 'email']

        def validate(self, data):
            if Emails.objects.get():
                return serializers.ValidationError(
                    f"Contact with the email {data['email']} already exists."
                )
            return data

class ContactDetailSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberSerializer(many=True)
    email = EmailSerializer(many=True)

    class Meta:
        model = Contacts
        fields = [
            'id',
            'profile_picture',
            'name',
            'phone_number',
            'email'
        ]

class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'profile_picture', 'name']

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'profile_picture']

class ContactNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'name']

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Contacts, Emails, PhoneNumbers


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumbers
        fields = ['id', 'contact', 'phonenumber_type', 'phoneNumber']

    def validate(self, attrs):
        if PhoneNumbers.objects.filter(contact_id=attrs['contact'], phoneNumber=attrs['phoneNumber']).exists():
            raise serializers.ValidationError(
                f"Contact with the phone number {attrs['phoneNumber']} already exists."
            )

        if PhoneNumbers.objects.filter(contact=attrs['contact'],
                                 phonenumber_type=attrs['phonenumber_type']).exists():
            raise serializers.ValidationError(
                'Contact already has a phone number with this type.'
            )
        return attrs

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields = ['id', 'contact', 'email_type', 'email']

    def validate(self, attrs):
        if Emails.objects.filter(contact_id=attrs['contact'], email=attrs['email']).exists():
            raise serializers.ValidationError(
                f"Contact with the email {attrs['email']} already exists."
            )

        if Emails.objects.filter(contact=attrs['contact'],
                                 email_type=attrs['email_type']).exists():
            raise serializers.ValidationError(
                'Contact already has an email with this type.'
            )
        return attrs

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

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        owner = User.objects.get(id=user_id)
        validated_data['owner'] = owner
        contact = Contacts(**validated_data)
        contact.save()
        return contact

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'profile_picture']

class ContactNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'name']

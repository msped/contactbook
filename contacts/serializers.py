from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from .models import Contacts, Emails, PhoneNumbers


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumbers
        fields = ['id', 'contact', 'type', 'data']

    def validate(self, attrs):
        url_id = self.context.get('phonenumber_id')
        if PhoneNumbers.objects.filter(~Q(id=url_id), data=attrs['data']).exists():
            raise serializers.ValidationError(
                f"Contact with the phone number {attrs['data']} already exists."
            )

        if PhoneNumbers.objects.filter(~Q(id=url_id), contact=attrs['contact'],
                                 type=attrs['type']).exists():
            raise serializers.ValidationError(
                'Contact already has a phone number with this type.'
            )
        return attrs

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields = ['id', 'contact', 'type', 'data']

    def validate(self, attrs):
        url_id = self.context.get('email_id')
        if Emails.objects.filter(~Q(id=url_id), data=attrs['data']).exists():
            raise serializers.ValidationError(
                f"Contact with the email {attrs['data']} already exists."
            )

        if Emails.objects.filter(~Q(id=url_id), contact=attrs['contact'],
                                 type=attrs['type']).exists():
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

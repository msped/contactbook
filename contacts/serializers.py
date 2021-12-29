from django.contrib.auth.models import User
from rest_framework import serializers
from django.db.models import Q
from .models import Contacts, Emails, PhoneNumbers

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumbers
        fields = ['id', 'contact', 'phonenumber_type', 'phoneNumber']

    def validate(self, attrs):
        url_id = self.context.get('phonenumber_id')
        if PhoneNumbers.objects.filter(~Q(id=url_id), phoneNumber=attrs['phoneNumber']).exists():
            raise serializers.ValidationError(
                f"Contact with the phone number {attrs['phoneNumber']} already exists."
            )

        if PhoneNumbers.objects.filter(~Q(id=url_id), contact=attrs['contact'],
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
        url_id = self.context.get('email_id')
        if Emails.objects.filter(~Q(id=url_id), email=attrs['email']).exists():
            raise serializers.ValidationError(
                f"Contact with the email {attrs['email']} already exists."
            )

        if Emails.objects.filter(~Q(id=url_id), contact=attrs['contact'],
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

from rest_framework import serializers
from .models import Contacts, Emails, PhoneNumbers

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumbers
        fields = ['id', 'contact', 'phonenumber_type', 'phoneNumber']

    def create(self, validated_data):
        if PhoneNumbers.objects.filter(contact=validated_data['contact'],
                                 phonenumber_type=validated_data['phonenumber_type']).exists():
            raise serializers.ValidationError(
                'Contact already has a phone number with this type.'
            )
        number = PhoneNumbers.objects.create(**validated_data)
        return number

    def validate(self, attrs):
        if PhoneNumbers.objects.filter(phoneNumber=attrs['phoneNumber']).exists():
            raise serializers.ValidationError(
                f"Contact with the phone number {attrs['phoneNumber']} already exists."
            )
        return attrs

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields = ['id', 'contact', 'email_type', 'email']

    def create(self, validated_data):
        if Emails.objects.filter(contact=validated_data['contact'],
                                 email_type=validated_data['email_type']).exists():
            raise serializers.ValidationError(
                'Contact already has an email with this type.'
            )
        email = Emails.objects.create(**validated_data)
        return email

    def validate(self, attrs):
        if Emails.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                f"Contact with the email {attrs['email']} already exists."
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

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'profile_picture']

class ContactNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'name']

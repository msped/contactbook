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

class ContactSerializer(serializers.ModelSerializer):
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

    def update(self, instance, validated_data):
        phonenumber_data = validated_data.pop('phone_number')
        phone_numbers = (instance.phone_number).all()
        phone_numbers = list(phone_numbers)
        email_data = validated_data.pop('email')
        emails = (instance.email).all()
        emails = list(emails)
        instance.name = validated_data.get('name', instance.name)

        for number in phonenumber_data:
            phone_number = phone_numbers.pop(0)
            phone_number.id = number.get('id', phone_number.id)
            phone_number.phonenumber_type = number.get(
                'phonenumber_type',
                phone_number.phonenumber_type
            )
            phone_number.phoneNumber = number.get('phoneNumber', phone_number.phoneNumber)
            phone_number.save()

        for mail in email_data:
            email = emails.pop(0)
            email.id = mail.get('id', email.id)
            email.email_type = mail.get(
                'email_type',
                email.email_type
            )
            email.email = mail.get('email', email.email)
            email.save()
        return instance

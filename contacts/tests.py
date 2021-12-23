import io
import json
import shutil
import tempfile

from django.test import override_settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Contacts, Emails, PhoneNumbers

MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ContactBookViewsTestCase(APITestCase):

    def setUp(self):
        """Set up database with prepopulated data"""
        Contacts.objects.create(
            name="Matt Edwards"
        )
        contact = Contacts.objects.get(id=1)
        PhoneNumbers.objects.create(
            contact=contact,
            phonenumber_type= "home",
            phoneNumber= "+447964974125"
        )
        Emails.objects.create(
            contact=contact,
            email_type="pers",
            email='matt@mspe.me'
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def generate_photo_file(self, file_name):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = f'{file_name}.png'
        file.seek(0)
        return file

    def create_new_contact_default_image(self):
        response = self.client.post(
            '/api/contacts/',
            {
                "name": "John Doe"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 2,
                "profile_picture": "/media/profile_pictures/default.jpg",
                "name": "John Doe",
            }
        )

    def create_new_contact_with_image(self):
        photo_file = self.generate_photo_file(file_name="test_1")
        response = self.client.post(
            '/api/contacts/',
            {
                "profile_picture": photo_file,
                "name": "Jane Doe"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 3,
                "profile_picture": "/media/profile_pictures/test_1.png",
                "name": "Jane Doe"
            }
        )

    def create_new_phone_number(self):
        response = self.client.post(
            '/api/contacts/phone-number',
            {
                "contact": 1,
                "phonenumber_type": "mob",
                "phoneNumber": "+447936498745"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 2,
                "contact": 1,
                "phonenumber_type": "mob",
                "phoneNumber": "+447936498745"
            }
        )

    def create_new_email(self):
        response = self.client.post(
            '/api/contacts/email',
            {
                "contact": 1,
                "email_type": "work",
                "email": "test@mspe.me"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 2,
                "contact": 1,
                "email_type": "work",
                "email": "test@mspe.me"
            }
        )

    def create_phone_number_that_already_exists(self):
        response = self.client.post(
            '/api/contacts/phone-number',
            {
                "contact": 1,
                "phonenumber_type": "mob",
                "phoneNumber": "+447964974125"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {'non_field_errors': ['Contact with the phone number +447964974125 already exists.']}
        )

    def create_email_that_already_exists(self):
        response = self.client.post(
            '/api/contacts/email',
            {
                "contact": 1,
                "email_type": "work",
                "email": "matt@mspe.me"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {'non_field_errors': ['Contact with the email matt@mspe.me already exists.']}
        )

    def request_contact_that_exists(self):
        response = self.client.get('/api/contacts/1')
        self.assertEqual(
            {
                "id": 1,
                "profile_picture": "/media/profile_pictures/default.jpg",
                "name": "Matt Edwards",
                "phone_number": [
                    {
                        "id": 1,
                        "contact": 1,
                        "phonenumber_type": "home",
                        "phoneNumber": "+447964974125"
                    }
                ],
                "email": [
                    {
                        "id": 1,
                        "contact": 1,
                        "email_type": "pers",
                        "email": "matt@mspe.me"
                    }
                ]
            },
            json.loads(response.content)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def request_contact_that_doesnt_exist(self):
        response = self.client.get('/api/contacts/50')
        self.assertEqual(
            {
                "detail": "Not found."
            },
            json.loads(response.content)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def list_all_contacts(self):
        response = self.client.get('/api/contacts/')
        self.assertEqual(
            json.loads(response.content),
            [
                {
                    "id": 1,
                    "profile_picture": "http://testserver/media/profile_pictures/default.jpg",
                    "name": "Matt Edwards"
                },
                {
                    "id": 2,
                    "profile_picture": "http://testserver/media/profile_pictures/default.jpg",
                    "name": "John Doe"
                },
                {
                    "id": 3,
                    "profile_picture": "http://testserver/media/profile_pictures/test_1.png",
                    "name": "Jane Doe"
                }
            ]
        )

    def update_contact_name(self):
        response = self.client.put(
            '/api/contacts/name/1',
            {"name": "Matthew Edwards"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 1,
                "name": "Matthew Edwards"
            }
        )

    def update_phone_number(self):
        response = self.client.put(
            '/api/contacts/phone-number/1',
            {
                "contact": 1,
                "phonenumber_type": "mob",
                "phoneNumber": "+447936792548"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 1,
                "contact": 1,
                "phonenumber_type": "mob",
                "phoneNumber": "+447936792548"
            }
        )

    def update_email(self):
        response = self.client.put(
            '/api/contacts/email/1',
            {
                "contact": 1,
                "email_type": "pers",
                "email": "matthew@mspe.me"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 1,
                "contact": 1,
                "email_type": "pers",
                "email": "matthew@mspe.me"
            }
        )

    def adding_same_phone_type(self):
        response = self.client.post(
            '/api/contacts/phone-number',
            {
                "contact": 1,
                "phonenumber_type": "mob",
                "phoneNumber": "+447964498453"

            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            ['Contact already has a phone number with this type.']
        )

    def adding_same_email_type(self):
        response = self.client.post(
            '/api/contacts/email',
            {
                "contact": 1,
                "email_type": "pers",
                "email": "testing@mspe.me"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            ['Contact already has an email with this type.']
        )

    def delete_contact_with_default_image(self):
        """default.jpg should not be deleted"""
        response = self.client.delete('/api/contacts/2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_phone_number(self):
        response = self.client.delete(
            '/api/contacts/phone-number/1'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def delete_email(self):
        response = self.client.delete(
            '/api/contacts/email/1'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def update_profile_picture(self):
        photo_file = self.generate_photo_file(file_name="new_pic")
        response = self.client.put(
            '/api/contacts/profile-picture/1',
            { 'profile_picture': photo_file },
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 1,
                "profile_picture": "http://testserver/media/profile_pictures/new_pic.png"
            }
        )

    def create_contact_error(self):
        response = self.client.post(
            '/api/contacts/',
            {
                "first_name": "Matt"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "name": ["This field is required."]
            }
        )

    def put_phone_number_error(self):
        response = self.client.put(
            '/api/contacts/phone-number/1',
            {
                "phone-number": "+447954793156"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "contact": ["This field is required."],
                "phoneNumber": ["This field is required."]
            }
        )

    def put_email_error(self):
        response = self.client.put(
            '/api/contacts/email/1',
            {
                "email": "+447954793156"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "contact": ["This field is required."],
                "email": ["Enter a valid email address."]
            }
        )

    def test_in_order(self):
        self.create_new_contact_default_image()
        self.create_new_contact_with_image()
        self.request_contact_that_exists()
        self.request_contact_that_doesnt_exist()
        self.create_phone_number_that_already_exists()
        self.create_email_that_already_exists()
        self.list_all_contacts()
        self.create_new_phone_number()
        self.create_new_email()
        self.update_contact_name()
        self.update_phone_number()
        self.update_email()
        self.adding_same_phone_type()
        self.adding_same_email_type()
        self.update_profile_picture()
        self.create_contact_error()
        self.put_phone_number_error()
        self.put_email_error()
        self.delete_contact_with_default_image()
        self.delete_phone_number()
        self.delete_email()

class ContactBookModelsTestCase(APITestCase):

    def setUp(self):
        """Set up database with prepopulated data"""
        Contacts.objects.create(
            name="Matt Edwards",
        )

    def generate_photo_file(self, file_name):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = f'{file_name}.png'
        file.seek(0)
        return file

    def test_contact_str(self):
        contact = Contacts.objects.get(id=1)
        self.assertEqual(str(contact), "Matt Edwards")

    def test_create_contact_without_image(self):
        contact = Contacts(
            name="John Doe",
        )
        contact.save()

        self.assertEqual(contact.profile_picture.url, "/media/profile_pictures/default.jpg")
        self.assertEqual(contact.name, "John Doe")

    def create_phonenumber(self):
        contact = Contacts.objects.get(name="Matt Edwards")
        phone_number = PhoneNumbers(
            contact=contact,
            phonenumber_type='home',
            phoneNumber="+44796411359"
        )
        phone_number.save()

        self.assertEqual(phone_number.contact.name, "Matt Edwards")
        self.assertEqual(phone_number.phonenumber_type, "home")
        self.assertEqual(phone_number.phoneNumber, "+44796411359")

    def phonenumber_str(self):
        phonenumber = PhoneNumbers.objects.get(id=1)
        self.assertEqual(str(phonenumber), "Matt Edwards: Home - +44796411359")

    def create_email(self):
        contact = Contacts.objects.get(name="Matt Edwards")
        email = Emails(
            contact=contact,
            email_type='work',
            email="matt@mspe.me"
        )
        email.save()

        self.assertEqual(email.contact.name, "Matt Edwards")
        self.assertEqual(email.email_type, "work")
        self.assertEqual(email.email, "matt@mspe.me")

    def email_str(self):
        email = Emails.objects.get(id=1)
        self.assertEqual(str(email), "Matt Edwards: Work - matt@mspe.me")

    def test_in_order(self):
        self.create_phonenumber()
        self.phonenumber_str()
        self.create_email()
        self.email_str()

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
            phonenumber_type= "1",
            phoneNumber= "+447964974125"
        )
        Emails.objects.create(
            contact=contact,
            email_type="1",
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
                        "phonenumber_type": "1",
                        "phoneNumber": "+447964974125"
                    }
                ],
                "email": [
                    {
                        "id": 1,
                        "email_type": "1",
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

    def delete_contact(self):
        response = self.client.delete('/api/contacts/2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_in_order(self):
        self.create_new_contact_default_image()
        self.create_new_contact_with_image()
        self.request_contact_that_exists()
        self.request_contact_that_doesnt_exist()
        self.list_all_contacts()
        self.delete_contact()

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
            phonenumber_type='1',
            phoneNumber="+44796411359"
        )
        phone_number.save()

        self.assertEqual(phone_number.contact.name, "Matt Edwards")
        self.assertEqual(phone_number.phonenumber_type, "1")
        self.assertEqual(phone_number.phoneNumber, "+44796411359")

    def phonenumber_str(self):
        phonenumber = PhoneNumbers.objects.get(id=1)
        self.assertEqual(str(phonenumber), "Matt Edwards: Home - +44796411359")

    def create_email(self):
        contact = Contacts.objects.get(name="Matt Edwards")
        email = Emails(
            contact=contact,
            email_type='2',
            email="matt@mspe.me"
        )
        email.save()

        self.assertEqual(email.contact.name, "Matt Edwards")
        self.assertEqual(email.email_type, "2")
        self.assertEqual(email.email, "matt@mspe.me")

    def email_str(self):
        email = Emails.objects.get(id=1)
        self.assertEqual(str(email), "Matt Edwards: Work - matt@mspe.me")

    def test_in_order(self):
        self.create_phonenumber()
        self.phonenumber_str()
        self.create_email()
        self.email_str()

import io
import json
import shutil
import tempfile

from django.test import override_settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Contacts

MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ContactBookViewsTestCase(APITestCase):

    def setUp(self):
        """Set up database with prepopulated data"""
        Contacts.objects.create(
            name="Matt Edwards",
            email="matt@mspe.me",
            phoneNumber="+447943337410"
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
                "name": "John Doe",
                "email": "john.doe@test.me",
                "phoneNumber": "+447968461978"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 2,
                "profile_picture": "/media/profile_pictures/default.jpg",
                "name": "John Doe",
                "email": "john.doe@test.me",
                "phoneNumber": "+447968461978"
            }
        )

    def create_new_contact_with_image(self):
        photo_file = self.generate_photo_file(file_name="test_1")
        response = self.client.post(
            '/api/contacts/',
            {
                "profile_picture": photo_file,
                "name": "Jane Doe",
                "email": "jane.doe@test.me",
                "phoneNumber": "+447968456978"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 3,
                "profile_picture": "/media/profile_pictures/test_1.png",
                "name": "Jane Doe",
                "email": "jane.doe@test.me",
                "phoneNumber": "+447968456978"
            }
        )

    def request_contact_that_exists(self):
        response = self.client.get('/api/contacts/1')
        self.assertEqual(
            {
                "id": 1,
                "profile_picture": "/media/profile_pictures/default.jpg",
                "name": "Matt Edwards",
                "email": "matt@mspe.me",
                "phoneNumber": "+447943337410"
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

    def contact_with_existing_phonenumber(self):
        response = self.client.post(
            '/api/contacts/',
            {
                "name": "Dave Smith",
                "email": "dave.smith@gmail.com",
                "phoneNumber": "+447943337410"
            }
        )
        self.assertEqual(
            json.loads(response.content),
            {
                "phoneNumber": [
                    "contacts with this phoneNumber already exists."
                ]
            }
        )

    def list_all_contacts(self):
        response = self.client.get('/api/contacts/')
        self.assertEqual(
            json.loads(response.content),
            [
                {
                    "id": 1,
                    "profile_picture": "http://testserver/media/profile_pictures/default.jpg",
                    "name": "Matt Edwards",
                    "email": "matt@mspe.me",
                    "phoneNumber": "+447943337410"
                },
                {
                    "id": 2,
                    "profile_picture": "http://testserver/media/profile_pictures/default.jpg",
                    "name": "John Doe",
                    "email": "john.doe@test.me",
                    "phoneNumber": "+447968461978"
                },
                {
                    "id": 3,
                    "profile_picture": "http://testserver/media/profile_pictures/test_1.png",
                    "name": "Jane Doe",
                    "email": "jane.doe@test.me",
                    "phoneNumber": "+447968456978"
                }
            ]
        )

    def update_contact(self):
        photo_file = self.generate_photo_file(file_name="test_2")
        response = self.client.put(
            '/api/contacts/1',
            {
                "profile_picture": photo_file,
                "name": "Matthew Edwards",
                "email": "matt@mspe.me",
                "phoneNumber": "+447943337410"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 1,
                "profile_picture": "/media/profile_pictures/test_2.png",
                "name": "Matthew Edwards",
                "email": "matt@mspe.me",
                "phoneNumber": "+447943337410"
            }
        )

    def delete_contact(self):
        response = self.client.delete('/api/contacts/2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            ["Contact John Doe has been deleted"]
        )

    def test_in_order(self):
        self.create_new_contact_default_image()
        self.create_new_contact_with_image()
        self.request_contact_that_exists()
        self.request_contact_that_doesnt_exist()
        self.contact_with_existing_phonenumber()
        self.list_all_contacts()
        self.update_contact()
        self.delete_contact()

class ContactBookModelsTestCase(APITestCase):

    def setUp(self):
        """Set up database with prepopulated data"""
        Contacts.objects.create(
            name="Matt Edwards",
            email="matt@mspe.me",
            phoneNumber="+447943337410"
        )

    def test_str(self):
        contact = Contacts.objects.get(id=1)
        self.assertEqual(str(contact), "Matt Edwards")

    def test_create_record(self):
        contact = Contacts(
            name="John Doe",
            email="john.doe@test.me",
            phoneNumber="+447965197492"
        )
        contact.save()

        self.assertEqual(contact.profile_picture.url, "/media/profile_pictures/default.jpg")
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.email, "john.doe@test.me")
        self.assertEqual(contact.phoneNumber, "+447965197492")

import io
import json
import shutil
import tempfile

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
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
        User.objects.create(
            username="test@mspe.me",
            email="test@mspe.me",
            password=make_password("5up3R!97")
        )
        user = User.objects.get(username="test@mspe.me")
        Contacts.objects.create(
            owner=user,
            name="Matt Edwards"
        )
        contact = Contacts.objects.get(id=1)
        PhoneNumbers.objects.create(
            contact=contact,
            type= "home",
            data= "07964974125"
        )
        Emails.objects.create(
            contact=contact,
            type="pers",
            data='matt@mspe.me'
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
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/contacts/',
            {
                "name": "John Doe"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
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
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/contacts/',
            {
                "profile_picture": photo_file,
                "name": "Jane Doe"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
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
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/contacts/phone-number',
            {
                "contact": 1,
                "type": "mob",
                "data": "07936498745"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 2,
                "contact": 1,
                "type": "mob",
                "data": "07936 498745"
            }
        )

    def create_new_email(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/contacts/email',
            {
                "contact": 1,
                "type": "work",
                "data": "test@mspe.me"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 2,
                "contact": 1,
                "type": "work",
                "data": "test@mspe.me"
            }
        )

    def create_phone_number_that_already_exists(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/contacts/phone-number',
            {
                "contact": 1,
                "type": "mob",
                "data": "07964974125"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {'non_field_errors': ['Contact with the phone number 07964974125 already exists.']}
        )

    def create_email_that_already_exists(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/contacts/email',
            {
                "contact": 1,
                "type": "work",
                "data": "matt@mspe.me"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {'non_field_errors': ['Contact with the email matt@mspe.me already exists.']}
        )

    def request_contact_that_exists(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.get('/api/contacts/1',
                                    **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        self.assertEqual(
            {
                "id": 1,
                "profile_picture": "/media/profile_pictures/default.jpg",
                "name": "Matt Edwards",
                "phone_number": [
                    {
                        "id": 1,
                        "contact": 1,
                        "type": "home",
                        "data": "07964 974125"
                    }
                ],
                "email": [
                    {
                        "id": 1,
                        "contact": 1,
                        "type": "pers",
                        "data": "matt@mspe.me"
                    }
                ]
            },
            json.loads(response.content)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def request_contact_that_doesnt_exist(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.get('/api/contacts/50',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        self.assertEqual(
            {
                "detail": "Not found."
            },
            json.loads(response.content)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def list_all_contacts(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.get('/api/contacts/',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
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
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.put(
            '/api/contacts/name/1',
            {"name": "Matthew Edwards"},
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
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
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.put(
            '/api/contacts/phone-number/2',
            {
                "contact": 1,
                "type": "mob",
                "data": "07936792548"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 2,
                "contact": 1,
                "type": "mob",
                "data": "07936 792548"
            }
        )

    def update_email(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.put(
            '/api/contacts/email/1',
            {
                "contact": 1,
                "type": "pers",
                "data": "matthew@mspe.me"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 1,
                "contact": 1,
                "type": "pers",
                "data": "matthew@mspe.me"
            }
        )

    def adding_same_phone_type(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/contacts/phone-number',
            {
                "contact": 1,
                "type": "mob",
                "data": "07964498453"

            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {'non_field_errors': ['Contact already has a phone number with this type.']}
        )

    def adding_same_type(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/contacts/email',
            {
                "contact": 1,
                "type": "pers",
                "data": "testing@mspe.me"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {'non_field_errors': ['Contact already has an email with this type.']}
        )

    def delete_contact_with_default_image(self):
        """default.jpg should not be deleted"""
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.delete('/api/contacts/2',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_phone_number(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.delete(
            '/api/contacts/phone-number/1',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def delete_email(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.delete(
            '/api/contacts/email/1',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def update_profile_picture(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        photo_file = self.generate_photo_file(file_name="new_pic")
        response = self.client.put(
            '/api/contacts/profile-picture/1',
            { 'profile_picture': photo_file },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'},
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
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.post(
            '/api/contacts/',
            {
                "first_name": "Matt"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "name": ["This field is required."]
            }
        )

    def put_phone_number_error(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.put(
            '/api/contacts/phone-number/1',
            {
                "data": "07954793156"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                'contact': ['This field is required.']
            }
        )

    def put_email_error(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.put(
            '/api/contacts/email/1',
            {
                "data": "07954793156"
            },
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "contact": [
                    "This field is required."
                ],
                "data": [
                    "Enter a valid email address."
                ]
            }
        )

    def get_email(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.get(
            '/api/contacts/email/1',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 1,
                "contact": 1,
                "type": "pers",
                "data": "matt@mspe.me"
            }
        )

    def get_phone_number(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.get(
            '/api/contacts/phone-number/1',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 1,
                "contact": 1,
                "type": "home",
                "data": "07964 974125"
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
        self.get_email()
        self.get_phone_number()
        self.update_contact_name()
        self.update_phone_number()
        self.update_email()
        self.adding_same_phone_type()
        self.adding_same_type()
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
        User.objects.create(
            username="test@mspe.me",
            email="test@mspe.me",
            password=make_password("5up3R!97")
        )
        user = User.objects.get(username="test@mspe.me")
        Contacts.objects.create(
            owner=user,
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
        user = User.objects.get(username="test@mspe.me")
        contact = Contacts(
            owner=user,
            name="John Doe",
        )
        contact.save()

        self.assertEqual(contact.owner.username, "test@mspe.me")
        self.assertEqual(contact.profile_picture.url, "/media/profile_pictures/default.jpg")
        self.assertEqual(contact.name, "John Doe")

    def create_phonenumber(self):
        contact = Contacts.objects.get(name="Matt Edwards")
        phone_number = PhoneNumbers(
            contact=contact,
            type='home',
            data="0796411359"
        )
        phone_number.save()

        self.assertEqual(phone_number.contact.name, "Matt Edwards")
        self.assertEqual(phone_number.type, "home")
        self.assertEqual(phone_number.data, "0796411359")

    def phonenumber_str(self):
        phonenumber = PhoneNumbers.objects.get(id=1)
        self.assertEqual(str(phonenumber), "Matt Edwards: Home - 0796411359")

    def create_email(self):
        contact = Contacts.objects.get(name="Matt Edwards")
        email = Emails(
            contact=contact,
            type='work',
            data="matt@mspe.me"
        )
        email.save()

        self.assertEqual(email.contact.name, "Matt Edwards")
        self.assertEqual(email.type, "work")
        self.assertEqual(email.data, "matt@mspe.me")

    def email_str(self):
        email = Emails.objects.get(id=1)
        self.assertEqual(str(email), "Matt Edwards: Work - matt@mspe.me")

    def test_in_order(self):
        self.create_phonenumber()
        self.phonenumber_str()
        self.create_email()
        self.email_str()

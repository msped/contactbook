import json
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Contacts

class ContactBookViewsTestCase(APITestCase):

    def setUp(self):
        """Set up database with prepopulated data"""
        Contacts.objects.create(
            name="Matt Edwards",
            email="matt@mspe.me",
            phoneNumber="+447943337410"
        )

    def create_new_contact(self):
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
                "name": "John Doe",
                "email": "john.doe@test.me",
                "phoneNumber": "+447968461978"
            }
        )

    def request_contact_that_exists(self):
        response = self.client.get('/api/contacts/1')
        self.assertEqual(
            {
                "id": 1,
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
                    "name": "Matt Edwards",
                    "email": "matt@mspe.me",
                    "phoneNumber": "+447943337410"
                },
                {
                    "id": 2,
                    "name": "John Doe",
                    "email": "john.doe@test.me",
                    "phoneNumber": "+447968461978"
                }
            ]
        )

    def update_contact(self):
        response = self.client.put(
            '/api/contacts/1',
            {
                "name": "Matthew Edwards",
                "email": "matt@mspe.me",
                "phoneNumber": "+447943337410"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                "id": 1,
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
        self.create_new_contact()
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

        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.email, "john.doe@test.me")
        self.assertEqual(contact.phoneNumber, "+447965197492")

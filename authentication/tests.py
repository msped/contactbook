import json
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

class AuthTests(APITestCase):

    def setUp(self):
        User.objects.create(
            username="matt@mspe.me",
            email="matt@mspe.me",
            password=make_password("5up3R!97")
        )

    def registration_working_response(self):
        response = self.client.post(
            '/api/auth/register',
            {
                'username': 'test@gmail.com',
                'password': '5up3R!98',
                'password2': '5up3R!98'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def registration_invalid_email(self):
        response = self.client.post(
            '/api/auth/register',
            {
                'username': 'test2gmail.com',
                'password': '5up3R!98',
                'password2': '5up3R!98'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "username": ["Enter a valid email address."]
            }
        )

    def registration_passwords_dont_match(self):
        response = self.client.post(
            '/api/auth/register',
            {
                'username': 'test3@gmail.com',
                'password': '5up4R!98',
                'password2': '5up4R!97'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {
                "password": ["Password fields don't match"]
            }
        )

    def request_access_token(self):
        response = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@gmail.com',
                'password': '5up3R!98'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def request_refresh_token(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'test@gmail.com',
                'password': '5up3R!98'
            },
            format='json'
        )
        refresh_token = access_request.data['refresh']
        response = self.client.post(
            '/api/auth/token/refresh',
            {
                'username': 'test@gmail.com',
                'password': '5up3R!98',
                'refresh': refresh_token
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_a_contact_as_another_user(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'matt@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.delete(
            '/api/auth/delete/2',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def delete_a_contact_as_owner(self):
        access_request = self.client.post(
            '/api/auth/token',
            {
                'username': 'matt@mspe.me',
                'password': '5up3R!97'
            },
            format='json'
        )
        access_token = access_request.data['access']
        response = self.client.delete(
            '/api/auth/delete/1',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_in_order(self):
        self.registration_working_response()
        self.registration_invalid_email()
        self.registration_passwords_dont_match()
        self.request_access_token()
        self.request_refresh_token()
        self.delete_a_contact_as_another_user()
        self.delete_a_contact_as_owner()

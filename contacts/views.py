from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Contacts, Emails, PhoneNumbers
from .serializers import (ContactDetailSerializer, ContactNameSerializer,
                          ContactsSerializer, EmailSerializer,
                          PhoneNumberSerializer, ProfilePictureSerializer)

# Create your views here.

class CreateListContactView(ListCreateAPIView):
    """Create a contact or list all contacts"""
    serializer_class = ContactsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        return Contacts.objects.filter(owner=user)

class ContactDetailView(APIView):

    """Get detailed contact or delete"""
    def get(self, request, contact_id):
        contact = get_object_or_404(Contacts, id=contact_id)
        if request.user.id != contact.owner.id:
            return Response(
                "You don't have access to view this contact.",
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = ContactDetailSerializer(contact, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, contact_id):
        contact = get_object_or_404(Contacts, id=contact_id)
        if request.user.id != contact.owner.id:
            return Response(
                "You don't have access to view this contact.",
                status=status.HTTP_401_UNAUTHORIZED
            )
        contact.delete()
        return Response(f"Contact {contact.name} deleted.", status=status.HTTP_200_OK)

class CreatePhoneNumber(CreateAPIView):
    serializer_class = PhoneNumberSerializer
    permission_classes = [IsAuthenticated]

class CreateEmail(CreateAPIView):
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

class UpdatePhoneNumber(APIView):
    serializer_class = PhoneNumberSerializer

    def put(self, request, phone_number_id):
        number = get_object_or_404(PhoneNumbers, id=phone_number_id)
        if request.user.id != number.contact.owner.id:
            return Response(
                "You don't have access to view this contact.",
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = self.serializer_class(number, data=request.data,
                                    context={'phonenumber_id': phone_number_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, phone_number_id):
        number = get_object_or_404(PhoneNumbers, id=phone_number_id)
        if request.user.id != number.contact.owner.id:
            return Response(
                "You don't have access to view this contact.",
                status=status.HTTP_401_UNAUTHORIZED
            )
        number.delete()
        return Response(
            f"Phone number {number.phoneNumber} has been deleted.",
            status=status.HTTP_204_NO_CONTENT
        )

class UpdateEmail(APIView):
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, email_id):
        email = get_object_or_404(Emails, id=email_id)
        if request.user.id != email.contact.owner.id:
            return Response(
                "You don't have access to view this contact.",
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = self.serializer_class(email, data=request.data, context={'email_id': email_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, email_id):
        email = get_object_or_404(Emails, id=email_id)
        if request.user.id != email.contact.owner.id:
            return Response(
                "You don't have access to view this contact.",
                status=status.HTTP_401_UNAUTHORIZED
            )
        email.delete()
        return Response(
            f"Email {email.email} has been deleted.",
            status=status.HTTP_204_NO_CONTENT
        )

class UpdateContactName(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactNameSerializer
    lookup_url_kwarg = "contact_id"
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        return Contacts.objects.filter(owner=user)

class UpdateProfilePicutre(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfilePictureSerializer
    lookup_url_kwarg = "contact_id"
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        return Contacts.objects.filter(owner=user)

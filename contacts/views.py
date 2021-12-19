from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, UpdateAPIView,
                                     get_object_or_404)
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
    queryset = Contacts.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactDetailView(APIView):
    """Get detailed contact or delete"""
    def get(self, request, contact_id):
        contact = get_object_or_404(Contacts, id=contact_id)
        serializer = ContactDetailSerializer(contact, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, contact_id):
        contact = get_object_or_404(Contacts, id=contact_id)
        contact.delete()
        return Response(f"Contact {contact.name} deleted.", status=status.HTTP_200_OK)

class UpdatePhoneNumber(APIView):
    serializer_class = PhoneNumberSerializer

    def post(self, request, phone_number_id):
        contact = get_object_or_404(Contacts, id=phone_number_id)
        serializer = self.serializer_class(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save(contact=contact)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    def put(self, request, phone_number_id):
        number = get_object_or_404(PhoneNumbers, id=phone_number_id)
        serializer = self.serializer_class(number, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, phone_number_id):
        number = get_object_or_404(PhoneNumbers, id=phone_number_id)
        number.delete()
        return Response(
            f"Phone number {number.phoneNumber} has been deleted.",
            status=status.HTTP_204_NO_CONTENT
        )

class UpdateEmail(APIView):
    serializer_class = EmailSerializer

    def post(self, request, email_id):
        contact = get_object_or_404(Contacts, id=email_id)
        serializer = self.serializer_class(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save(contact=contact)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    def put(self, request, email_id):
        email = get_object_or_404(Emails, id=email_id)
        serializer = self.serializer_class(email, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, email_id):
        email = get_object_or_404(Emails, id=email_id)
        email.delete()
        return Response(
            f"Email {email.email} has been deleted.",
            status=status.HTTP_204_NO_CONTENT
        )

class UpdateContactName(UpdateAPIView):
    serializer_class = ContactNameSerializer
    lookup_url_kwarg = "contact_id"
    lookup_field = "id"

    def get_queryset(self):
        return Contacts.objects.all()

class UpdateProfilePicutre(UpdateAPIView):
    serializer_class = ProfilePictureSerializer
    lookup_url_kwarg = "contact_id"
    lookup_field = "id"

    def get_queryset(self):
        return Contacts.objects.all()

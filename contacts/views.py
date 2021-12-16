from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView, UpdateAPIView, get_object_or_404)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Contacts, Emails, PhoneNumbers
from .serializers import (ContactDetailSerializer, ContactsSerializer,
                          EmailSerializer, PhoneNumberSerializer,
                          ProfilePictureSerializer, ContactNameSerializer)

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
    def get(self, contact_id):
        contact = get_object_or_404(Contacts, id=contact_id)
        serializer = ContactDetailSerializer(contact, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, contact_id):
        contact = get_object_or_404(Contacts, id=contact_id)
        contact.delete()
        return Response(f"Contact {contact.name} deleted.", status=status.HTTP_200_OK)

class UpdatePhoneNumber(RetrieveUpdateDestroyAPIView):
    serializer_class = PhoneNumberSerializer
    lookup_url_kwarg = "phone_number_id"
    lookup_field = "id"

    def get_queryset(self):
        return PhoneNumbers.objects.all()

class UpdateEmail(RetrieveUpdateDestroyAPIView):
    serializer_class = EmailSerializer
    lookup_url_kwarg = "email_id"
    lookup_field = "id"

    def get_queryset(self):
        return Emails.objects.all()

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

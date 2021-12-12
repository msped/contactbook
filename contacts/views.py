from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Contacts
from .serializers import ContactSerializer

# Create your views here.

class ContactsView(ListCreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contacts.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactView(APIView):
    def get(self, request, contact_id):
        contact = get_object_or_404(Contacts, id=contact_id)
        serializer = ContactSerializer(contact)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, contact_id):
        contact = get_object_or_404(Contacts, id=contact_id)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, contact_id):
        contact = get_object_or_404(Contacts, id=contact_id)
        contact.delete()
        return Response(
            {f'Contact {contact.name} has been deleted'},
            status=status.HTTP_200_OK
        )

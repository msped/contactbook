from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Contacts
from .serializers import ContactSerializer

# Create your views here.

class ContactsView(ListAPIView):
    serializer_class = ContactSerializer
    queryset = Contacts.objects.all()

class ContactView(APIView):
    def get(self, request, contact_id):
        contact = Contacts.objects.get(id=contact_id)
        serializer = ContactSerializer(contact)
        return Response(serializer.data, status=status.HTTP_200_OK)

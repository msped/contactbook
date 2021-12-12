from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
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

class ContactView(RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    lookup_url_kwarg = "contact_id"
    lookup_field = "id"

    def get_queryset(self):
        return Contacts.objects.all()

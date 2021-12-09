from rest_framework.generics import ListAPIView
from .models import Contacts
from .serializers import ContactSerializer

# Create your views here.

class ContactsView(ListAPIView):
    serializer_class = ContactSerializer
    queryset = Contacts.objects.all()

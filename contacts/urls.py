from django.urls import path
from .views import ContactsView, ContactView

urlpatterns = [
    path('', ContactsView.as_view(), name="contacts_view"),
    path('<int:contact_id>', ContactView.as_view(), name="contact_view")
]

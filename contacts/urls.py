from django.urls import path
from .views import ContactsView, ContactView, UpdatePhoneNumber

urlpatterns = [
    path('', ContactsView.as_view(), name="contacts_view"),
    path('<int:contact_id>', ContactView.as_view(), name="contact_view"),
    path(
        'phone-number/<int:phone_number_id>',
        UpdatePhoneNumber.as_view(),
        name="update_phone_number"
    ),
]

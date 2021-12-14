from django.urls import path
from .views import ContactsView, ContactView, UpdatePhoneNumber, UpdateEmail

urlpatterns = [
    path('', ContactsView.as_view(), name="contacts_view"),
    path('<int:contact_id>', ContactView.as_view(), name="contact_view"),
    path(
        'phone-number/<int:phone_number_id>',
        UpdatePhoneNumber.as_view(),
        name="update_phone_number"
    ),
    path(
        'email/<int:email_id>',
        UpdateEmail.as_view(),
        name="update_email"
    ),
]

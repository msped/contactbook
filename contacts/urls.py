from django.urls import path

from .views import (ContactDetailView, CreateEmail, CreateListContactView,
                    CreatePhoneNumber, UpdateContactName, UpdateEmail,
                    UpdatePhoneNumber, UpdateProfilePicutre)

urlpatterns = [
    path('', CreateListContactView.as_view(), name="contacts"),
    path('<int:contact_id>', ContactDetailView.as_view(), name="contact_detail"),
    path('phone-number', CreatePhoneNumber.as_view(), name="create_phone_number"),
    path('email', CreateEmail.as_view(), name="create_email"),
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
    path('name/<int:contact_id>', UpdateContactName.as_view(), name="update_contact_name"),
    path(
        'profile-picture/<int:contact_id>',
        UpdateProfilePicutre.as_view(),
        name="update_profile_picture"
    ),
]

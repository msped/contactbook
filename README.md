# Contact Book

## Features

- Create a program that can be used to manage contacts.
- To work as an HTTP REST API.
- Be able to add a contact with a name, email and, phone number.
- Be able to list all contacts.
- Be able to edit a contact.
- Be able to delete a contact.
- Contact must persist (e.g. if you close the app you should not lose them)

## Routes

Detailed below are routes and information required to create and received requests.

`GET POST /api/contacts`
- `GET` returns all contacts.
- `POST` creates a contact using the following body:
    - `"profile_picture"`: `file`, `"name"`: `string`.

`GET DELETE /api/contacts/:contact_id`
- `GET` return single contact with associated phone numbers and emails.
- `DELETE` deletes the single contact and associated phone numbers and emails.

`POST /api/contacts/phone-number`
- Creates a new phone number using the following body:
    - `"contact"`: `id` of the associated contact, `"phonenumber_type"`: `string`, `"phoneNumber"`: `string`.
- `"phonenumber_type"` values are `home` (Home), `mob` (Mobile) & `work` (Work).
- `"phoneNumber"` format is UK only starting in +44..

`POST /api/contacts/email`
- Creates a new email using the following body:
    - `"contact"`: `id` of the associated contact, `"email_type"`: `string`, `"email"`: `string`.
- `"email_type"` values are `pers` (Personal) & `work` (Work).
- `"email"` format will only accept a valid email format, test@example.com.

`PUT DELETE /api/contacts/phone-number/:phone_number_id`
- Updates a single phone number record using the following body:
    - `"contact"`: `id` of the associated contact, `"phonenumber_type"`: `string`, `"phoneNumber"`: `string`.
- `"phonenumber_type"` values are `home` (Home), `mob` (Mobile) & `work` (Work).
- `"phoneNumber"` format is UK only starting in +44..

`PUT DELETE /api/contacts/email/:email`
- Updates a single email record using the following body:
    - `"contact"`: `id` of the associated contact, `"phonenumber_type"`: `string`, `"phoneNumber"`: `string`.
- `"phonenumber_type"` values are `home` (Home), `mob` (Mobile) & `work` (Work).
- `"phoneNumber"` format is UK only starting in +44..


`PUT /api/contacts/name/:contact_id`
- Updates a single contacts name using the following body:
    - `"name"`: `string`

`PUT /api/contacts/profile-picture/:contact_id`
- Updates a single contacts profile picture using the following body:
    - `"profile_picture"`: file

### How to run this project on your local machine

In order to the the code locally you must first clone the repository using `git clone https://github.com/msped/contactbook.git`.

Once cloned open your terminal and navigate to the folder the files have been downloaded to. Using `python -m venv *venv name*`, setup a virtual environment for this project.

To access the virtual environment, in your terminal at the same location, run `*venv name*\Scripts\activate` on Windows and `source *venv name*/Scripts/activate` on the Mac. Once the the virtual environment is activated it should shows `(*venv name*)` in the termial before your current path. 

In order to run the project you must install it's dependencies using `pip install -r requirements.txt`. Once the install has completed, you can run `python manage.py runserver` where the server will run on `http://127.0.0.1:8000/`.
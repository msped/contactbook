# Generated by Django 3.2.10 on 2021-12-13 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0007_auto_20211213_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emails',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email', to='contacts.contacts'),
        ),
        migrations.AlterField(
            model_name='phonenumbers',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_number', to='contacts.contacts'),
        ),
    ]
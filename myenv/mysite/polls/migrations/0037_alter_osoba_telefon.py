# Generated by Django 3.2.3 on 2021-05-30 17:36

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0036_osoba_telefon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osoba',
            name='telefon',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]
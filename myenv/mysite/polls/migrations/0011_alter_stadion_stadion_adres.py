# Generated by Django 3.2.3 on 2021-05-28 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20210528_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stadion',
            name='stadion_adres',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='polls.adres'),
        ),
    ]

# Generated by Django 3.2.3 on 2021-05-30 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0030_auto_20210530_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adres',
            name='NrLokalu',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
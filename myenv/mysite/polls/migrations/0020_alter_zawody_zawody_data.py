# Generated by Django 3.2.3 on 2021-05-29 18:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0019_alter_zawody_zawody_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zawody',
            name='zawody_data',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Kiedy'),
        ),
    ]
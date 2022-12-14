# Generated by Django 3.2.3 on 2021-05-29 18:58

from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0021_alter_zawody_zawody_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zawody',
            name='aff_url',
            field=models.SlugField(blank=True, help_text='wyrazy-oddzielone-myslnikami', null=True),
        ),
        migrations.AlterField(
            model_name='zawody',
            name='zawody_data',
            field=models.DateTimeField(default=polls.models.return_date_time, help_text='<em>YYYY-MM-DD HH:MM</em>', verbose_name='Kiedy'),
        ),
    ]

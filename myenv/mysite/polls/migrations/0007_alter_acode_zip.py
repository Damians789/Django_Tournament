# Generated by Django 3.2.3 on 2021-05-27 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20210525_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acode',
            name='ZIP',
            field=models.CharField(max_length=6),
        ),
    ]

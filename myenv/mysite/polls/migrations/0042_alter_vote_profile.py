# Generated by Django 3.2.3 on 2021-05-31 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0041_alter_vote_stadion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.profile'),
        ),
    ]

# Generated by Django 3.2.3 on 2021-05-31 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0044_alter_vote_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='nawierzchnia',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='organizacja',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='szatnie',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
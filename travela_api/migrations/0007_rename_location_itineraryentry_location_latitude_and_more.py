# Generated by Django 4.2 on 2023-05-05 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travela_api', '0006_remove_user_acceptedrequests_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itineraryentry',
            old_name='location',
            new_name='location_latitude',
        ),
        migrations.AddField(
            model_name='itineraryentry',
            name='location_longitude',
            field=models.CharField(default=' ', max_length=80),
            preserve_default=False,
        ),
    ]
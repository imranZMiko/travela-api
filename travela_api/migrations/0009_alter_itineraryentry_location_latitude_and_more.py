# Generated by Django 4.2 on 2023-05-06 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travela_api', '0008_alter_itineraryentry_location_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itineraryentry',
            name='location_latitude',
            field=models.DecimalField(decimal_places=20, max_digits=25),
        ),
        migrations.AlterField(
            model_name='itineraryentry',
            name='location_longitude',
            field=models.DecimalField(decimal_places=20, max_digits=25),
        ),
    ]

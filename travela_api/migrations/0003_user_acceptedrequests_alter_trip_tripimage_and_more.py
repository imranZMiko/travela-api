# Generated by Django 4.2 on 2023-05-01 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travela_api', '0002_trip_pendingusers_user_pendingrequests_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='acceptedRequests',
            field=models.ManyToManyField(blank=True, related_name='accepted_requests', to='travela_api.trip'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='tripImage',
            field=models.ImageField(blank=True, null=True, upload_to='tripImages/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='pendingRequests',
            field=models.ManyToManyField(blank=True, related_name='pending_requests', to='travela_api.trip'),
        ),
    ]

# Generated by Django 4.2 on 2023-05-01 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travela_api', '0003_user_acceptedrequests_alter_trip_tripimage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='userEmail',
            field=models.CharField(default='example@example.com', max_length=50),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2 on 2023-04-14 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userID', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=50)),
                ('userImage', models.ImageField(upload_to='userImages/')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tripName', models.CharField(max_length=80)),
                ('tripImage', models.ImageField(upload_to='tripImages/')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='travela_api.user')),
                ('sharedUsers', models.ManyToManyField(to='travela_api.user')),
            ],
        ),
        migrations.CreateModel(
            name='ItineraryEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField()),
                ('description', models.CharField(max_length=500)),
                ('location', models.CharField(max_length=80)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itinerary_entries', to='travela_api.trip')),
            ],
        ),
    ]

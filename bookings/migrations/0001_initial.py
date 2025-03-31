# Generated by Django 5.1.7 on 2025-03-31 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=100)),
                ('check_in_datetime', models.DateTimeField()),
                ('check_out_datetime', models.DateTimeField()),
                ('num_persons', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

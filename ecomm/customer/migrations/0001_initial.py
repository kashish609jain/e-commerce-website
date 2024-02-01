# Generated by Django 5.0.1 on 2024-01-31 10:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address', models.CharField(max_length=250, verbose_name='address')),
                ('city', models.CharField(max_length=20, verbose_name='city')),
                ('state', models.CharField(max_length=250, verbose_name='state')),
                ('phone_number', models.CharField(max_length=11, verbose_name='phone number')),
            ],
        ),
    ]

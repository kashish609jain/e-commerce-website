# Generated by Django 5.0.1 on 2024-02-01 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0007_rename_master_email_vendor_master_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='master_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
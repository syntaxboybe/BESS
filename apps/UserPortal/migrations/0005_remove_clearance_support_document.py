# Generated by Django 4.1.2 on 2025-03-27 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserPortal', '0004_supportingdocument'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clearance',
            name='support_document',
        ),
    ]

# Generated by Django 4.2.21 on 2025-05-29 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productmodel',
            options={'ordering': ['-created_date']},
        ),
    ]

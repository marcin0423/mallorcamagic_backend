# Generated by Django 3.2.9 on 2022-05-12 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saved_data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedguide',
            name='category',
        ),
    ]

# Generated by Django 4.0.4 on 2023-01-09 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_guides', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidemodel',
            name='highlighted',
            field=models.BooleanField(default=False),
        ),
    ]
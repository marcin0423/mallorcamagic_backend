# Generated by Django 3.2.9 on 2022-05-12 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedProperty',
            fields=[
                ('slug', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('partner', models.CharField(max_length=64)),
                ('thumbnail', models.TextField()),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('price_unit', models.CharField(max_length=4)),
                ('price_amount', models.CharField(max_length=16)),
                ('bathrooms', models.IntegerField(default=0)),
                ('bedrooms', models.IntegerField(default=0)),
                ('area', models.CharField(max_length=16)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedGuide',
            fields=[
                ('slug', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('creator', models.CharField(max_length=64)),
                ('thumbnail', models.TextField()),
                ('category', models.CharField(max_length=64)),
                ('title_en', models.TextField()),
                ('title_es', models.TextField()),
                ('title_de', models.TextField()),
                ('short_desc_en', models.TextField()),
                ('short_desc_es', models.TextField()),
                ('short_desc_de', models.TextField()),
                ('long_desc_en', models.TextField()),
                ('long_desc_es', models.TextField()),
                ('long_desc_de', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

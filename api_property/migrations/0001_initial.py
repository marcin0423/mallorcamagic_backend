# Generated by Django 4.0.4 on 2022-06-12 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyModel',
            fields=[
                ('slug', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=256)),
                ('type', models.CharField(max_length=64)),
                ('thumbnail', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('price_unit', models.CharField(max_length=4)),
                ('price_amount', models.CharField(max_length=16)),
                ('bathrooms', models.CharField(max_length=8)),
                ('bedrooms', models.CharField(max_length=8)),
                ('area', models.CharField(max_length=16)),
            ],
        ),
    ]

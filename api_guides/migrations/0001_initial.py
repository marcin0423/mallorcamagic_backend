# Generated by Django 3.2.9 on 2022-05-12 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GuideModel',
            fields=[
                ('slug', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('creator', models.CharField(max_length=64)),
                ('thumbnail', models.TextField()),
                ('category', models.CharField(max_length=64)),
                ('timestamp', models.CharField(max_length=64)),
                ('title_en', models.TextField()),
                ('title_es', models.TextField()),
                ('title_de', models.TextField()),
                ('short_desc_en', models.TextField()),
                ('short_desc_es', models.TextField()),
                ('short_desc_de', models.TextField()),
                ('long_desc_en', models.TextField()),
                ('long_desc_es', models.TextField()),
                ('long_desc_de', models.TextField()),
            ],
        ),
    ]
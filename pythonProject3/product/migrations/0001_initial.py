# Generated by Django 4.2 on 2024-01-23 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255)),
                ('price', models.FloatField(max_length=255)),
                ('stock', models.IntegerField()),
                ('image_url', models.TextField(max_length=2083)),
            ],
        ),
    ]

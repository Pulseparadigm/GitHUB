# Generated by Django 4.2 on 2024-02-21 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patientsesss', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(default='2024-02-24', max_length=255),
        ),
    ]

# Generated by Django 4.2 on 2024-03-06 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Patientsesss', '0002_alter_patient_date_of_birth'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('Department', models.CharField(max_length=255)),
                ('ContactInfo', models.IntegerField()),
                ('Salary', models.FloatField()),
                ('Schedule', models.DateField()),
                ('on_vacation', models.CharField(max_length=255)),
                ('test_ordered', models.IntegerField()),
                ('tests_pending', models.IntegerField()),
            ],
            options={
                'db_table': 'Nurse',
            },
        ),
        migrations.CreateModel(
            name='SampleCollector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample', models.CharField(max_length=255)),
                ('CollectorName', models.CharField(max_length=255)),
                ('orderDate', models.DateField(auto_now_add=True)),
                ('Nurse_ID', models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='Nurses.nurse')),
                ('Patient_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Patientsesss.patient')),
            ],
            options={
                'db_table': 'Sample_Collector',
            },
        ),
    ]
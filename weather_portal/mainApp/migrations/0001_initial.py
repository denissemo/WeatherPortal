# Generated by Django 2.0.3 on 2019-04-10 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=30)),
                ('min_temp', models.CharField(max_length=5)),
                ('max_temp', models.CharField(max_length=5)),
                ('wind', models.CharField(max_length=5)),
                ('description', models.CharField(max_length=100)),
                ('clouds', models.CharField(max_length=5)),
                ('icon', models.CharField(max_length=5)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.City')),
            ],
        ),
    ]

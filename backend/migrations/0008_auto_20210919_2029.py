# Generated by Django 3.1.2 on 2021-09-19 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_remove_services_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='title',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
# Generated by Django 3.1.2 on 2021-10-07 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_auto_20211007_0338'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='response',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]

# Generated by Django 3.1.2 on 2021-12-09 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0025_auto_20211207_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='launderette',
            name='delivery_fee_pkm',
            field=models.FloatField(default=0),
        ),
    ]

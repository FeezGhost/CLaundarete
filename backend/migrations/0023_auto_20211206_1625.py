# Generated by Django 3.1.2 on 2021-12-06 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0022_order_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='lon',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='launderer',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='launderer',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='launderer',
            name='lon',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

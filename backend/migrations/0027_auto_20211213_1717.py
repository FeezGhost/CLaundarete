# Generated by Django 3.1.2 on 2021-12-13 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0026_launderette_delivery_fee_pkm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_started',
            field=models.DateField(blank=True, null=True),
        ),
    ]

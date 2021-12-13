# Generated by Django 3.1.2 on 2021-12-13 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0031_auto_20211213_1810'),
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
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('finished', 'Finished'), ('pre-finished', 'Pre-Finished'), ('ongoing', 'Ongoing'), ('declined', 'Declined'), ('canceled', 'Canceled')], default='pending', max_length=50, null=True),
        ),
    ]

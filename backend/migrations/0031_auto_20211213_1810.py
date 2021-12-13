# Generated by Django 3.1.2 on 2021-12-13 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0030_remove_order_hasdelivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='isFinished',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('finished', 'Finished'), ('pre finished', 'Pre Finished'), ('ongoing', 'Ongoing'), ('declined', 'Declined'), ('canceled', 'Canceled')], default='pending', max_length=50, null=True),
        ),
    ]
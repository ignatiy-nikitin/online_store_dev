# Generated by Django 3.2.2 on 2021-05-19 22:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderfinal',
            name='status',
        ),
        migrations.AddField(
            model_name='orderfinal',
            name='delivery_time_from',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderfinal',
            name='delivery_time_to',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderfinal',
            name='extra_info',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

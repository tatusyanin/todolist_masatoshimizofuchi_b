# Generated by Django 5.0.6 on 2024-06-04 03:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_todoitem_name_alter_todoitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='store_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]

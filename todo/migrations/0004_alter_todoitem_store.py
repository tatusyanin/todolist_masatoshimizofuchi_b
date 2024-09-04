# Generated by Django 5.1 on 2024-09-04 01:30

import django.db.models.deletion
import django.db.models.query
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_alter_todoitem_store_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='store',
            field=models.ForeignKey(default=django.db.models.query.QuerySet.first, on_delete=django.db.models.deletion.CASCADE, to='todo.store'),
        ),
    ]

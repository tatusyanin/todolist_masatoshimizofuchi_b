# Generated by Django 5.0.6 on 2024-09-02 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='location',
        ),
        migrations.RemoveField(
            model_name='todoitem',
            name='store_id',
        ),
        migrations.AddField(
            model_name='todoitem',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='todo.store'),
        ),
    ]

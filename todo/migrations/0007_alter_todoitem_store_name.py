# Generated by Django 5.0.6 on 2024-06-04 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_todoitem_store_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='store_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
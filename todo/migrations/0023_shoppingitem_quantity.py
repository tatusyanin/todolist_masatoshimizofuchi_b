# Generated by Django 5.0.6 on 2024-07-23 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0022_alter_category_id_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]

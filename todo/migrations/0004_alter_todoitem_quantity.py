# Generated by Django 5.1.2 on 2024-12-16 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0003_alter_todoitem_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todoitem",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
# Generated by Django 5.1.2 on 2024-11-15 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_alter_item_description_alter_item_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='created_by',
        ),
    ]

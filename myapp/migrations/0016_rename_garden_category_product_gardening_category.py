# Generated by Django 4.0.3 on 2022-05-05 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_product_product_maintainance_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='garden_category',
            new_name='gardening_category',
        ),
    ]

# Generated by Django 4.0.3 on 2022-05-05 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_rename_garden_category_product_gardening_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='gardening_category',
            new_name='garden_category',
        ),
    ]

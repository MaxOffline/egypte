# Generated by Django 2.1.5 on 2019-02-11 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='orderedTime',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
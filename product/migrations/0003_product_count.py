# Generated by Django 2.1.5 on 2019-02-11 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20190211_0255'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

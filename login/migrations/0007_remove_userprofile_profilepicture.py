# Generated by Django 2.1.5 on 2019-02-10 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20190210_0640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profilepicture',
        ),
    ]

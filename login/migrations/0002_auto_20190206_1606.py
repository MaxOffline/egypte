# Generated by Django 2.1.5 on 2019-02-06 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastname',
            field=models.CharField(max_length=20, null=True, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mobile',
            field=models.IntegerField(blank=True, null=True, verbose_name='Mobile'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profilepicture',
            field=models.ImageField(default='background.jpg', null=True, upload_to='bedding/', verbose_name='Profile picture'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=models.CharField(max_length=100, null=True, verbose_name='State'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='streetAdrress1',
            field=models.CharField(max_length=100, null=True, verbose_name='Street Address'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='streetAdrress2',
            field=models.CharField(max_length=100, null=True, verbose_name='Street Address 1'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='zip',
            field=models.IntegerField(null=True, verbose_name='ZIP Code'),
        ),
    ]

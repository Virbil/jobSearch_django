# Generated by Django 2.2 on 2021-07-20 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobSearch_app', '0005_auto_20210719_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='summary',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
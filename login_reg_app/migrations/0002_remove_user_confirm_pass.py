# Generated by Django 2.2 on 2021-05-27 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirm_pass',
        ),
    ]

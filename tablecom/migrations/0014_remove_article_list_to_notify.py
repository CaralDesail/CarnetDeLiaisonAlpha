# Generated by Django 3.1.3 on 2020-11-17 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tablecom', '0013_auto_20201116_1035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='list_to_notify',
        ),
    ]

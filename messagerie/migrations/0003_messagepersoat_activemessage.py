# Generated by Django 3.1.3 on 2020-11-16 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagerie', '0002_auto_20201112_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagepersoat',
            name='activeMessage',
            field=models.BooleanField(default=True),
        ),
    ]

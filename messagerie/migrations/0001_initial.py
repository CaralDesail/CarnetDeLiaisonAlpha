# Generated by Django 3.1.3 on 2020-11-12 10:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessagePersoAT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('auteurID', models.CharField(max_length=6)),
                ('AttachedChildNotebookID', models.CharField(max_length=7)),
                ('receiverID', models.CharField(default='0', max_length=6)),
                ('contenu', models.TextField(null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name="Date d'envoi'")),
            ],
            options={
                'verbose_name': 'Message Privé',
                'ordering': ['date'],
            },
        ),
    ]

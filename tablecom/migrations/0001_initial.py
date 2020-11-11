# Generated by Django 3.0.5 on 2020-05-02 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('id_ChildSNotebook', models.IntegerField(verbose_name='Id Carnet Enfant')),
                ('id_Professionnal', models.IntegerField(verbose_name='Id Professionnel')),
                ('title', models.CharField(max_length=255, verbose_name='Titre')),
                ('content', models.TextField(verbose_name='Contenu')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de parution')),
                ('valid_art', models.BooleanField(default=False)),
                ('list_to_notify', models.TextField(null=True, verbose_name='Id des personnes notifiée')),
            ],
            options={
                'verbose_name': 'article',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='CategoriePro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='ChildSNotebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=80, verbose_name='Nom')),
                ('forename', models.CharField(max_length=80, verbose_name='Prénom')),
                ('date_of_birth', models.DateField(verbose_name='Date de naissance')),
                ('id_RespLeg', models.CharField(default='', max_length=20, verbose_name='Id responsables legaux')),
                ('num_ident', models.CharField(max_length=20, verbose_name='Identifiant sécurité sociale')),
                ('id_prof_auth', models.TextField(max_length=1200, verbose_name='Id Professionnels Rattachés')),
            ],
            options={
                'verbose_name': 'Carnet Enfant',
                'ordering': ['date_of_birth'],
            },
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statusRL', models.CharField(default='non défini', max_length=20)),
                ('num_ident', models.CharField(max_length=20, verbose_name='Identifiant sécurité sociale')),
                ('mail', models.CharField(max_length=80, null=True)),
                ('phone', models.CharField(max_length=60, null=True)),
                ('rolePro', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tablecom.CategoriePro')),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

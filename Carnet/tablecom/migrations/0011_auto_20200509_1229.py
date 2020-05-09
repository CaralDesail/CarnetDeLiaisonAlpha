# Generated by Django 3.0.5 on 2020-05-09 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablecom', '0010_auto_20200509_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='child_access_asked',
            field=models.CharField(blank=True, default=' ', max_length=255, verbose_name='Nom des enfants rattachés'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='RLorPro',
            field=models.CharField(choices=[('0', 'Je ne sais pas'), ('1', 'Responsable_Legal'), ('2', 'Professionnel')], default='0', max_length=11, verbose_name='Quel est votre statut ? (Professionnel = Enseignant, Professionnel de santé, Responsable légal = Parent, tuteur)'),
        ),
    ]

# Generated by Django 3.0.5 on 2020-05-09 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablecom', '0006_auto_20200509_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='RLorPro',
            field=models.CharField(choices=[('0', 'Professionnel'), ('1', 'Responsable_Legal')], default='0', max_length=11, verbose_name='Quel est votre statut ? (Professionnel = Enseignant, Professionnel de santé, Responsable légal = Parent, tuteur)'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='phone',
            field=models.CharField(max_length=60, null=True, verbose_name='Téléphone'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='statusRL',
            field=models.CharField(default=' ', max_length=25, verbose_name='Statut si résponsable légal (Mère, Père, Tuteur, ...)'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='username',
            field=models.CharField(max_length=255, verbose_name="Nom d'utilisateur"),
        ),
    ]

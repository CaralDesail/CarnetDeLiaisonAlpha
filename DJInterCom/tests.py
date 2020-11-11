from django.test import TestCase
from datetime import datetime, timedelta
from .models import CorrespondanceTableMessagesByUser
from django.contrib.auth.models import Permission, User

# Create your tests here.
class TravailTest(TestCase):
    def test_minimal(self):
        """Initialisation des tests : Au moins lui doit passer"""
        a = 3.14
        b = 3.14
        self.assertEqual(a,b)



# tests about correspondance Table By User

class CorrespondanceTableTest(TestCase):
    def test_idUserUnique(self):
        for userSel in User.objects.all():
            pkSel = userSel.pk
            print(pkSel)
            lentT=len(CorrespondanceTableMessagesByUser.objects.get(idUser=pkSel))

            self.assertEqual(lentT,1)

    def test_idUserExist(self):
        for userSel in User.objects.all():
            pkSel = userSel.pk
            print(pkSel)
            exist=(CorrespondanceTableMessagesByUser.objects.get(idUser=pkSel)!=None)
            print(exist)


            self.assertEqual(exist, 1)


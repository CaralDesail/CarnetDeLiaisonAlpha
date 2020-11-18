from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
from .views import *
from .models import *
from .urls import *


class TestDeTest(TestCase):

    def test_de_demonstration(self):
        """
        test de bon fonctionnement ... des tests !
        :return:
        True
        """
        a=10
        b=12
        c=2
        b-=c
        self.assertIs(a,b)

class modules_complementaires_test(TestCase):

    def test_list_of_prof(self):
        """va tester si la fonction nous renvoie bien la liste vide des objets profs puisque non loggué"""
        stringAtester="15;18;20"
        result=list_of_prof(request,stringAtester,1)
        self.assertIs(len(result),0)

class url_test(TestCase):

    def test_connexion_access(self):
        """ va tester le bon acces à la page de connexion sans login"""
        response=self.client.get(reverse('connexion'))
        self.assertIs(response.status_code,200)
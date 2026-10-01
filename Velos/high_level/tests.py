
from django.test import TestCase

from .models import (
    Pays,
    Ville,
    Machine,
    QuantiteMachine,
    Lieu,
)


class CostsTests(TestCase):
    def test_lieu_costs(self):
        france = Pays.objects.create(
            nom="France",
            tva=20,
            tarif_electrique=0.2,
            salaire_minimum=12,
        )

        labege = Ville.objects.create(
            nom="Labège",
            pays=france,
            prix_m2=2_000,
            texe_immobiliere=0,
        )

        machine_1 = Machine.objects.create(
            nom="Machine 1",
            prix=10_000,
            duree_de_vie=1,
            cout_maintenance=0,
            superficie=1,
        )

        machine_2 = Machine.objects.create(
            nom="Machine 2",
            prix=5_000,
            duree_de_vie=1,
            cout_maintenance=0,
            superficie=1,
        )

        quantite_machine_1 = QuantiteMachine.objects.create(
            nombre=1,
            machine=machine_1,
        )

        quantite_machine_2 = QuantiteMachine.objects.create(
            nombre=1,
            machine=machine_2,
        )

        lieu = Lieu.objects.create(
            nom="Local Labège",
            ville=labege,
            superficie=50,
            consommation_electrique=5_000,
        )

        lieu.quantite_machines.add(
            quantite_machine_1,
            quantite_machine_2,
        )

        self.assertEqual(
            Lieu.objects.first().costs(),
            111_000,
        )
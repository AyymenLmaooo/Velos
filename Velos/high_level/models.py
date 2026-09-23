from django.db import models


class Pays(models.Model):
    nom = models.CharField(max_length=100)
    tva = models.IntegerField()
    tarif_electrique = models.IntegerField()
    salaire_minimum = models.IntegerField()


class Ville(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.ForeignKey(
        Pays,
        on_delete=models.PROTECT,
    )
    prix_m2 = models.IntegerField()
    texe_immobiliere = models.IntegerField()


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()
    duree_de_vie = models.IntegerField()
    cout_maintenance = models.IntegerField()
    superficie = models.IntegerField()


class QuantiteMachine(models.Model):
    nombre = models.IntegerField()
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
    )


class Lieu(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(
        Ville,
        on_delete=models.PROTECT,
    )
    superficie = models.IntegerField()
    quantite_machines = models.ManyToManyField(QuantiteMachine)
    consommation_electrique = models.IntegerField()


class Transport(models.Model):
    nombre_palettes = models.IntegerField()
    cout = models.IntegerField()
    delai = models.IntegerField()

    depart = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
    )
    arrivee = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
    )


class Operation(models.Model):
    nom = models.CharField(max_length=100)
    operation_suivante = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
    )
    cout = models.IntegerField()
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
    )
    quantite_produits = models.IntegerField()
    heures_de_travail = models.IntegerField()
    consommation_electrique = models.IntegerField()


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_de_vente = models.IntegerField()
    duree_de_vie = models.IntegerField()
    nombre_par_palette = models.IntegerField()
    operations = models.ManyToManyField(Operation)


class QuantiteProduit(models.Model):
    nombre = models.IntegerField()
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
    )


class Stock(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    palettes_max = models.IntegerField()


class PointDeVente(models.Model):
    nom = models.CharField(max_length=100)
    lieu = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
    )
    heures_de_travail = models.IntegerField()
    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
    )


class Facture(models.Model):
    quantite_preoduits = models.ManyToManyField(QuantiteProduit)
    reduction = models.IntegerField()
    point_de_vente = models.ForeignKey(
        PointDeVente,
        on_delete=models.PROTECT,
    )
    client = models.CharField(max_length=100)


class PrixProduit(models.Model):
    prix_achat = models.IntegerField()
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
    )


class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    prix_produits = models.ManyToManyField(PrixProduit)

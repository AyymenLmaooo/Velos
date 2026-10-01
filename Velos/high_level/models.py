from django.db import models


class Pays(models.Model):
    nom = models.CharField(max_length=100)
    tva = models.FloatField()
    tarif_electrique = models.FloatField()
    salaire_minimum = models.FloatField()

    def __str__(self):
        return self.nom



class Ville(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.ForeignKey(
        Pays,
        on_delete=models.PROTECT,
    )
    prix_m2 = models.FloatField()
    texe_immobiliere = models.FloatField()

    def __str__(self):
        return self.nom


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.FloatField()
    duree_de_vie = models.FloatField()
    cout_maintenance = models.FloatField()
    superficie = models.FloatField()

    def __str__(self):
        return self.nom

    def costs(self):
        return self.prix + self.cout_maintenance


class QuantiteMachine(models.Model):
    nombre = models.IntegerField()
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.nombre} x {self.machine}"

    def costs(self):
        return self.nombre * self.machine.costs()


class Lieu(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.ForeignKey(
        Ville,
        on_delete=models.PROTECT,
    )
    superficie = models.IntegerField()
    quantite_machines = models.ManyToManyField(QuantiteMachine)
    consommation_electrique = models.IntegerField()

    def __str__(self):
        return self.nom

    def costs(self):
        return (
            self.superficie * (self.ville.prix_m2 + self.ville.texe_immobiliere)
            + self.consommation_electrique * self.ville.pays.tarif_electrique
            + sum(qm.costs() for qm in self.quantite_machines.all())
        )


class Transport(models.Model):
    nombre_palettes = models.IntegerField()
    cout = models.IntegerField()
    delai = models.IntegerField()

    depart = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
        related_name="transports_depart",
    )
    arrivee = models.ForeignKey(
        Lieu,
        on_delete=models.PROTECT,
        related_name="transports_arrivee",
    )

    def __str__(self):
        return f"{self.depart} -> {self.arrivee}"

    def costs(self):
        return self.cout * self.nombre_palettes

class Operation(models.Model):
    nom = models.CharField(max_length=100)
    operation_suivante = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    cout = models.IntegerField()
    machine = models.ForeignKey(
        Machine,
        on_delete=models.PROTECT,
    )
    quantite_produits = models.ForeignKey(
        "QuantiteProduit",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    heures_de_travail = models.IntegerField()
    consommation_electrique = models.IntegerField()


    def __str__(self):
        return str(self.nom)

    def costs(self):
        return self.cout + self.heures_de_travail * self.consommation_electrique

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    prix_de_vente = models.IntegerField()
    duree_de_vie = models.IntegerField()
    nombre_par_palette = models.IntegerField()
    operations = models.ManyToManyField(Operation)

    def __str__(self):
        return str(self.nom)

    def costs(self):
        return sum(operation.costs() for operation in self.operations.all())


class QuantiteProduit(models.Model):
    nombre = models.IntegerField()
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.produit} x {self.nombre}"

    def costs(self):
        return self.nombre * self.produit.costs()

class Stock(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    palettes_max = models.IntegerField()

    def __str__(self):
        return f"Stock {self.pk}"

    def costs(self):
        return sum(qp.costs() for qp in self.quantite_produits.all())


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

    def __str__(self):
        return self.nom

    def costs(self):
        return self.lieu.costs() + self.stock.costs()


class Facture(models.Model):
    quantite_produits = models.ManyToManyField(QuantiteProduit)
    reduction = models.IntegerField()
    point_de_vente = models.ForeignKey(
        PointDeVente,
        on_delete=models.PROTECT,
    )
    client = models.CharField(max_length=100)

    def __str__(self):
        return f"Facture {self.pk} - {self.client}"

    def costs(self):
        return sum(qp.costs() for qp in self.quantite_produits.all()) - self.reduction


class PrixProduit(models.Model):
    prix_achat = models.IntegerField()
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.produit} - {self.prix_achat}"

    def costs(self):
        return self.prix_achat


class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    prix_produits = models.ManyToManyField(PrixProduit)

    def __str__(self):
        return self.nom

    def costs(self):
        return sum(pp.costs() for pp in self.prix_produits.all())

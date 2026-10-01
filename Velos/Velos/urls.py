"""
URL configuration for Velos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

import high_level.views


urlpatterns = [
    path("admin/", admin.site.urls),


path(
        "pays/<int:pk>",
        high_level.views.PaysDetailView.as_view(),
        name="pays",
    ),

path(
        "ville/<int:pk>",
        high_level.views.VilleDetailView.as_view(),
        name="ville",
    ),

path(
        "machine/<int:pk>",
        high_level.views.MachineDetailView.as_view(),
        name="machine",
    ),

path(
        "quantite-machine/<int:pk>",
        high_level.views.QuantiteMachineDetailView.as_view(),
        name="quantite-machine",
    ),

path(
        "lieu/<int:pk>",
        high_level.views.LieuDetailView.as_view(),
        name="lieu",
    ),

path(
        "transport/<int:pk>",
        high_level.views.TransportDetailView.as_view(),
        name="transport",
    ),

path(
        "operation/<int:pk>",
        high_level.views.OperationDetailView.as_view(),
        name="operation",
    ),

path(
        "produit/<int:pk>",
        high_level.views.ProduitDetailView.as_view(),
        name="produit",
    ),

path(
        "quantite-produit/<int:pk>",
        high_level.views.QuantiteProduitDetailView.as_view(),
        name="quantite-produit",
    ),

path(
        "stock/<int:pk>",
        high_level.views.StockDetailView.as_view(),
        name="stock",
    ),

path(
        "point-de-vente/<int:pk>",
        high_level.views.PointDeVenteDetailView.as_view(),
        name="point-de-vente",
    ),

path(
        "facture/<int:pk>",
        high_level.views.FactureDetailView.as_view(),
        name="facture",
    ),

path(
        "prix-produit/<int:pk>",
        high_level.views.PrixProduitDetailView.as_view(),
        name="prix-produit",
    ),

path(
        "fournisseur/<int:pk>",
        high_level.views.FournisseurDetailView.as_view(),
        name="fournisseur",
    ),
]
from rest_framework import viewsets
from .models import Ingredient, Recipe, MeasurementUnit, RecipeIngredient
from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    MeasurementUnitSerializer,
    RecipeIngredientSerializer,
)


class MeasurementUnitViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing measurement unit instances.
    """

    queryset = MeasurementUnit.objects.all()
    serializer_class = MeasurementUnitSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing recipe instances.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ingredient instances.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing recipiesingredient instances.
    """

    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

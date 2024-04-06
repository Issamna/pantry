from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeIngredient, MeasurementUnit


class MeasurementUnitSerializer(serializers.ModelSerializer):
    """
    Serializer for MeasurementUnit model.
    """

    class Meta:
        model = MeasurementUnit
        fields = ["id", "name"]


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed ingredient information, including the measurement unit.
    """

    measurement_unit = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "calories",
            "fats",
            "proteins",
            "carbohydrates",
            "measurement_unit",
        ]


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for Recipe model, integrating ingredients with their quantities and measurement units.
    """

    ingredients = IngredientSerializer(many=True, read_only=True)
    calories_per_serving = serializers.ReadOnlyField()
    total_fats = serializers.ReadOnlyField()
    total_proteins = serializers.ReadOnlyField()
    total_carbohydrates = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "instructions",
            "servings",
            "ingredients",
            "calories_per_serving",
            "total_fats",
            "total_proteins",
            "total_carbohydrates",
        ]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ["id", "recipe", "ingredient", "quantity"]

from django.test import TestCase
from pantry_api.models import Recipe, Ingredient, MeasurementUnit, RecipeIngredient

class MeasurementUnitTest(TestCase):
    """Tests for the MeasurementUnit model."""

    def test_measurement_unit_creation(self):
        unit = MeasurementUnit.objects.create(name="Cup")
        self.assertEqual(unit.name, "Cup")

class IngredientTest(TestCase):
    """Tests for the Ingredient model."""

    def setUp(self):
        MeasurementUnit.objects.create(name="Tablespoon")

    def test_ingredient_creation(self):
        unit = MeasurementUnit.objects.first()
        ingredient = Ingredient.objects.create(
            name="Flour", 
            calories=364, 
            fats=1, 
            proteins=10, 
            carbohydrates=76,
            measurement_unit=unit
        )
        self.assertEqual(ingredient.name, "Flour")
        self.assertEqual(ingredient.measurement_unit.name, "Tablespoon")

class RecipeTest(TestCase):
    """Tests for the Recipe model."""

    def test_recipe_creation(self):
        recipe = Recipe.objects.create(
            name="Pancakes",
            instructions="Mix ingredients. Cook on griddle.",
            servings=4
        )
        self.assertEqual(recipe.name, "Pancakes")
        self.assertEqual(recipe.servings, 4)

class RecipeIngredientTest(TestCase):
    """Tests for the RecipeIngredient model."""

    def setUp(self):
        self.unit = MeasurementUnit.objects.create(name="Teaspoon")
        self.ingredient = Ingredient.objects.create(
            name="Sugar", 
            calories=49, 
            fats=0, 
            proteins=0, 
            carbohydrates=13,
            measurement_unit=self.unit
        )
        self.recipe = Recipe.objects.create(
            name="Sugar Cookies",
            instructions="Mix ingredients. Bake.",
            servings=12
        )

    def test_recipe_ingredient_creation(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=2
        )
        self.assertEqual(recipe_ingredient.recipe.name, "Sugar Cookies")
        self.assertEqual(recipe_ingredient.ingredient.name, "Sugar")
        self.assertEqual(recipe_ingredient.quantity, 2)

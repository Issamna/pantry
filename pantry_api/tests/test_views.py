from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from pantry_api.models import Recipe, MeasurementUnit, Ingredient, RecipeIngredient

class RecipeViewSetTest(APITestCase):
    """Test suite for the Recipe viewset CRUD operations."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.recipe_data = {'name': 'Cheesecake', 'instructions': 'Mix and bake.', 'servings': 8}
        self.response = self.client.post(
            reverse('recipe-list'),
            self.recipe_data,
            format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        self.recipe = Recipe.objects.get(id=self.response.data['id'])

    def test_retrieve_recipe(self):
        """Test retrieving a recipe."""
        response = self.client.get(
            reverse('recipe-detail', kwargs={'pk': self.recipe.id}),
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.recipe_data['name'])

    def test_update_recipe(self):
        """Test updating a recipe with put."""
        update_data = {'name': 'Updated Cheesecake', 'instructions': 'New instructions', 'servings': 12}
        response = self.client.put(
            reverse('recipe-detail', kwargs={'pk': self.recipe.id}),
            update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.name, update_data['name'])
        self.assertEqual(self.recipe.instructions, update_data['instructions'])
        self.assertEqual(self.recipe.servings, update_data['servings'])

    def test_partial_update_recipe(self):
        """Test updating a recipe with patch."""
        partial_update_data = {'name': 'Partially Updated Cheesecake'}
        response = self.client.patch(
            reverse('recipe-detail', kwargs={'pk': self.recipe.id}),
            partial_update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.name, partial_update_data['name'])

    def test_delete_recipe(self):
        """Test deleting a recipe."""
        response = self.client.delete(
            reverse('recipe-detail', kwargs={'pk': self.recipe.id}),
            format='json',
            follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=self.recipe.id).exists())


class MeasurementUnitViewSetTest(APITestCase):
    """Test suite for the MeasurementUnit viewset."""

    def setUp(self):
        """Create an initial measurement unit to be used in the tests."""
        self.measurement_unit = MeasurementUnit.objects.create(name="Teaspoon")
        self.valid_payload = {'name': 'Cup'}
        self.invalid_payload = {'name': ''}  # Assuming 'name' is a required field

    def test_create_measurement_unit(self):
        """Ensure we can create a new measurement unit object."""
        url = reverse('measurementunit-list')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MeasurementUnit.objects.count(), 2)
        self.assertEqual(MeasurementUnit.objects.get(id=2).name, 'Cup')

    def test_retrieve_measurement_unit(self):
        """Test retrieving a measurement unit."""
        url = reverse('measurementunit-detail', kwargs={'pk': self.measurement_unit.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.measurement_unit.name)

    def test_update_measurement_unit(self):
        """Test updating an existing measurement unit."""
        url = reverse('measurementunit-detail', kwargs={'pk': self.measurement_unit.id})
        response = self.client.put(url, {'name': 'Updated Name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.measurement_unit.refresh_from_db()
        self.assertEqual(self.measurement_unit.name, 'Updated Name')

    def test_partial_update_measurement_unit(self):
        """Test partially updating an existing measurement unit."""
        url = reverse('measurementunit-detail', kwargs={'pk': self.measurement_unit.id})
        response = self.client.patch(url, {'name': 'Partially Updated'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.measurement_unit.refresh_from_db()
        self.assertEqual(self.measurement_unit.name, 'Partially Updated')

    def test_delete_measurement_unit(self):
        """Ensure we can delete a measurement unit object."""
        url = reverse('measurementunit-detail', kwargs={'pk': self.measurement_unit.id})
        response = self.client.delete(url, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MeasurementUnit.objects.filter(id=self.measurement_unit.id).exists())


class IngredientViewSetTest(APITestCase):
    """Test suite for the Ingredient viewset."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.measurement_unit = MeasurementUnit.objects.create(name="Cup")
        self.ingredient_data = {'name': 'Flour', 'calories': 364, 'measurement_unit': self.measurement_unit.id}
        self.response = self.client.post(
            reverse('ingredient-list'),
            self.ingredient_data,
            format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.ingredient = Ingredient.objects.get(id=self.response.data['id'])

    def test_retrieve_ingredient(self):
        """Test retrieving an ingredient."""
        response = self.client.get(
            reverse('ingredient-detail', kwargs={'pk': self.ingredient.id}),
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.ingredient_data['name'])

    def test_update_ingredient(self):
        """Test updating an ingredient with put."""
        updated_data = {'name': 'Sugar', 'calories': 387, 'measurement_unit': self.measurement_unit.id}
        response = self.client.put(
            reverse('ingredient-detail', kwargs={'pk': self.ingredient.id}),
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ingredient.refresh_from_db()
        self.assertEqual(self.ingredient.name, updated_data['name'])

    def test_partial_update_ingredient(self):
        """Test updating an ingredient with patch."""
        partial_update_data = {'name': 'Butter'}
        response = self.client.patch(
            reverse('ingredient-detail', kwargs={'pk': self.ingredient.id}),
            partial_update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ingredient.refresh_from_db()
        self.assertEqual(self.ingredient.name, partial_update_data['name'])

    def test_delete_ingredient(self):
        """Test deleting an ingredient."""
        response = self.client.delete(
            reverse('ingredient-detail', kwargs={'pk': self.ingredient.id}),
            format='json',
            follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(id=self.ingredient.id).exists())


class RecipeIngredientViewSetTest(APITestCase):
    """Test suite for the RecipeIngredient viewset."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.recipe = Recipe.objects.create(name="Chocolate Cake", instructions="Mix and bake.", servings=8)
        self.ingredient = Ingredient.objects.create(name="Chocolate", calories=546)
        self.recipe_ingredient_data = {'recipe': self.recipe.id, 'ingredient': self.ingredient.id, 'quantity': 2}
        self.response = self.client.post(
            reverse('recipeingredient-list'),
            self.recipe_ingredient_data,
            format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.recipe_ingredient = RecipeIngredient.objects.get(id=self.response.data['id'])

    def test_retrieve_recipe_ingredient(self):
        """Test retrieving a recipe ingredient."""
        response = self.client.get(
            reverse('recipeingredient-detail', kwargs={'pk': self.recipe_ingredient.id}),
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['quantity']), Decimal(self.recipe_ingredient_data['quantity']))

    def test_update_recipe_ingredient(self):
        """Test updating a recipe ingredient with put."""
        updated_data = {'recipe': self.recipe.id, 'ingredient': self.ingredient.id, 'quantity': 3}
        response = self.client.put(
            reverse('recipeingredient-detail', kwargs={'pk': self.recipe_ingredient.id}),
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe_ingredient.refresh_from_db()
        self.assertEqual(self.recipe_ingredient.quantity, updated_data['quantity'])

    def test_partial_update_recipe_ingredient(self):
        """Test partially updating a recipe ingredient with patch."""
        partial_update_data = {'quantity': 1.5}
        response = self.client.patch(
            reverse('recipeingredient-detail', kwargs={'pk': self.recipe_ingredient.id}),
            partial_update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe_ingredient.refresh_from_db()
        self.assertEqual(self.recipe_ingredient.quantity, partial_update_data['quantity'])

    def test_delete_recipe_ingredient(self):
        """Test deleting a recipe ingredient."""
        response = self.client.delete(
            reverse('recipeingredient-detail', kwargs={'pk': self.recipe_ingredient.id}),
            format='json',
            follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RecipeIngredient.objects.filter(id=self.recipe_ingredient.id).exists())
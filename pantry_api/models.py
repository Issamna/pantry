from django.db import models


class MeasurementUnit(models.Model):
    """
    Represents a unit of measurement for ingredients, such as cup, tablespoon, or piece.
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Represents an ingredient used in recipes, including its name, caloric value, and macronutrients.
    Measurement unit for this ingredient is defined to standardize recipes.
    """

    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    proteins = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    measurement_unit = models.ForeignKey(
        MeasurementUnit, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.name} ({self.calories} calories)"


class Recipe(models.Model):
    """
    Represents a cooking recipe, which includes a name, cooking instructions, and the number of servings.
    This model also provides properties to calculate nutritional values per serving.
    """

    name = models.CharField(max_length=255)
    instructions = models.TextField()
    servings = models.IntegerField(default=1)
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient", related_name="recipes"
    )

    def __str__(self):
        return self.name

    @property
    def calories_per_serving(self):
        """
        Calculates the total calories per serving of the recipe.
        """
        total_calories = sum(
            [
                ri.quantity * ri.ingredient.calories
                for ri in self.recipeingredient_set.all()
            ]
        )
        return total_calories / self.servings if self.servings else 0

    @property
    def total_fats(self):
        """
        Calculates the total fats in grams for the recipe.
        """
        return sum(
            [ri.quantity * ri.ingredient.fats for ri in self.recipeingredient_set.all()]
        )

    @property
    def total_proteins(self):
        """
        Calculates the total proteins in grams for the recipe.
        """
        return sum(
            [
                ri.quantity * ri.ingredient.proteins
                for ri in self.recipeingredient_set.all()
            ]
        )

    @property
    def total_carbohydrates(self):
        """
        Calculates the total carbohydrates in grams for the recipe.
        """
        return sum(
            [
                ri.quantity * ri.ingredient.carbohydrates
                for ri in self.recipeingredient_set.all()
            ]
        )


class RecipeIngredient(models.Model):
    """
    A bridge model between Recipe and Ingredient to specify the quantity of each ingredient used in a recipe.
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=5, decimal_places=2
    )  # The quantity of the ingredient in the recipe

    def __str__(self):
        return f"{self.quantity} of {self.ingredient} for {self.recipe}"

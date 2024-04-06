from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, RecipeViewSet, MeasurementUnitViewSet, RecipeIngredientViewSet

router = DefaultRouter()
router.register(r"ingredients", IngredientViewSet)
router.register(r"recipes", RecipeViewSet)
router.register(r"measurementunits", MeasurementUnitViewSet)
router.register(r'recipeingredients', RecipeIngredientViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

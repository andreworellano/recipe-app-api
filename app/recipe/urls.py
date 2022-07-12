"""
URL mappings for the recipe app
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
# auto generated urls based on the view set
router.register('recipes', views.RecipeViewSet)

# for reverse lookup in tests
app_name = 'recipe'

# retrieves available urls
urlpatterns = [
    path('', include(router.urls))
]

from django.urls import path, include
from .serializer import RatingSerializer, MealSerializer
from rest_framework import routers
from .views import MealViewSet, RatingViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('meals', MealViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls))
]

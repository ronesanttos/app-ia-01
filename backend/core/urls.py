from django.urls import path
from rest_framework.routers import DefaultRouter #type:ignore
from .views import ListaViewSet

router = DefaultRouter()
router.register(r'listas', ListaViewSet, basename='listas')

urlpatterns = router.urls

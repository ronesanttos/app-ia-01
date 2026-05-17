from django.contrib import admin
from django.urls import path,include
from core import views
urlpatterns = [
    path('api/', include('core.urls')),
    path('admin/', admin.site.urls),
    path("health/", views.health, name="health"),
]
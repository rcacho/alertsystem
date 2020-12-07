from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alerts import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'glucose-points', views.GlucosePointViewSet)
router.register(r'alert-settings', views.AlertSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
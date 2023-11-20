"""
URL mappings for the content app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from content import views


router = DefaultRouter()
router.register('contents', views.ContentViewSet)

app_name = 'content'

urlpatterns = [
    path('', include(router.urls)),
]

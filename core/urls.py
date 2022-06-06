from django.urls import re_path
from rest_framework.routers import DefaultRouter

from core import viewsets

router = DefaultRouter()
router.register(r'user', viewset=viewsets.UserViewSet)
router.register(r'document', viewset=viewsets.DocumentViewSet)

urlpatterns = router.urls + [
    re_path(
        r'^document/download/(?P<path>.*)$',
        viewsets.DocumentViewSet.as_view({'get': 'download'}),
        name='document-download'
    ),
]

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action

from core import models, serializers, filters, services


# ViewSets define the view behavior.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    filter_class = filters.DocumentFilter
    ordering_fields = '__all__'
    ordering = ('-id',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super(DocumentViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def download(self, request, path, *args, **kwargs):
        rs = serializers.DocumentDownloadSerializer(data=request.query_params)
        rs.is_valid(raise_exception=True)

        service = services.DocumentDownloadService(request=self.request, path=path)
        return service.download(**rs.validated_data)

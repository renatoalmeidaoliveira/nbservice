from rest_framework import viewsets

from nb_service import models
from nb_service import filters
from . import serializers

class ICViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.IC.objects.all()
    serializer_class = serializers.nb_ICserializer
    filterset_class = filters.ICFilter


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.nb_ServiceSerializer

class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.nb_Applicationserializer

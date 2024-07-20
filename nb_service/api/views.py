from netbox.api.viewsets import NetBoxModelViewSet

from nb_service import models
from nb_service import filtersets
from . import serializers

class ICViewSet(NetBoxModelViewSet):
    queryset = models.IC.objects.all()
    serializer_class = serializers.ICSerializer
    filterset_class = filtersets.ICFilter


class ServiceViewSet(NetBoxModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

class ApplicationViewSet(NetBoxModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer

class RelationViewSet(NetBoxModelViewSet):
    queryset = models.Relation.objects.all()
    serializer_class = serializers.RelationSerializer

class PenTestViewSet(NetBoxModelViewSet):
    queryset = models.PenTest.objects.all()
    serializer_class = serializers.PenTestSerializer
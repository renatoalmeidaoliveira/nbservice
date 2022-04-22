"""
from rest_framework.serializers import ModelSerializer

from nb_service.models import MyModel1


class MyModel1Serializer(ModelSerializer):

    class Meta:
        model = MyModel1
        fields = '__all__'
"""
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from netbox.api import ChoiceField, ContentTypeField, WritableNestedSerializer
from utilities.api import get_serializer_for_model
from tenancy.api.nested_serializers import NestedTenantSerializer
from ipam.choices import ServiceProtocolChoices
from dcim.api.nested_serializers import NestedDeviceSerializer
from virtualization.api.nested_serializers import NestedVirtualMachineSerializer

from nb_service import models
from nb_service import choices

class NestedApplicationSerializer(WritableNestedSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    class Meta:
        model = models.Application
        fields = ['id', 'name',]


class nb_Applicationserializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    protocol = ChoiceField(choices=ServiceProtocolChoices, required=False)
    version = serializers.CharField()
    devices = NestedDeviceSerializer(many=True,required=False, allow_null=True)
    vm = NestedVirtualMachineSerializer(many=True,required=False, allow_null=True)


    class Meta:
        model = models.Application
        fields = [
            'id',
            'name',
            'protocol',
            'ports',
            'version',
            'devices',
            'vm',
            ]

class nb_ICserializer(serializers.Serializer):

    name = serializers.CharField(read_only=True)
    display = serializers.SerializerMethodField('get_display')
    service = serializers.CharField(source='service.name', required=False)

    id = serializers.IntegerField(read_only=True)
    service_id = serializers.IntegerField(source='service.id', required=True,)

    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(choices.OBJETO_ASSIGNMENT_MODELS),
        required=True,
        allow_null=True
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    assigned_object_id = serializers.IntegerField(source='assigned_object.id')
    
    def get_display(self, obj):
        return obj.name

    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object, prefix='Nested')
        context = {'request': self.context['request']}
        return serializer(obj.assigned_object, context=context).data


    class Meta:
        model = models.IC
        fields = ['id', 'display', 'name', 'service', 'assigned_object_type', 'assigned_object', 'assigned_object_id']

class nb_ServiceSerializer(serializers.Serializer):

    name = serializers.CharField()
    clients = NestedTenantSerializer(many=True,required=False, allow_null=True)
    comments = serializers.CharField()
    backup_profile = serializers.CharField(required=False)

    class Meta:
        model = models.Service
        fields = ['name', 'clients', 'comments', 'backup_profile']
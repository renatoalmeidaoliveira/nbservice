from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from netbox.api.fields import ChoiceField, ContentTypeField
from netbox.api.serializers import WritableNestedSerializer

from utilities.api import get_serializer_for_model
from tenancy.api.serializers import TenantSerializer

from ipam.choices import ServiceProtocolChoices
from dcim.api.serializers import DeviceSerializer
from virtualization.api.serializers import VirtualMachineSerializer

from netbox.api.serializers import NetBoxModelSerializer

from nb_service import models
from nb_service import choices


class ApplicationSerializer(NetBoxModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    display = serializers.SerializerMethodField("get_display")
    protocol = ChoiceField(choices=ServiceProtocolChoices, required=False)
    version = serializers.CharField()
    devices = DeviceSerializer(many=True, required=False, allow_null=True, nested=True)
    vm = VirtualMachineSerializer(many=True, required=False, allow_null=True, nested=True)

    def get_display(self, obj):
        return f"{obj}"

    class Meta:
        model = models.Application
        fields = [
            "id",
            "display",
            "name",
            "protocol",
            "ports",
            "version",
            "devices",
            "vm",
        ]

    def create(self, validated_data):
        devices = validated_data.pop("devices", None)
        virtual_machines = validated_data.pop("vm", None)

        application = super().create(validated_data)

        if devices is not None:
            application.devices.set(devices)
        if virtual_machines is not None:
            application.vm.set(virtual_machines)

        return application

    def update(self, instance, validated_data):
        devices = validated_data.pop("devices", None)
        virtual_machines = validated_data.pop("vm", None)

        application = super().update(instance, validated_data)

        if devices is not None:
            application.devices.set(devices)
        if virtual_machines is not None:
            application.vm.set(virtual_machines)

        return application


class ICSerializer(serializers.Serializer):

    name = serializers.CharField(read_only=True)
    display = serializers.SerializerMethodField("get_display")
    service = serializers.CharField(source="service.name", required=False)

    id = serializers.IntegerField(read_only=True)
    service_id = serializers.IntegerField(
        source="service.id",
        required=True,
    )

    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(choices.OBJETO_ASSIGNMENT_MODELS),
        required=True,
        allow_null=True,
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    assigned_object_id = serializers.IntegerField(source="assigned_object.id", write_only=True)

    def get_display(self, obj):
        return obj.name

    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, nested=True, context=context).data

    class Meta:
        model = models.IC
        fields = [
            "id",
            "display",
            "name",
            "service",
            "assigned_object_type",
            "assigned_object",
            "assigned_object_id",
        ]


class ServiceSerializer(NetBoxModelSerializer):

    name = serializers.CharField()
    display = serializers.SerializerMethodField("get_display")
    clients = TenantSerializer(many=True, required=False, allow_null=True, nested=True)
    comments = serializers.CharField()
    backup_profile = serializers.CharField(required=False)

    def get_display(self, obj):
        return obj.name

    def create(self, validated_data):
        clients = validated_data.pop("clients", None)

        service = super().create(validated_data)

        if clients is not None:
            service.clients.set(clients)

        return service

    def update(self, instance, validated_data):
        clients = validated_data.pop("clients", None)

        service = super().update(instance, validated_data)

        if clients is not None:
            service.clients.set(clients)

        return service

    class Meta:
        model = models.Service
        fields = ["id", "display", "name", "clients", "comments", "backup_profile"]


class RelationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    service = serializers.SlugRelatedField(
        slug_field="name", queryset=models.Service.objects.all()
    )

    def get_display(self, obj):
        return obj.name

    class Meta:
        model = models.Relation
        fields = [
            "id",
            "display",
            "name",
            "service",
            "source",
            "source_shape",
            "destination",
            "destination_shape",
            "connector_shape",
            "link_text",
        ]

class PenTestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    service = serializers.SlugRelatedField(
        slug_field="name", queryset=models.Service.objects.all()
    )


    class Meta:
        model = models.PenTest
        fields = [
            "id",
            "service",
            "status",
            "comments",
            "date",
            "ticket",
            "report_link"
        ]

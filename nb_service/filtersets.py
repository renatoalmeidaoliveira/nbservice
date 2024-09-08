import django_filters
from django.db.models import Q
from tenancy.models import Tenant
from dcim.models import Device
from virtualization.models import VirtualMachine

from netbox.filtersets import NetBoxModelFilterSet

from . import models

class ICFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    service = django_filters.ModelMultipleChoiceFilter(
        field_name="service__name",
        queryset=models.Service.objects.all(),
        to_field_name="name",
    )
    service_id = django_filters.ModelMultipleChoiceFilter(
        field_name="service__id",
        queryset=models.Service.objects.all(),
        to_field_name="id",
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        ids = []
        for ic in queryset:
            if value in ic.name:
                ids.append(ic.id)
        return queryset.filter(id__in = ids)

    class Meta:
        model = models.IC

        fields = [
            "service",
        ]

class ServiceFilterSet(NetBoxModelFilterSet):

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    clients = django_filters.ModelMultipleChoiceFilter(
        field_name="clients__name",
        queryset=Tenant.objects.all(),
        to_field_name="name",
    )
    clients_id = django_filters.ModelMultipleChoiceFilter(
        field_name="clients__id",
        queryset=Tenant.objects.all(),
        to_field_name="id",
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value) |
            Q(clients__name__icontains=value)
        )
        return queryset.filter(qs_filter)


    class Meta:
        model = models.Service

        fields = [
            "id",
            "name",
            "clients",
            "backup_profile",
        ]

class ApplicationFilterSet(NetBoxModelFilterSet):

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    devices = django_filters.ModelMultipleChoiceFilter(
        field_name="devices__name",
        queryset=Device.objects.all(),
        to_field_name="name",
    )
    devices_id = django_filters.ModelMultipleChoiceFilter(
        field_name="devices__id",
        queryset=Device.objects.all(),
        to_field_name="id",
    )

    virtual_machines = django_filters.ModelMultipleChoiceFilter(
        field_name="vm__name",
        queryset=VirtualMachine.objects.all(),
        to_field_name="name",
    )
    virtual_machines_id = django_filters.ModelMultipleChoiceFilter(
        field_name="vm__id",
        queryset=VirtualMachine.objects.all(),
        to_field_name="id",
    )

    ports = django_filters.NumberFilter(
        field_name="ports",
        lookup_expr="contains",
    )

    def search(self, queryset, name, value):

        if not value.strip():
            return queryset

        qs_filter = (
            Q(name__icontains=value) |
            Q(devices__name__icontains=value) |
            Q(vm__name__icontains=value)
        )

        return queryset.filter(qs_filter).distinct()

    class Meta:
        model = models.Application

        fields = [
            "id",
            "name",
            "protocol",
            "version",
            "devices",
            "virtual_machines",
        ]

class RelationFilter(NetBoxModelFilterSet):

    class Meta:
        model = models.Relation

        fields = [
            "id",
            "service",
        ]

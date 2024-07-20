from django import forms

from dcim.models import Device
from circuits.models import Circuit, Provider
from tenancy.models import Tenant
from ipam.models import Service
from ipam.choices import ServiceProtocolChoices
from ipam.constants import SERVICE_PORT_MIN, SERVICE_PORT_MAX
from virtualization.models import VirtualMachine
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
    DynamicModelChoiceField,
    CSVModelMultipleChoiceField,
    NumericArrayField,
    CSVChoiceField,
)
from utilities.forms.widgets import DatePicker

from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelFilterSetForm,
    NetBoxModelBulkEditForm,
    NetBoxModelImportForm,
)

from . import models

class ServiceForm(NetBoxModelForm):

    clients = DynamicModelMultipleChoiceField(label="Clients",
        queryset=Tenant.objects.all(),
        required=False,
    )

    backup_profile = forms.CharField(required=False)

    class Meta:
        model = models.Service
        fields = [
            "name",
            "clients",
            "comments",
            "backup_profile",
        ]

class ApplicationForm(NetBoxModelForm):

    ports = NumericArrayField(
        label="Ports",
        base_field=forms.IntegerField(
            min_value=SERVICE_PORT_MIN,
            max_value=SERVICE_PORT_MAX
        ),
    )
    devices = DynamicModelMultipleChoiceField(label="Devices",
        queryset=Device.objects.all(),
        required=False,
    )
    vm = DynamicModelMultipleChoiceField(label="Virtual Machines",
        queryset=VirtualMachine.objects.all(),
        required=False,
    )


    class Meta:
        model = models.Application
        fields = [
            "name",
            "protocol",
            "ports",
            "version",
            "devices",
            "vm",
        ]

class ICForm(NetBoxModelForm):

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
    )

    application = DynamicModelChoiceField(
        queryset=models.Application.objects.all(),
        required=False,
    )

    class Meta:
        model = models.IC
        fields = [
            'service',
        ]


class PenTestForm(NetBoxModelForm):

    class Meta:
        model = models.PenTest
        fields = [
            'service',
            'comments',
            'status',
            'date',
            'ticket',
            "report_link",
        ]

        widgets = {
            'date': DatePicker(),
        }

class RelationForm(NetBoxModelForm):

    source = DynamicModelChoiceField(
        queryset=models.IC.objects.all(),
        required=True,
        label='Source',
        query_params={
            'service_id': '$service',
        },
    )

    destination = DynamicModelChoiceField(
        queryset=models.IC.objects.all(),
        required=True,
        label='Destination',
        query_params={
            'service_id': '$service',
        },
    )

    link_text = forms.CharField(required=False)

    class Meta:
        model = models.Relation
        fields = [
            'service',
            'source',
            'source_shape',
            'destination',
            'destination_shape',
            "connector_shape",
            "link_text",
        ]

class RelationFilterForm(NetBoxModelFilterSetForm):
    model = models.Relation

    class Meta:
        fields = [
            'service',
            'source',
            'source_shape',
            'destination',
            'destination_shape',
            "connector_shape",
            "link_text",
        ]


class ServiceFilterForm(forms.ModelForm):

    q = forms.CharField(
        required=False,
        label='Search'
    )
    clients = DynamicModelMultipleChoiceField(
        label="Clients",
        queryset=Tenant.objects.all(),
        required=False,
    )

    class Meta:
        model = models.Service
        fields = [
            'q',
            'clients',
        ]

class ServiceBulkEditForm(NetBoxModelBulkEditForm):
    model = models.Service

    clients = DynamicModelMultipleChoiceField(
        label="Clients",
        queryset=Tenant.objects.all(),
        required=False,
    )
    comments = forms.Textarea(
        attrs={'class': 'font-monospace'}
    )
    backup_profile = forms.CharField(
        required=False,
    )

    class Meta:
        nullable_fields = ("clients", "comments", "backup_profile")

class ServiceImportForm(NetBoxModelImportForm):
    clients = CSVModelMultipleChoiceField(
        label="Clients",
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": "Client name not found",
        }
    )

    class Meta:
        model = models.Service
        fields = ["name", "clients", "comments", "backup_profile"]


class ApplicationFilterForm(forms.ModelForm):

    q = forms.CharField(
        required=False,
        label='Search'
    )
    devices = DynamicModelMultipleChoiceField(label="Devices",
        queryset=Device.objects.all(),
        required=False,
    )

    virtual_machines = DynamicModelMultipleChoiceField(label="Virtual Machines",
        queryset=VirtualMachine.objects.all(),
        required=False,
    )

    class Meta:
        model = models.Service
        fields = [
            'q',
            'devices',
            'virtual_machines',
        ]

class ApplicationImportForm(NetBoxModelImportForm):

    devices = CSVModelMultipleChoiceField(
        label="Devices",
        queryset=Device.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": "Device name not found",
        }
    )
    vm = CSVModelMultipleChoiceField(
        label="Virtual Machines",
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name="name",
        error_messages={
            "invalid_choice": "Virtual machine name not found",
        }
    )

    class Meta:
        model = models.Application
        fields = ["name", "protocol", "ports", "version", "devices", "vm"]

class ApplicationBulkEditForm(NetBoxModelBulkEditForm):
    model = models.Application

    ports = NumericArrayField(
        label="Ports",
        base_field=forms.IntegerField(
            min_value=SERVICE_PORT_MIN,
            max_value=SERVICE_PORT_MAX
        ),
        help_text="Comma-separated list of one or more port numbers. A range may be specified using a hyphen.",
        required=False,
    )
    protocol = CSVChoiceField(
        label="Protocol",
        choices=ServiceProtocolChoices,
    )
    devices = DynamicModelMultipleChoiceField(
        label="Devices",
        queryset=Device.objects.all(),
        required=False,
    )
    vm = DynamicModelMultipleChoiceField(
        label="Virtual Machines",
        queryset=VirtualMachine.objects.all(),
        required=False,
    )

    class Meta:
        fields = ["protocol", "ports", "version", "devices", "vm"]
        nullable_fields = ("devices", "vm")

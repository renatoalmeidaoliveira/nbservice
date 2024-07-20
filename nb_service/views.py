from . import models
from . import filtersets
from . import forms
from . import tables

from netbox.views import generic
from tenancy.tables import TenantTable
from virtualization.models import VirtualMachine
from dcim.models import Device
from dcim.tables import DeviceTable
from virtualization.tables import VirtualMachineTable
from utilities.views import ViewTab, register_model_view




class ServiceListView(generic.ObjectListView):
    queryset = models.Service.objects.all()
    table = tables.ServiceTable
    filterset = filtersets.ServiceFilterSet
    filterset_form = forms.ServiceFilterForm

class ServiceView(generic.ObjectView):
    queryset = models.Service.objects.all()

    def get_extra_context(self, request, instance):
        tenants_table = TenantTable(instance.clients.all())
        vuln_table = tables.VulnTable(instance.pentest_reports.all())

        data = {
                "tenant_table" : tenants_table,
                "vuln_table" : vuln_table,
            }
        return data

@register_model_view(models.Service, name='IC')
class ServiceICView(generic.ObjectChildrenView):
    queryset = models.Service.objects.all()
    table = tables.ICTable
    template_name = "nb_service/service_IC_view.html"
    tab = ViewTab(label='IC', badge=lambda obj: obj.config_itens.all().count(), hide_if_empty=True)

    def get_children(self, request, parent):
            childrens = parent.config_itens.all()
            return childrens



@register_model_view(models.Service, name='Relationships')
class ServiceRelationView(generic.ObjectChildrenView):
    queryset = models.Service.objects.all()
    child_model = models.Relation
    table = tables.RelationTable
    template_name = "nb_service/service_Relation_view.html"
    tab = ViewTab(label='Relationships', badge=lambda obj: obj.relationships.all().count(), hide_if_empty=True)

    def get_children(self, request, parent):
            childrens = parent.relationships.all()
            return childrens

    def get_extra_context(self, request, instance):
        relations = tables.RelationTable(instance.relationships.all())
        data = {
                "table" : relations,
            }
        return data

@register_model_view(models.Service, name='Diagram')
class ServiceDiagramView(generic.ObjectChildrenView):
    queryset = models.Service.objects.all()
    child_model = models.Service
    table = tables.ServiceTable
    template_name = "nb_service/service_diagram_view.html"
    tab = ViewTab(label='Diagram')

    def get_children(self, request, parent):
            childrens = parent.relationships.all()
            return childrens

class ServiceEditView(generic.ObjectEditView):
    queryset = models.Service.objects.all()
    form  = forms.ServiceForm


class ServiceImportView(generic.BulkImportView):
    queryset = models.Service.objects.all()
    model_form = forms.ServiceImportForm
    table = tables.ServiceTable

class ServiceBulkEditView(generic.BulkEditView):
    queryset = models.Service.objects.all()
    filterset = filtersets.ServiceFilterSet
    table = tables.ServiceTable
    form = forms.ServiceBulkEditForm

class ServiceBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Service.objects.all()
    table = tables.ServiceTable

class ServiceDeleteView(generic.ObjectDeleteView):
    queryset = models.Service.objects.all()


class ICCreateView(generic.ObjectEditView):
    queryset = models.IC.objects.all()
    form = forms.ICForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        if 'device' in request.POST:
            try:
                obj.assigned_object =  Device.objects.get(pk=request.POST['device'])
            except (ValueError, Device.DoesNotExist):
                pass

        if 'virtual_machine' in request.POST:
            try:
                obj.assigned_object =  VirtualMachine.objects.get(pk=request.POST['virtual_machine'])
            except (ValueError, Device.DoesNotExist):
                pass
        if 'application' in request.POST:
            try:
                obj.assigned_object =  models.Application.objects.get(pk=request.POST['application'])
            except (ValueError, Device.DoesNotExist):
                pass

        return obj


class RelationEditView(generic.ObjectEditView):
    queryset = models.Relation.objects.all()
    form = forms.RelationForm

class PenTestEditView(generic.ObjectEditView):
    queryset = models.PenTest.objects.all()
    form = forms.PenTestForm

class PenTestDeleteView(generic.ObjectDeleteView):
    queryset = models.PenTest.objects.all()

class RelationDeleteView(generic.ObjectDeleteView):
    queryset = models.Relation.objects.all()

class ICDeleteView(generic.ObjectDeleteView):
    queryset = models.IC.objects.all()


class ApplicationListView(generic.ObjectListView):
    queryset = models.Application.objects.all()
    table = tables.ApplicationTable
    filterset = filtersets.ApplicationFilterSet
    filterset_form = forms.ApplicationFilterForm


class ApplicationView(generic.ObjectView):
    queryset = models.Application.objects.all()

@register_model_view(models.Application, name='Devices')
class ApplicationDevicesView(generic.ObjectChildrenView):
    queryset = models.Application.objects.all()
    child_model = Device
    table = DeviceTable
    template_name = "nb_service/application_objs.html"
    tab = ViewTab(label='Devices', badge=lambda obj: obj.devices.all().count(), hide_if_empty=True)

    def get_children(self, request, parent):
            childrens = parent.devices.all()
            return childrens
    
    def get_extra_context(self, request, instance):
        device_table = DeviceTable(instance.devices.all())
        device_table.exclude = ('actions',)
        data = {
                "table" : device_table,
            }
        return data

@register_model_view(models.Application, name='VMs')
class ApplicationVMsView(generic.ObjectChildrenView):
    queryset = models.Application.objects.all()
    child_model = VirtualMachine
    table = VirtualMachineTable
    template_name = "nb_service/application_objs.html"
    tab = ViewTab(label='Virtual Machines', badge=lambda obj: obj.vm.all().count(), hide_if_empty=True)

    def get_children(self, request, parent):
            childrens = parent.vm.all()
            return childrens

    def get_extra_context(self, request, instance):
        vm_table = VirtualMachineTable(instance.vm.all())
        vm_table.exclude = ('actions',)
        data = {
                "table" : vm_table,
            }
        return data

class ApplicationEditView(generic.ObjectEditView):
    queryset = models.Application.objects.all()
    form = forms.ApplicationForm


class ApplicationImportView(generic.BulkImportView):
    queryset = models.Application.objects.all()
    model_form = forms.ApplicationImportForm
    table = tables.ApplicationTable

class ApplicationBulkEditView(generic.BulkEditView):
    queryset = models.Application.objects.all()
    filterset = filtersets.ApplicationFilterSet
    table = tables.ApplicationTable
    form = forms.ApplicationBulkEditForm

class ApplicationBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Application.objects.all()
    table = tables.ApplicationTable

class ApplicationDeleteView(generic.ObjectDeleteView):
    queryset = models.Application.objects.all()

class RelationListView(generic.ObjectListView):
    queryset = models.Relation.objects.all()
    table = tables.RelationTable
    filterset = filtersets.RelationFilter
    filterset_form = forms.RelationFilterForm

class RelationView(generic.ObjectView):
    queryset = models.Relation.objects.all()
from . import models
from . import filters
from . import forms
from . import tables

from django.conf import settings
from packaging import version
from netbox.views import generic
from tenancy.tables import TenantTable
from virtualization.models import VirtualMachine
from dcim.models import Device
from dcim.tables import DeviceTable
from virtualization.tables import VirtualMachineTable
from utilities.views import ViewTab, register_model_view



NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)


class ServiceListView(generic.ObjectListView):
    queryset = models.Service.objects.all()
    table = tables.ServiceTable
    filterset = filters.ServiceFilter
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
    table = tables.ServiceTable
    template_name = "nb_service/service_IC_view.html"
    tab = ViewTab(label='IC', badge=lambda obj: obj.config_itens.all().count(), hide_if_empty=True)

    def get_children(self, request, parent):
            childrens = parent.config_itens.all()
            return childrens

    def get_extra_context(self, request, instance):
        items_obj = instance.config_itens.all()
        data = {
                "config_items" : items_obj,
            }
        return data


@register_model_view(models.Service, name='Relationships')
class ServiceRelationView(generic.ObjectChildrenView):
    queryset = models.Service.objects.all()
    child_model = models.Relation
    table = tables.ServiceTable
    template_name = "nb_service/service_Relation_view.html"
    tab = ViewTab(label='Relationships', badge=lambda obj: obj.relationships.all().count(), hide_if_empty=True)

    def get_children(self, request, parent):
            childrens = parent.relationships.all()
            return childrens

    def get_extra_context(self, request, instance):
        relations = instance.relationships.all()
        data = {
                "relations_objs" : relations,
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
    model_form = forms.ServiceForm
    form  = forms.ServiceForm

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/obj_edit.html'
        else:
            self.template_name = 'nb_service/2.x/obj_edit.html'
        super().__init__(*args, *kwargs)

    def get_extra_context(self, request, instance):
        data = {}
        if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
            data['obj'] = instance

        return data

class ServiceImportView(generic.BulkImportView):
    queryset = models.Service.objects.all()
    model_form = forms.ServiceImportForm
    table = tables.ServiceTable

class ServiceBulkEditView(generic.BulkEditView):
    queryset = models.Service.objects.all()
    filterset = filters.ServiceFilter
    table = tables.ServiceTable
    form = forms.ServiceBulkEditForm

class ServiceBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Service.objects.all()
    table = tables.ServiceTable

if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
    from nb_service.views_3_x import ServiceDeleteView as ServiceDeleteView_3x
    from nb_service.views_3_x import ApplicationDeleteView as ApplicationDeleteView_3x
    ServiceDeleteView = ServiceDeleteView_3x
    ApplicationDeleteView = ApplicationDeleteView_3x
else:
    from nb_service.views_2_x import ServiceDeleteView as ServiceDeleteView_2x
    from nb_service.views_2_x import ApplicationDeleteView as ApplicationDeleteView_2x
    ServiceDeleteView = ServiceDeleteView_2x
    ApplicationDeleteView = ApplicationDeleteView_2x


class ICCreateView(generic.ObjectEditView):
    queryset = models.IC.objects.all()
    model_form = forms.ICForm
    form = forms.ICForm

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/IC/ic_edit.html'
        else:
            self.template_name = 'nb_service/2.x/IC/ic_edit.html'
        super().__init__(*args, *kwargs)
        self.alter_object = self.alter_obj

    def get_extra_context(self, request, instance):
        data = {}
        if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
            data['obj'] = instance

        return data

    def alter_obj(self, obj, request, url_args, url_kwargs):
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
    model_form = forms.RelationForm
    form = forms.RelationForm

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/obj_edit.html'
        else:
            self.template_name = 'nb_service/2.x/obj_edit.html'
        super().__init__(*args, *kwargs)

    def get_extra_context(self, request, instance):
        data = {}
        if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
            data['obj'] = instance

        return data

class PenTestEditView(generic.ObjectEditView):
    queryset = models.PenTest.objects.all()
    model_form = forms.PenTestForm
    form = forms.PenTestForm

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/obj_edit.html'
        else:
            self.template_name = 'nb_service/2.x/obj_edit.html'
        super().__init__(*args, *kwargs)

    def get_extra_context(self, request, instance):
        data = {}
        if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
            data['obj'] = instance

        return data

class PenTestDeleteView(generic.ObjectDeleteView):
    queryset = models.PenTest.objects.all()

class RelationDeleteView(generic.ObjectDeleteView):
    queryset = models.Relation.objects.all()

class ICDeleteView(generic.ObjectDeleteView):
    queryset = models.IC.objects.all()


class ApplicationListView(generic.ObjectListView):
    queryset = models.Application.objects.all()
    table = tables.ApplicationTable
    filterset = filters.ApplicationFilter
    filterset_form = forms.ApplicationFilterForm

class ApplicationView(generic.ObjectView):
    queryset = models.Application.objects.all()

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/Application/application_view.html'
        else:
            self.template_name = 'nb_service/2.x/Application/application_view.html'
        super().__init__(*args, *kwargs)

class ApplicationDevicesView(generic.ObjectView):
    queryset = models.Application.objects.all()

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/Application/application_objs.html'
        else:
            self.template_name = 'nb_service/2.x/Application/application_objs.html'
        super().__init__(*args, *kwargs)

    def get_extra_context(self, request, instance):
        objs = instance.devices.all()
        table = DeviceTable(objs)
        return {
            'Object_type': 'Devices',
            'active_tab' : 'device',
            'table': table,
        }

class ApplicationVMsView(generic.ObjectView):
    queryset = models.Application.objects.all()

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/Application/application_objs.html'
        else:
            self.template_name = 'nb_service/2.x/Application/application_objs.html'
        super().__init__(*args, *kwargs)


    def get_extra_context(self, request, instance):
        objs = instance.vm.all()
        table = VirtualMachineTable(objs)
        return {
            'Object_type': 'Virtual Machines',
            'active_tab' : 'virtual_machine',
            'table': table,
        }

class ApplicationEditView(generic.ObjectEditView):
    queryset = models.Application.objects.all()
    model_form = forms.ApplicationForm
    form = forms.ApplicationForm

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/obj_edit.html'
        else:
            self.template_name = 'nb_service/2.x/obj_edit.html'
        super().__init__(*args, *kwargs)

    def get_extra_context(self, request, instance):
        data = {}
        if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
            data['obj'] = instance

        return data


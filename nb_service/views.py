import logging
from . import models 
from . import filters
from . import forms 
from . import tables
from django.conf import settings
from packaging import version
from django.contrib.contenttypes.models import ContentType
from netbox.views import generic
from tenancy.tables import TenantTable
from virtualization.models import VirtualMachine
from dcim.models import Device
from dcim.tables import DeviceTable
from virtualization.tables import VirtualMachineTable
from utilities.utils import normalize_querydict 
from utilities.forms import restrict_form_fields, ConfirmationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.utils.html import escape
from django.contrib import messages
from django.utils.safestring import mark_safe
from utilities.permissions import get_permission_for_model



NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)


class ServiceListView(generic.ObjectListView):
    queryset = models.Service.objects.all()
    table = tables.ServiceTable
    filterset = filters.ServiceFilter
    filterset_form = forms.ServiceFilterForm
    action_buttons = ("add")
    actions = action_buttons

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/custom_list.html'
        else:
            self.template_name = 'nb_service/2.x/custom_list.html'        
        super().__init__(*args, *kwargs)

    def get_extra_context(self, request):
        data = {}
        model = self.queryset.model
        permissions = {}
        for action in ('add', 'change', 'delete', 'view'):
            perm_name = get_permission_for_model(model, action)
            permissions[action] = request.user.has_perm(perm_name)

        content_type = ContentType.objects.get_for_model(model)
        if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
            data['content_type'] = content_type
            data['permissions'] = permissions
            data['action_buttons'] = self.action_buttons

        return data

class ServiceView(generic.ObjectView):
    queryset = models.Service.objects.all()

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/service/service_view.html'
        else:
            self.template_name = 'nb_service/2.x/service/service_view.html'     
        super().__init__(*args, *kwargs)

    def get_extra_context(self, request, instance):
        items_obj = instance.config_itens.all()
        objetos_table = tables.ICTable(items_obj)
        tenants_table = TenantTable(instance.clients.all())
        vuln_table = tables.VulnTable(instance.pentest_reports.all())
        model = self.queryset.model
        permissions = {}
        for action in ('add', 'change', 'delete', 'view'):
            perm_name = get_permission_for_model(model, action)
            permissions[action] = request.user.has_perm(perm_name)

        data = {
                "tenant_table" : tenants_table,
                "permissions": permissions,
                "vuln_table" : vuln_table,
                "objetos_table": objetos_table,
                "config_items" : items_obj,
            }
        return data


class ServiceDiagramView(generic.ObjectView):
    queryset = models.Service.objects.all()

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/service/service_diagram_view.html'
        else:
            self.template_name = 'nb_service/2.x/service/service_diagram_view.html'  
        super().__init__(*args, *kwargs)

class ServiceICView(generic.ObjectView):
    queryset = models.Service.objects.all()

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/service/service_IC_view.html'
        else:
            self.template_name = 'nb_service/2.x/service/service_IC_view.html'
        super().__init__(*args, *kwargs)

    def get_extra_context(self, request, instance):
        items_obj = instance.config_itens.all()
        data = {
                "config_items" : items_obj,
            }
        return data

class ServiceRelationView(generic.ObjectView):
    queryset = models.Service.objects.all()

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/service/service_Relation_view.html'
        else:
            self.template_name = 'nb_service/2.x/service/service_Relation_view.html'
        super().__init__(*args, *kwargs)

    def get_extra_context(self, request, instance):
        relations = instance.relationships.all()
        data = {
                "relations_objs" : relations,
            }
        return data


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
    action_buttons = ("add")

    def __init__(self, *args, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.0") :
            self.template_name = 'nb_service/3.x/custom_list.html'
        else:
            self.template_name = 'nb_service/2.x/custom_list.html'
        super().__init__(*args, *kwargs)

    def get_extra_context(self, request):
        data = {}
        model = self.queryset.model
        permissions = {}
        for action in ('add', 'change', 'delete', 'view'):
            perm_name = get_permission_for_model(model, action)
            permissions[action] = request.user.has_perm(perm_name)

        content_type = ContentType.objects.get_for_model(model)
        if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
            data['content_type'] = content_type
            data['permissions'] = permissions
            data['action_buttons'] = self.action_buttons

        return data

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
    

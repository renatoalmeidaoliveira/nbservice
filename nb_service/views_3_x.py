from . import models 
from netbox.views import generic
from django.conf import settings
from packaging import version

from utilities.htmx import is_htmx
from utilities.forms import ConfirmationForm
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)
if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
    from netbox.views.generic import ObjectChangeLogView
else:
    from extras.views import ObjectChangeLogView



class ServiceDeleteView(generic.ObjectDeleteView):
    queryset = models.Service.objects.all()

    def get(self, request, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
            obj = self.get_object(**kwargs)
        else:
            obj = self.get_object(kwargs)
        
        form = ConfirmationForm(initial=request.GET)

        # If this is an HTMX request, return only the rendered deletion form as modal content
        if is_htmx(request):
            viewname = f'plugins:{self.queryset.model._meta.app_label}:{self.queryset.model._meta.model_name}_delete'
            form_url = reverse(viewname, kwargs={'pk': obj.pk})
            return render(request, 'htmx/delete_form.html', {
                'object': obj,
                'object_type': self.queryset.model._meta.verbose_name,
                'form': form,
                'form_url': form_url,
            })

        return render(request, self.template_name, {
            'object': obj,
            'object_type': self.queryset.model._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, obj),
        })


class ApplicationDeleteView(generic.ObjectDeleteView):
    queryset = models.Application.objects.all()

    def get(self, request, **kwargs):
        if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
            obj = self.get_object(**kwargs)
        else:
            obj = self.get_object(kwargs)
        
        form = ConfirmationForm(initial=request.GET)

        # If this is an HTMX request, return only the rendered deletion form as modal content
        if is_htmx(request):
            viewname = f'plugins:{self.queryset.model._meta.app_label}:{self.queryset.model._meta.model_name}_delete'
            form_url = reverse(viewname, kwargs={'pk': obj.pk})
            return render(request, 'htmx/delete_form.html', {
                'object': obj,
                'object_type': self.queryset.model._meta.verbose_name,
                'form': form,
                'form_url': form_url,
            })

        return render(request, self.template_name, {
            'object': obj,
            'object_type': self.queryset.model._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, obj),
        })


class ServiceChangeLogView(ObjectChangeLogView):
    base_template = 'nb_service/3.x/service/service_ChangeLog_view.html'

class ApplicationChangeLogView(ObjectChangeLogView):
    base_template = 'nb_service/3.x/Application/application_ChangeLog.html'
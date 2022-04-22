from . import models 
from netbox.views import generic

class ServiceDeleteView(generic.ObjectDeleteView):
    queryset = models.Service.objects.all()

class ApplicationDeleteView(generic.ObjectDeleteView):
    queryset = models.Application.objects.all()

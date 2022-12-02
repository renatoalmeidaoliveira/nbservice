"""
from rest_framework import routers
from .views import MyModel1ViewSet


router = routers.DefaultRouter()
router.register('', MyModel1ViewSet)
urlpatterns = router.urls

"""
from django.conf import settings
from packaging import version

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)
if NETBOX_CURRENT_VERSION >= version.parse("3.3") :
    from netbox.api.routers import NetBoxRouter
elif NETBOX_CURRENT_VERSION >= version.parse("3.2") :
    from netbox.api import NetBoxRouter
else:
    from netbox.api import OrderedDefaultRouter as NetBoxRouter

from . import views

router = NetBoxRouter()

router.register('ic', views.ICViewSet)
router.register('service', views.ServiceViewSet)
router.register('application', views.ApplicationViewSet)

urlpatterns = router.urls
app_name = 'nb_service-api'
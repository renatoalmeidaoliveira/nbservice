from django.urls import path, include
from utilities.urls import get_model_urls

from django.conf import settings
from packaging import version


NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)


from . import views
from . import models

app_name = 'nb_service'

urlpatterns = [
    path("service/", views.ServiceListView.as_view(), name="service_list"),
    path('service/<int:pk>/', include(get_model_urls(app_name, 'service'))),
    path("service/<int:pk>/", views.ServiceView.as_view(), name="service"),
    path('service/add/', views.ServiceEditView.as_view(), name='service_add'),
    path('service/<int:pk>/edit/', views.ServiceEditView.as_view(), name='service_edit'),
    path('service/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),
    path('service/import/', views.ServiceImportView.as_view(), name='service_import'),
    path('service/edit/', views.ServiceBulkEditView.as_view(), name='service_bulk_edit'),
    path('service/delete/', views.ServiceBulkDeleteView.as_view(), name='service_bulk_delete'),

    path('relation/add', views.RelationEditView.as_view(), name='relation_add'),
    path('relation/<int:pk>/edit/', views.RelationEditView.as_view(), name='relation_edit'),
    path('relation/<int:pk>/delete/', views.RelationDeleteView.as_view(), name='relation_delete'),

    path('ic/add', views.ICCreateView.as_view(), name='IC_add'),
    path('ic/<int:pk>/delete/', views.ICDeleteView.as_view(), name='IC_delete'),

    path('pentest/add', views.PenTestEditView.as_view(), name='pentest_add'),
    path('pentest/<int:pk>/edit/', views.PenTestEditView.as_view(), name='pentest_edit'),
    path('pentest/<int:pk>/delete/', views.PenTestDeleteView.as_view(), name='pentest_delete'),
    path('pentest/<int:pk>/', include(get_model_urls(app_name, 'pentest'))),

    path('application/', views.ApplicationListView.as_view(), name='application_list'),
    path("application/<int:pk>/", views.ApplicationView.as_view(), name="application"),
    path('application/add', views.ApplicationEditView.as_view(), name='application_add'),
    path('application/<int:pk>/edit/', views.ApplicationEditView.as_view(), name='application_edit'),
    path('application/<int:pk>/delete/', views.ApplicationDeleteView.as_view(), name='application_delete'),
    path('application/import/', views.ApplicationImportView.as_view(), name='application_import'),
    path('application/edit/', views.ApplicationBulkEditView.as_view(), name='application_bulk_edit'),
    path('application/delete/', views.ApplicationBulkDeleteView.as_view(), name='application_bulk_delete'),
    path("application/<int:pk>/devices", views.ApplicationDevicesView.as_view(), name="application_devices"),
    path("application/<int:pk>/vms", views.ApplicationVMsView.as_view(), name="application_vms"),
]

urlpatterns_3_2 = []
urlpatterns_2_x = []
NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)
if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
    from nb_service.views_3_x import   ApplicationChangeLogView
    urlpatterns_3_2 = [
#        path("service/<int:pk>/changelog", ServiceChangeLogView.as_view(), name="service_changelog", kwargs={'model': models.Service}),
        path("application/<int:pk>/changelog", ApplicationChangeLogView.as_view(), name="application_changelog", kwargs={'model': models.Application}),
    ]
else:
    from extras.views import ObjectChangeLogView
    urlpatterns_2_x = [
#        path("service/<int:pk>/changelog", ObjectChangeLogView.as_view(), name="service_changelog", kwargs={'model': models.Service}),
        path("application/<int:pk>/changelog", ObjectChangeLogView.as_view(), name="application_changelog", kwargs={'model': models.Application}),
    ]

urlpatterns.extend(urlpatterns_3_2)
urlpatterns.extend(urlpatterns_2_x)

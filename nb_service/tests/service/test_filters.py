from django.test import TestCase

from tenancy.models import Tenant
from utilities.testing import ChangeLoggedFilterSetTests

from nb_service.models import Service
from nb_service.filters import ServiceFilter


class ServiceFilterTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = Service.objects.all()
    filterset = ServiceFilter

    @classmethod
    def setUpTestData(cls):
        cls.tenants = (
            Tenant(name="Tenant 1", slug="tenant-1"),
            Tenant(name="Tenant 2", slug="tenant-2"),
            Tenant(name="Tenant 3", slug="tenant-3"),
        )
        Tenant.objects.bulk_create(cls.tenants)

        cls.services = (
            Service(name="Service 1"),
            Service(name="Service 2"),
            Service(name="Service 3"),
        )
        Service.objects.bulk_create(cls.services)

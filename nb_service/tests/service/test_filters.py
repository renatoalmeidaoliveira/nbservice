from django.test import TestCase

from tenancy.models import Tenant
from utilities.testing import ChangeLoggedFilterSetTests

from nb_service.models import Service
from nb_service.filtersets import ServiceFilterSet


class ServiceFilterTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = Service.objects.all()
    filterset = ServiceFilterSet
    
    @classmethod
    def setUpTestData(cls):
        cls.ignore_fields = ( "clients", )
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

        cls.services[0].clients.set([cls.tenants[0].pk, cls.tenants[1].pk])
        cls.services[1].clients.set([cls.tenants[1].pk, cls.tenants[2].pk])
        cls.services[2].clients.set([cls.tenants[0].pk])

    def test_name(self):
        params = {'name': ['Service 1', 'Service 2']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_clients(self):
        params = {"clients": [self.tenants[0].name, self.tenants[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"clients": [self.tenants[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"clients_id": [self.tenants[0].pk, self.tenants[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"clients_id": [self.tenants[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

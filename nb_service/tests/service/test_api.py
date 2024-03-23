from utilities.testing import APIViewTestCases, create_tags
from tenancy.models import Tenant

from nb_service.tests.custom import APITestCase
from nb_service.models import Service


class ServiceAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = Service

    @classmethod
    def setUpTestData(cls):
        tags = create_tags("Alpha", "Bravo", "Charlie")

        services = (
            Service(name="Test Service 1", comments="Test Comment 1", backup_profile='Test Profile 1'),
            Service(name="Test Service 2", comments="Test Comment 2", backup_profile='Test Profile 2'),
            Service(name="Test Service 3", comments="Test Comment 3", backup_profile='Test Profile 3'),
        )
        Service.objects.bulk_create(services)

        tenants = (
            Tenant(name="Tenant 1", slug="tenant-1"),
            Tenant(name="Tenant 2", slug="tenant-2"),
            Tenant(name="Tenant 3", slug="tenant-3"),
        )
        Tenant.objects.bulk_create(tenants)

        cls.create_data = [
            {"name": "Test Service 4", "comments": "Test Comment 4", "backup_profile": "Test Profile 4", "clients": [tenants[0].pk, tenants[1].pk] },
            {"name": "Test Service 5", "comments": "Test Comment 5", "backup_profile": "Test Profile 5", "clients": [tenants[1].pk, tenants[2].pk] },
            {"name": "Test Service 6", "comments": "Test Comment 6", "backup_profile": "Test Profile 6", "clients": [tenants[2].pk] },
        ]

        cls.bulk_update_data = {
            "clients": [tenants[1].pk]
        }

        cls.brief_fields = ['backup_profile', 'clients', 'comments', 'display', 'id', 'name']

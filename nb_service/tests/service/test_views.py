from utilities.testing import ViewTestCases
from utilities.testing import create_tags

from nb_service.tests.custom import ModelViewTestCase
from nb_service.models import Service


class ServiceViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = Service

    @classmethod
    def setUpTestData(cls):
        services = (
            Service(name="Test Service 1", comments="Test Comment 1", backup_profile='Test Profile 1'),
            Service(name="Test Service 2", comments="Test Comment 2", backup_profile='Test Profile 1'),
            Service(name="Test Service 3", comments="Test Comment 3", backup_profile='Test Profile 1'),
        )
        Service.objects.bulk_create(services)

        cls.form_data = {
            "name": "Test Service 4",
        }

        cls.csv_data = (
            "name",
            "Service 4",
            "Service 5",
            "Service 6",
        )

        cls.csv_update_data = (
            "id,name,backup_profile",
            f"{services[0].pk},New Test Service 1,Test Profile 1",
            f"{services[1].pk},New Test Service 2,Test Profile 2",
        )

    maxDiff = None

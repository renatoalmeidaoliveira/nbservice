from utilities.testing import ViewTestCases, create_tags
from virtualization.models import VirtualMachine, ClusterType, Cluster
from dcim.models import Device, DeviceRole, Manufacturer, DeviceType, Site
from ipam.choices import ServiceProtocolChoices

from nb_service.tests.custom import ModelViewTestCase
from nb_service.models import Application


class ApplicationViewTestCase(
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
    model = Application

    @classmethod
    def setUpTestData(cls):
        site = Site.objects.create(name="Site 1")
        manufacturer = Manufacturer.objects.create(name='Manufacturer 1')
        device_type = DeviceType.objects.create(manufacturer=manufacturer)
        device_role = DeviceRole.objects.create(name='Device Role 1')

        devices = (
            Device(name='Device 1', device_type=device_type, role=device_role, site=site),
            Device(name='Device 2', device_type=device_type, role=device_role, site=site),
            Device(name='Device 3', device_type=device_type, role=device_role, site=site),
        )
        Device.objects.bulk_create(devices)

        clustertype = ClusterType.objects.create(name='Cluster Type 1')
        cluster = Cluster.objects.create(name='Cluster 1', type=clustertype)

        virtual_machines = (
            VirtualMachine(name="Virtual Machine 1", cluster=cluster),
            VirtualMachine(name="Virtual Machine 2", cluster=cluster),
            VirtualMachine(name="Virtual Machine 3", cluster=cluster),
        )
        VirtualMachine.objects.bulk_create(virtual_machines)

        applications = (
            Application(name="SSH", protocol=ServiceProtocolChoices.PROTOCOL_TCP, ports=[22], version="2.0"),
            Application(name="Telnet", protocol=ServiceProtocolChoices.PROTOCOL_TCP, ports=[23], version="42"),
            Application(name="HTTPS", protocol=ServiceProtocolChoices.PROTOCOL_TCP, ports=[443, 8443], version="23"),
            Application(name="SNMP", protocol=ServiceProtocolChoices.PROTOCOL_UDP, ports=[161], version="3"),
        )
        Application.objects.bulk_create(applications)

        cls.form_data = {
            "name": "Test Application 4", "protocol": ServiceProtocolChoices.PROTOCOL_TCP, "ports": "42", "version": "1.0"
        }

        cls.csv_data = (
            "name,protocol,ports,version,devices,vm",
            f"Application 4,tcp,43,1.0,\"{devices[0].name}\",",
            f"Application 5,tcp,44,2.0,{devices[2].name},{virtual_machines[1].name}",
            f"Application 6,tcp,45,2.0,,{virtual_machines[1].name}",
        )

        cls.csv_update_data = (
            "id,name",
            f"{applications[0].pk},New Test Application 1",
            f"{applications[1].pk},New Test Application 2",
        )

    maxDiff = None

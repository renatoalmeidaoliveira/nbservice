from utilities.testing import APIViewTestCases, create_tags

from virtualization.models import VirtualMachine, ClusterType, Cluster
from dcim.models import Device, DeviceRole, Manufacturer, DeviceType, Site
from ipam.choices import ServiceProtocolChoices

from nb_service.tests.custom import APITestCase
from nb_service.models import Application


class ApplicationAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = Application

    @classmethod
    def setUpTestData(cls):
        tags = create_tags("Alpha", "Bravo", "Charlie")

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
        )
        Application.objects.bulk_create(applications)

        cls.create_data = [
            {"name": "SMTP", "protocol": ServiceProtocolChoices.PROTOCOL_TCP, "ports": [25, 587], "version": "1.0", "devices": [devices[2].pk]},
            {"name": "SNMP", "protocol": ServiceProtocolChoices.PROTOCOL_UDP, "ports": [161], "version": "3", "devices": [devices[1].pk, devices[2].pk]},
            {"name": "SNMP Trap", "protocol": ServiceProtocolChoices.PROTOCOL_UDP, "ports": [162], "version": "3", "vm": [virtual_machines[0].pk, virtual_machines[1].pk]},
        ]

        cls.bulk_update_data = {
            "protocol": ServiceProtocolChoices.PROTOCOL_SCTP,
            "vm": [virtual_machines[0].pk, virtual_machines[1].pk, virtual_machines[2].pk],
            "devices": [devices[0].pk, devices[1].pk],
        }

        cls.brief_fields = ['devices', 'display', 'id', 'name', 'ports', 'protocol', 'version', 'vm']

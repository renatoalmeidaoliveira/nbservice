from django.test import TestCase

from utilities.testing import ChangeLoggedFilterSetTests
from virtualization.models import VirtualMachine, ClusterType, Cluster
from dcim.models import Device, DeviceRole, Manufacturer, DeviceType, Site
from ipam.choices import ServiceProtocolChoices

from nb_service.models import Application
from nb_service.filtersets import ApplicationFilterSet


class ApplicationFilterTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = Application.objects.all()
    filterset = ApplicationFilterSet


    @classmethod
    def setUpTestData(cls):
        cls.ignore_fields = [ "vm", "devices" ]
        site = Site.objects.create(name="Site 1")
        manufacturer = Manufacturer.objects.create(name='Manufacturer 1')
        device_type = DeviceType.objects.create(manufacturer=manufacturer)
        device_role = DeviceRole.objects.create(name='Device Role 1')

        cls.devices = (
            Device(name='Device 1', device_type=device_type, role=device_role, site=site),
            Device(name='Device 2', device_type=device_type, role=device_role, site=site),
            Device(name='Device 3', device_type=device_type, role=device_role, site=site),
        )
        Device.objects.bulk_create(cls.devices)

        clustertype = ClusterType.objects.create(name='Cluster Type 1')
        cluster = Cluster.objects.create(name='Cluster 1', type=clustertype)

        cls.virtual_machines = (
            VirtualMachine(name="Virtual Machine 1", cluster=cluster),
            VirtualMachine(name="Virtual Machine 2", cluster=cluster),
            VirtualMachine(name="Virtual Machine 3", cluster=cluster),
        )
        VirtualMachine.objects.bulk_create(cls.virtual_machines)

        applications = (
            Application(name="SSH", protocol=ServiceProtocolChoices.PROTOCOL_TCP, ports=[22], version="2.0"),
            Application(name="Telnet", protocol=ServiceProtocolChoices.PROTOCOL_TCP, ports=[23], version="42"),
            Application(name="HTTPS", protocol=ServiceProtocolChoices.PROTOCOL_TCP, ports=[443, 8443], version="23"),
            Application(name="SNMP", protocol=ServiceProtocolChoices.PROTOCOL_UDP, ports=[161], version="3"),
        )
        Application.objects.bulk_create(applications)

        applications[0].devices.set([cls.devices[0], cls.devices[1]])
        applications[1].devices.set([cls.devices[1], cls.devices[2]])

        applications[0].vm.set([cls.virtual_machines[0], cls.virtual_machines[1]])
        applications[1].vm.set([cls.virtual_machines[1], cls.virtual_machines[2]])

    def test_name(self):
        params = {'name': ['SSH', 'HTTPS']}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_protocol(self):
        params = {'protocol': ServiceProtocolChoices.PROTOCOL_TCP}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_devices(self):
        params = {'devices': [self.devices[0].name, self.devices[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'devices': [self.devices[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'devices_id': [self.devices[0].pk, self.devices[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'devices_id': [self.devices[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_virtual_machines(self):
        params = {'virtual_machines': [self.virtual_machines[0].name, self.virtual_machines[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'virtual_machines': [self.virtual_machines[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {'virtual_machines_id': [self.virtual_machines[0].pk, self.virtual_machines[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {'virtual_machines_id': [self.virtual_machines[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

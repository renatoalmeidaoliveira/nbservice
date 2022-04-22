from django.conf import settings
from packaging import version
import django_tables2 as tables


NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)
if NETBOX_CURRENT_VERSION >= version.parse("3.2") :
    from netbox.tables import NetBoxTable, ToggleColumn
else: 
    from utilities.tables import BaseTable as NetBoxTable
    from utilities.tables import ToggleColumn

from . import models


class ServiceTable(NetBoxTable):

    name = tables.LinkColumn(verbose_name="Service")
    id = ToggleColumn()
    backup_profile = tables.Column(verbose_name="Backup Profile")

    
    class Meta(NetBoxTable.Meta):
        model = models.Service
        fields = (
            "name",
            "backup_profile",
        )

class ICTable(NetBoxTable):
    id = ToggleColumn()
    assigned_object = tables.LinkColumn(verbose_name="CI")
    obj_type = tables.Column(verbose_name="Type")
    
    class Meta(NetBoxTable.Meta):
        model = models.IC        
        fields = (
            "id",
            "assigned_object",
            "obj_type"
        )

class VulnTable(NetBoxTable):
    id = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = models.PenTest        
        fields = (
            "id",
            "ticket",
            "date",
            "status",
        )

class ApplicationTable(NetBoxTable):

    name = tables.LinkColumn(verbose_name="Application")
    id = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = models.Application
        fields = [
            "name",
            "version",
            "protocol",
            "ports",
         ]
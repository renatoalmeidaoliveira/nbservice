from django.conf import settings
from packaging import version
import django_tables2 as tables


from netbox.tables import NetBoxTable, ToggleColumn , columns


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
    actions = columns.ActionsColumn(actions=("delete",))
    
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
        
class RelationTable(NetBoxTable):
    id = ToggleColumn()

    service = tables.LinkColumn(verbose_name="Service")
    source = tables.LinkColumn(verbose_name="Source")
    destination = tables.LinkColumn(verbose_name="Destination")
    
    class Meta(NetBoxTable.Meta):
        model = models.Relation
        fields = [
            "service",
            "source",
            "source_shape",
            "destination",
            "destination_shape",
            "connector_shape",
            "link_text",            
        ]
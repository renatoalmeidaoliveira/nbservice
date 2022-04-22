from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from dcim.models import Device
from virtualization.models import VirtualMachine

from . import models

def handle_IC_assigned_Object_delete(sender,instance,*args,**kwargs):
    related_ics = models.IC.objects.filter(
        assigned_object_type=ContentType.objects.get_for_model(instance),
         assigned_object_id=instance.id)
    for ic in related_ics:
        ic.delete()


device_delete = receiver(post_delete, sender=Device)(handle_IC_assigned_Object_delete)
vm_delete = receiver(post_delete, sender=VirtualMachine)(handle_IC_assigned_Object_delete)
app_delete = receiver(post_delete, sender=models.Application)(handle_IC_assigned_Object_delete)

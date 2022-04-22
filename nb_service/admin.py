from django.contrib import admin
from . import models



@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = ("name",
              "clients",
              "comments",
              "backup_profile",
    )

@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    fields = ("name",
              "protocol",
              "ports",
              "version",
              "devices",
              "vm",
    )

@admin.register(models.IC)
class ICAdmin(admin.ModelAdmin):
    fields = ("service",
              "assigned_object_type",
              "assigned_object_id",)

@admin.register(models.Relation)
class RelationAdmin(admin.ModelAdmin):
    fields = ("service",
              "source",
              "source_shape",
              "destination",
              "destination_shape",
              "connector_shape",
    )

@admin.register(models.PenTest)
class PenTestAdmin(admin.ModelAdmin):
    fields = ("service",
              "status",
              "date",
              "ticket",
              "report_link")


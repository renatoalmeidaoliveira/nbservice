#

# Django imports
from django.conf import settings
from packaging import version
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError

from taggit.managers import TaggableManager


# Netbox imports
from utilities.querysets import RestrictedQuerySet
from netbox.models import NetBoxModel


from dcim.models import Device
from virtualization.models import VirtualMachine
from tenancy.models import Tenant
from ipam.models import Service
from ipam.choices import ServiceProtocolChoices



# module imports
from . import choices

SERVICE_PORT_MIN = 1
SERVICE_PORT_MAX = 65535
SHAPE_NAMES = [
    "Round Edges",
    "Stadium Shaped",
    "Subroutine Shape",
    "Cylindrical Shape",
    "Circle Shape",
    "asymmetric shape",
    "rhombus",
    "Hexagon",
    "Parallelogram",
    "Trapezoid",
]


class Service(NetBoxModel):
    name = models.CharField("Name", max_length=100)
    clients = models.ManyToManyField(
        Tenant, related_name="itsm_services", verbose_name="Clients"
    )
    comments = models.TextField(blank=True)
    backup_profile = models.CharField("Backup Profile", max_length=100, blank=True, null=True)

    tags = TaggableManager(
        through="extras.TaggedItem",
        related_name="itsm_service_set",
    )


    @property
    def diagram(self):
        graph = "graph TB\n"
        open_shape = [
            "(",
            "([",
            "[[",
            "[(",
            "((",
            ">",
            "{",
            "{{",
            "[/",
            "[/",
        ]

        close_shape = [
            ")",
            "])",
            "]]",
            ")]",
            "))",
            "]",
            "}",
            "}}",
            "/]",
            "\]",
        ]
        arrow_shape = ["-->", "---", "-.->", "-.-"]
        nodes = {}
        for ic in self.config_itens.all():
            node = ic.name.replace(" ", "_")
            graph += f"{node}\n"
            if node not in nodes:
                nodes[node] = ic.get_absolute_url()
        for rel in self.relationships.all():
            src_node = rel.source.name.replace(" ", "_")
            dest_node = rel.destination.name.replace(" ", "_")
            if src_node not in nodes:
                nodes[src_node] = rel.source.get_absolute_url()
            if dest_node not in nodes:
                nodes[dest_node] = rel.destination.get_absolute_url()

            graph += (
                f"    {src_node}{open_shape[rel.source_shape -1]}"
                + f"{rel.source.name}{close_shape[rel.source_shape -1]}"
                + f" {arrow_shape[rel.connector_shape -1]} "
            )
            if rel.link_text != "":
                graph += f"| {rel.link_text} |"
            graph += (
                f"{dest_node}{open_shape[rel.destination_shape -1]}"
                + f"{rel.destination.name}{close_shape[rel.destination_shape -1]}\n"
            )
        for node in nodes:
            graph += f'click {node} "{nodes[node]}"\n'
        return graph

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("plugins:nb_service:service", kwargs={"pk": self.pk})


class Application(NetBoxModel):
    name = models.CharField("Name", max_length=100)
    protocol = models.CharField(
        "Protocol", max_length=50, choices=ServiceProtocolChoices, null=False, blank=False
    )
    ports = ArrayField(
        base_field=models.PositiveIntegerField(
            validators=[
                MinValueValidator(SERVICE_PORT_MIN),
                MaxValueValidator(SERVICE_PORT_MAX),
            ]
        ),
        verbose_name="Port numbers",
    )
    version = models.CharField("Version", max_length=100)
    devices = models.ManyToManyField(
        Device,
        related_name="uses_apps",
        verbose_name="Devices",
        blank=True,
    )
    vm = models.ManyToManyField(
        VirtualMachine,
        related_name="uses_apps",
        verbose_name="Virtual Machines",
        blank=True,
    )
    tags = TaggableManager(
        through="extras.TaggedItem",
        related_name="itsm_application_set",
    )

    def get_absolute_url(self):
        return reverse("plugins:nb_service:application", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.name} - {self.version}"


class IC(NetBoxModel):
    service = models.ForeignKey(
        to=Service, on_delete=models.CASCADE, related_name="config_itens"
    )

    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=choices.OBJETO_ASSIGNMENT_MODELS,
        on_delete=models.CASCADE,
        related_name="+",
        blank=True,
        null=True,
    )
    assigned_object_id = models.PositiveIntegerField(blank=True, null=True)
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type",
        fk_field="assigned_object_id",
    )

    @property
    def obj_type(self):
        return self.assigned_object_type.name

    @property
    def name(self):
        if self.assigned_object is not None:
            return self.assigned_object.name
        else:
            return ""

    def __str__(self):
        return str(self.assigned_object)

    def get_absolute_url(self):
        url = reverse("plugins:nb_service:service", kwargs={"pk": self.service.pk})
        try:
            url = self.assigned_object.get_absolute_url()
        except Exception as e:
            pass
        return url

    def validate_unique(self, exclude=None):
        ICs = self.service.config_itens.filter(
            assigned_object_type=self.assigned_object_type
        )
        candidate_obj = self.assigned_object
        for obj in ICs:
            if candidate_obj == obj.assigned_object:
                raise ValidationError(
                    (f"{self.assigned_object} already in {self.service}")
                )

        super().validate_unique(exclude=exclude)

    class Meta:
        unique_together = [
            ["service", "assigned_object_type", "assigned_object_id"],
        ]


class Relation(NetBoxModel):
    service = models.ForeignKey(
        verbose_name="Service",
        to=Service,
        on_delete=models.CASCADE,
        related_name="relationships",
    )
    source = models.ForeignKey(
        verbose_name="Source", to=IC, on_delete=models.CASCADE, related_name="+"
    )
    source_shape = models.IntegerField("Source Shape", choices=choices.ShapeChoices)
    destination = models.ForeignKey(
        verbose_name="Destination", to=IC, on_delete=models.CASCADE, related_name="+"
    )
    destination_shape = models.IntegerField(
        "Destination Shape", choices=choices.ShapeChoices
    )
    connector_shape = models.IntegerField(
        "Connector Shape", choices=choices.ConnectorChoices
    )

    link_text = models.CharField("Link Text", max_length=100)

    @property
    def source_shape_name(self):
        return SHAPE_NAMES[self.source_shape - 1]

    @property
    def destiny_shape_name(self):
        return SHAPE_NAMES[self.destination_shape - 1]

    @property
    def connector(self):
        arrow_shape = ["-->", "---", "-.->", "-.-"]
        return f"{arrow_shape[self.connector_shape -1]}"

    def get_absolute_url(self):
        return reverse("plugins:nb_service:relation", kwargs={"pk": self.pk})
    
    @property
    def diagram(self):
        graph = "graph TB\n"
        open_shape = [
            "(",
            "([",
            "[[",
            "[(",
            "((",
            ">",
            "{",
            "{{",
            "[/",
            "[/",
        ]

        close_shape = [
            ")",
            "])",
            "]]",
            ")]",
            "))",
            "]",
            "}",
            "}}",
            "/]",
            "\]",
        ]
        arrow_shape = ["-->", "---", "-.->", "-.-"]
        nodes = {}
        relations = [ self ]
        for rel in relations:
            src_node = rel.source.name.replace(" ", "_")
            dest_node = rel.destination.name.replace(" ", "_")
            if src_node not in nodes:
                nodes[src_node] = rel.source.get_absolute_url()
            if dest_node not in nodes:
                nodes[dest_node] = rel.destination.get_absolute_url()

            graph += (
                f"    {src_node}{open_shape[rel.source_shape -1]}"
                + f"{rel.source.name}{close_shape[rel.source_shape -1]}"
                + f" {arrow_shape[rel.connector_shape -1]} "
            )
            if rel.link_text != "":
                graph += f"| {rel.link_text} |"
            graph += (
                f"{dest_node}{open_shape[rel.destination_shape -1]}"
                + f"{rel.destination.name}{close_shape[rel.destination_shape -1]}\n"
            )
        for node in nodes:
            graph += f'click {node} "{nodes[node]}"\n'
        return graph
    
    def __str__(self) -> str:
        arrow_shape = ["-->", "---", "-.->", "-.-"]
        src_node = self.source.name.replace(" ", "_")
        dest_node = self.destination.name.replace(" ", "_")

        return f"{src_node} {arrow_shape[self.connector_shape -1]} {dest_node}"


class PenTest(NetBoxModel):
    service = models.ForeignKey(
        to=Service, on_delete=models.CASCADE, related_name="pentest_reports"
    )
    comments = models.TextField(blank=True)
    status = models.IntegerField(
        "State",
        choices=choices.PenTestChoices,
        blank=True,
        help_text="Approved or Reproved",
    )
    date = models.DateField("Execution Date", blank=True)
    ticket = models.CharField("Ticket", max_length=100)
    report_link = models.CharField("Report link", max_length=100)

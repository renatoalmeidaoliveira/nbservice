from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from netbox.models.features import *
from utilities.querysets import RestrictedQuerySet


class NetBoxFeatureSet(
    BookmarksMixin,
    ChangeLoggingMixin,
    CloningMixin,
    CustomFieldsMixin,
    CustomLinksMixin,
    CustomValidationMixin,
    ExportTemplatesMixin,
    JournalingMixin,
    EventRulesMixin,
):
    class Meta:
        abstract = True

    @property
    def docs_url(self):
        return f"{settings.STATIC_URL}docs/models/{self._meta.app_label}/{self._meta.model_name}/"


class NetBoxModel(NetBoxFeatureSet, models.Model):
    """
    Base model for most object types. Suitable for use by plugins.
    """

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        abstract = True

    def clean(self):
        """
        Validate the model for GenericForeignKey fields to ensure that the content type and object ID exist.
        """
        super().clean()

        for field in self._meta.get_fields():
            if isinstance(field, GenericForeignKey):
                ct_value = getattr(self, field.ct_field, None)
                fk_value = getattr(self, field.fk_field, None)

                if ct_value is None and fk_value is not None:
                    raise ValidationError(
                        {
                            field.ct_field: "This field cannot be null.",
                        }
                    )
                if fk_value is None and ct_value is not None:
                    raise ValidationError(
                        {
                            field.fk_field: "This field cannot be null.",
                        }
                    )

                if ct_value and fk_value:
                    klass = getattr(self, field.ct_field).model_class()
                    try:
                        obj = klass.objects.get(pk=fk_value)
                    except ObjectDoesNotExist:
                        raise ValidationError(
                            {
                                field.fk_field: f"Related object not found using the provided value: {fk_value}."
                            }
                        )

                    # update the GFK field value
                    setattr(self, field.name, obj)

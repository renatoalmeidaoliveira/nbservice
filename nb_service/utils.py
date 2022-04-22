import django_filters

from utilities.forms import widgets
from django.forms import BoundField
from django import forms
from django.urls import reverse
from django.conf import settings

class DynamicModelChoiceMixin:
    """
    :param display_field: The name of the attribute of an API response object to display in the selection list
    :param query_params: A dictionary of additional key/value pairs to attach to the API request
    :param initial_params: A dictionary of child field references to use for selecting a parent field's initial value
    :param null_option: The string used to represent a null selection (if any)
    :param disabled_indicator: The name of the field which, if populated, will disable selection of the
        choice (optional)
    :param brief_mode: Use the "brief" format (?brief=true) when making API requests (default)
    """
    filter = django_filters.ModelChoiceFilter
    widget = widgets.APISelect

    def __init__(self, display_field='name', query_params=None, initial_params=None, null_option=None,
                 disabled_indicator=None, brief_mode=True, *args, **kwargs):
        self.display_field = display_field
        self.query_params = query_params or {}
        self.initial_params = initial_params or {}
        self.null_option = null_option
        self.disabled_indicator = disabled_indicator
        self.brief_mode = brief_mode

        # to_field_name is set by ModelChoiceField.__init__(), but we need to set it early for reference
        # by widget_attrs()
        self.to_field_name = kwargs.get('to_field_name')

        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = {
            'display-field': self.display_field,
        }

        # Set value-field attribute if the field specifies to_field_name
        if self.to_field_name:
            attrs['value-field'] = self.to_field_name

        # Set the string used to represent a null option
        if self.null_option is not None:
            attrs['data-null-option'] = self.null_option

        # Set the disabled indicator, if any
        if self.disabled_indicator is not None:
            attrs['disabled-indicator'] = self.disabled_indicator

        # Toggle brief mode
        if not self.brief_mode:
            attrs['data-full'] = 'true'

        # Attach any static query parameters
        for key, value in self.query_params.items():
            widget.add_query_param(key, value)

        return attrs

    def get_bound_field(self, form, field_name):
        bound_field = BoundField(form, self, field_name)

        # Set initial value based on prescribed child fields (if not already set)
        if not self.initial and self.initial_params:
            filter_kwargs = {}
            for kwarg, child_field in self.initial_params.items():
                value = form.initial.get(child_field.lstrip('$'))
                if value:
                    filter_kwargs[kwarg] = value
            if filter_kwargs:
                self.initial = self.queryset.filter(**filter_kwargs).first()

        # Modify the QuerySet of the field before we return it. Limit choices to any data already bound: Options
        # will be populated on-demand via the APISelect widget.
        data = bound_field.value()
        if data:
            field_name = getattr(self, 'to_field_name') or 'pk'
            filter = self.filter(field_name=field_name)
            try:
                self.queryset = filter.filter(self.queryset, data)
            except TypeError:
                # Catch any error caused by invalid initial data passed from the user
                self.queryset = self.queryset.none()
        else:
            self.queryset = self.queryset.none()

        # Set the data URL on the APISelect widget (if not already set)
        widget = bound_field.field.widget
        if not widget.attrs.get('data-url'):
            app_label = self.queryset.model._meta.app_label
            model_name = self.queryset.model._meta.model_name
            data_url = reverse('plugins-api:{}-api:{}-list'.format(app_label, model_name))
            widget.attrs['data-url'] = data_url

        return bound_field


class DynamicModelChoiceField(DynamicModelChoiceMixin, forms.ModelChoiceField):
    """
    Override get_bound_field() to avoid pre-populating field choices with a SQL query. The field will be
    rendered only with choices set via bound data. Choices are populated on-demand via the APISelect widget.
    """

    def clean(self, value):
        """
        When null option is enabled and "None" is sent as part of a form to be submitted, it is sent as the
        string 'null'.  This will check for that condition and gracefully handle the conversion to a NoneType.
        """
        if self.null_option is not None and value == settings.FILTERS_NULL_CHOICE_VALUE:
            return None
        return super().clean(value)
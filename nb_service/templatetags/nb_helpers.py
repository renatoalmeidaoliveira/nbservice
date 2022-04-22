from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()

@register.filter()
def plugin_validated_viewname(model, action):
    """
    Return the view name for the given model and action if valid, or None if invalid.
    """
    viewname = f'plugins:{model._meta.app_label}:{model._meta.model_name}_{action}'
    try:
        # Validate and return the view name. We don't return the actual URL yet because many of the templates
        # are written to pass a name to {% url %}.
        reverse(viewname)
        return viewname
    except NoReverseMatch:
        return None


@register.filter()
def plugin_viewname(model, action):
    """
    Return the view name for the given model and action. Does not perform any validation.
    """
    return f'plugins:{model._meta.app_label}:{model._meta.model_name}_{action}'
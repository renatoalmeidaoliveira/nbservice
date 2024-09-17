from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem


from django.conf import settings

plugin_settings = settings.PLUGINS_CONFIG["nb_service"]

menu_buttons = (
    PluginMenuItem(
        permissions=["nb_service.view_service"],
        link="plugins:nb_service:service_list",
        link_text="Services",
    ),
    PluginMenuItem(
        permissions=["nb_service.view_application"],
        link="plugins:nb_service:application_list",
        link_text="Applications",
    ),
)

if plugin_settings.get("top_level_menu"):
    menu = PluginMenu(
        label="Service Management",
        groups=(("Services", menu_buttons),),
        icon_class="mdi mdi-cog-outline",
    )
else:
    menu_items = menu_buttons
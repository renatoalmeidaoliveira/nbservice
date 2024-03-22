from extras.plugins import PluginMenuItem


menu_items = (
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

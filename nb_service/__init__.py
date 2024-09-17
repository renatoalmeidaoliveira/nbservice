from netbox.plugins import PluginConfig
from .version import __version__


class NbserviceConfig(PluginConfig):
    name = 'nb_service'
    base_url = 'nb_service'
    verbose_name = 'Service Management'
    description = 'ITSM Service Management'
    version = __version__
    author = 'Renato Almeida de Oliveira Zaroubin'
    author_email = 'renato.almeida.oliveira@gmail.com'
    min_version = "4.1.0"
    max_version = "4.1.99"
    required_settings = []
    default_settings = {
        "top_level_menu": True
    }

    def ready(self):
        from . import signals
        super().ready()


config = NbserviceConfig # noqa

from extras.plugins import PluginConfig
from .version import __version__


class NbserviceConfig(PluginConfig):
    name = 'nb_service'
    verbose_name = 'Service Management'
    description = ''
    version = __version__
    author = ''
    author_email = ''
    required_settings = []
    default_settings = {}

    def ready(self):
        from . import signals
        super().ready()


config = NbserviceConfig # noqa

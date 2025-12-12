__version__ = "1.0.0"

from django.urls import include, path
from django.utils.translation import gettext_lazy as _

try:
    from pretix.base.plugins import PluginConfig
except ImportError:

    class PluginConfig:
        pass


class PluginApp(PluginConfig):
    default = True
    name = "pretix_iyzico"
    verbose_name = "iyzico"

    class PretixPluginMeta:
        name = _("iyzico")
        author = "Fidelio Software"
        description = _("Pretix payment provider plugin for iyzico integration")
        visible = True
        version = __version__
        category = "PAYMENT"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # noqa

    @property
    def url(self):
        from . import urls

        return [
            path(
                "iyzico/",
                include((urls.urlpatterns, "pretix_iyzico"), namespace="pretix_iyzico"),
            )
        ]


default_app_config = "pretix_iyzico.PluginApp"

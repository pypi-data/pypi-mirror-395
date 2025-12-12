from django.utils.translation import gettext_lazy as _
from pretix.base.plugins import PluginConfig, PLUGIN_LEVEL_ORGANIZER
from . import __version__

class AccessibilityPluginApp(PluginConfig):
    name = "pretix_all_in_one_accessibility"
    verbose_name = _("All In One Accessibility")

    class PretixPluginMeta:
        name = _("All In One Accessibility")
        author = "Skynet Technologies USA LLC"
        description = _("Website accessibility widget for improving WCAG 2.0, 2.1, 2.2 and ADA compliance!")
        visible = True
        version = __version__
        category = "FEATURE"
        featured = True
        level = PLUGIN_LEVEL_ORGANIZER
        settings_links = [
            (("All In One Accessibility", "Settings"), "plugins:pretix_all_in_one_accessibility:settings", {})
        ]

    def ready(self):
        from . import views  

    
       

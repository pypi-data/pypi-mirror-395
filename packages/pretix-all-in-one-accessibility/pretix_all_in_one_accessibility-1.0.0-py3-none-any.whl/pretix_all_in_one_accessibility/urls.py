from django.urls import path
from .views import AccessibilitySettingsView

app_name = "pretix_all_in_one_accessibility"

urlpatterns = [
    path(
        'control/organizer/<slug:organizer>/pretix_all_in_one_accessibility/settings/',
        AccessibilitySettingsView.as_view(),
        name='settings'
    ),
]

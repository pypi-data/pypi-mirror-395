import requests
from django.views.generic.edit import FormView
from .forms import AllInOneAccessibilityForm
from pretix.control.permissions import OrganizerPermissionRequiredMixin

class AccessibilitySettingsView(OrganizerPermissionRequiredMixin, FormView):
    template_name = 'pretix_all_in_one_accessibility/settings.html'
    form_class = AllInOneAccessibilityForm
    permission = 'can_change_organizer_settings'

    def form_valid(self, form):
        data = form.cleaned_data

        # ---- DOMAIN NAME -----------------------
        from urllib.parse import urlparse
        domain = urlparse(self.request.build_absolute_uri())
        domain_url = f"{domain.scheme}://{domain.hostname}"

        # ---- BASE PAYLOAD ---------------------------------------------
        payload = {
            "u": domain_url,
            "widget_color_code": data["aioa_color_code"],
            "is_widget_custom_position": int(data["enable_widget_icon_position"]),
            "is_widget_custom_size": int(data["enable_icon_custom_size"]),
        }

        # ---- POSITION LOGIC -------------------------------------------
        if not data["enable_widget_icon_position"]:
            payload.update({
                "widget_position_top": 0,
                "widget_position_right": 0,
                "widget_position_bottom": 0,
                "widget_position_left": 0,
                "widget_position": data["aioa_place"],
            })

        else:
            position = {
                "widget_position_top": 0,
                "widget_position_right": 0,
                "widget_position_bottom": 0,
                "widget_position_left": 0,
            }

            # Horizontal
            if data["to_the_right"] == "to_the_left":
                position["widget_position_left"] = data["to_the_right_px"]
            elif data["to_the_right"] == "to_the_right":
                position["widget_position_right"] = data["to_the_right_px"]

            # Vertical
            if data["to_the_bottom"] == "to_the_bottom":
                position["widget_position_bottom"] = data["to_the_bottom_px"]
            elif data["to_the_bottom"] == "to_the_top":
                position["widget_position_top"] = data["to_the_bottom_px"]

            payload.update(position)
            payload["widget_position"] = ""  

        # ---- ICON SIZE LOGIC ------------------------------------------
        if not data["enable_icon_custom_size"]:
            payload.update({
                "widget_icon_size": data["aioa_icon_size"],
                "widget_icon_size_custom": 0,
            })
        else:
            payload.update({
                "widget_icon_size": "",
                "widget_icon_size_custom": data["aioa_size_value"],
            })

        # ---- Remaining fields -----------------------------------------
        widget_size_value = 1 if data["aioa_size"] == "oversize" else 0

        payload.update({
            "widget_size": widget_size_value,
            "widget_icon_type": data["aioa_icon_type"],
        })

        # ---- SEND TO API  -----------------------------------
        files=[
        ]
        headers = {}

        settings_api = "https://ada.skynettechnologies.us/api/widget-setting-update-platform"
        try:
            response = requests.post(url=settings_api ,headers=headers, data=payload, files=files)
            response.raise_for_status()
        except requests.RequestException as e:
            return self.form_invalid(form)

        return super().form_valid(form)


    def get_initial(self):
        # Optional: load default values from external API if needed
        return {}
    
    def get_success_url(self):
        # Redirect back to the same settings page
        return self.request.path

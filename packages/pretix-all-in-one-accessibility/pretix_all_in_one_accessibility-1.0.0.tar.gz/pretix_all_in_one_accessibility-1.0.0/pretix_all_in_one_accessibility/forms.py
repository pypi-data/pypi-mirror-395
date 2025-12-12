from django import forms
from django.utils.safestring import mark_safe

AIOA_SELECT_CHOICES = [
    ('top_left', 'Top Left'),
    ('top_center', 'Top Center'),
    ('top_right', 'Top Right'),
    ('middle_left', 'Middle Left'),
    ('middle_right', 'Middle Right'),
    ('bottom_left', 'Bottom Left'),
    ('bottom_center', 'Bottom Center'),
    ('bottom_right', 'Bottom Right'),
]

AIOA_SIZE_CHOICES = [
    ('regular', 'Regular Size'),
    ('oversize', 'Oversize'),
]

TO_THE_RIGHT_CHOICES = [
    ('to_the_left', 'To the left'),
    ('to_the_right', 'To the right'),
]

TO_THE_BOTTOM_CHOICES = [
    ('to_the_bottom', 'To the bottom'),
    ('to_the_top', 'To the top'),
]

AIOA_ICON_SIZE_CHOICES = [
    ('aioa-big-icon', 'Big'),
    ('aioa-medium-icon', 'Medium'),
    ('aioa-default-icon', 'Default'),
    ('aioa-small-icon', 'Small'),
    ('aioa-extra-small-icon', 'Extra Small'),
]

ICON_CHOICES = [
    (f'aioa-icon-type-{i}', f'/static/pretix_all_in_one_accessibility/icons/{i}.png')
    for i in range(1, 30)  
]

# ================================================================
#   CUSTOM WIDGETS (Pretix-safe HTML/JS widgets)
# ================================================================

class IconSelectWidget(forms.Widget):
    """Clickable tile-style icon selector."""

    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs)
        self.choices = list(choices)

    def render(self, name, value, attrs=None, renderer=None):
        html = ['<div class="aioa-icon-select-wrapper">']

        for option_value, icon_url in self.choices:
            selected = "selected" if value == option_value else ""
            checked = "checked" if value == option_value else ""

            html.append(f"""
                <label class="aioa-icon-option {selected}">
                    <input type="radio" name="{name}" value="{option_value}" {checked}>
                    <img src="{icon_url}" class="aioa-icon-img"/>
                    <span class="aioa-checkmark">&#10004;</span>
                </label>
            """)

        html.append("</div>")
        return mark_safe("\n".join(html))


class IconSizeSelectWidget(forms.Widget):
    """Clickable tile-style size selector with preview image."""

    SIZE_MAP = {
        'aioa-big-icon': 75,
        'aioa-medium-icon': 65,
        'aioa-default-icon': 55,
        'aioa-small-icon': 45,
        'aioa-extra-small-icon': 35,
    }

    def __init__(self, attrs=None, icon_url="", choices=()):
        super().__init__(attrs)
        self.icon_url = icon_url
        self.choices = list(choices)

    def render(self, name, value, attrs=None, renderer=None):
        html = ['<div class="aioa-icon-size-select-wrapper">']

        for option_value, _ in self.choices:
            selected = "selected" if value == option_value else ""
            checked = "checked" if value == option_value else ""
            size = self.SIZE_MAP[option_value]

            html.append(f"""
                <label class="aioa-icon-option {selected}" data-size="{size}">
                    <input type="radio" name="{name}" value="{option_value}" {checked}>
                    <img src="{self.icon_url}" class="aioa-icon-img-size aioa-size-{option_value}"/>

                    <span class="aioa-checkmark">&#10004;</span>
                </label>
            """)

        html.append("</div>")
        return mark_safe("\n".join(html))


# ================================================================
#       MAIN PRETIX FORM
# ================================================================

class AllInOneAccessibilityForm(forms.Form):

    aioa_color_code = forms.CharField(required=False, label="Hex Color Code",help_text="You can customize the ADA Widget color. For example: FF5733")

    enable_widget_icon_position = forms.BooleanField(required=False,initial=False, label="Enable precise accessibility widget icon position")

    to_the_right_px = forms.IntegerField(min_value=0, max_value=250, initial=20, help_text="0 - 250px are permitted values", label="Right offset (PX)")
    to_the_right = forms.ChoiceField(choices=TO_THE_RIGHT_CHOICES,initial="to_the_left", label="To the right")

    to_the_bottom_px = forms.IntegerField(min_value=0, max_value=250, initial=20, label="Bottom offset (PX)", help_text="0 - 250px are permitted values")
    to_the_bottom = forms.ChoiceField(choices=TO_THE_BOTTOM_CHOICES,initial="to_the_bottom", label="To the bottom")

    aioa_place = forms.ChoiceField(choices=AIOA_SELECT_CHOICES,initial="bottom_right", label="Where would you like to place the accessibility icon on your site")

    aioa_size = forms.ChoiceField(choices=AIOA_SIZE_CHOICES,initial="regular", label="Select Widget Size")

    aioa_icon_type = forms.ChoiceField(
        choices=ICON_CHOICES,
        widget=IconSelectWidget(choices=ICON_CHOICES),
        initial="aioa-icon-type-1",
        label="Select icon type"
    )

    enable_icon_custom_size = forms.BooleanField(required=False,initial=False, label="Enable icon custom size")

    aioa_size_value = forms.IntegerField(min_value=20, max_value=150, initial=50, label="Select exact icon size (PX)",help_text="20 - 150px are permitted values")

    aioa_icon_size = forms.ChoiceField(
        choices=AIOA_ICON_SIZE_CHOICES,
        widget=IconSizeSelectWidget(
            choices=AIOA_ICON_SIZE_CHOICES,
            icon_url="/static/pretix_all_in_one_accessibility/icons/1.png"
        ),
        initial="aioa-default-icon",
        label="Select icon size for Desktop"
    )

    # override to update icon_url dynamically
    def clean(self):
        cleaned = super().clean()

        selected = cleaned.get("aioa_icon_type")
        icon_url = dict(ICON_CHOICES).get(selected, "")

        # update the icon-size widget
        self.fields["aioa_icon_size"].widget.icon_url = icon_url

        return cleaned

    


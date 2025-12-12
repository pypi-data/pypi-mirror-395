from django import forms
from django.utils.translation import gettext_lazy as _


class ActionForm(forms.Form):
    """Simplified version of django.contrib.admin.helpers.ActionForm."""

    action = forms.ChoiceField(label=_("Action:"))

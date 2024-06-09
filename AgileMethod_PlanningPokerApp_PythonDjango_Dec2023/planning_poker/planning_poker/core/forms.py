from planning_poker.core.models import PokerSession

from django import forms


class PokerSessionForm(forms.ModelForm):
    class Meta:
        model = PokerSession
        fields = ["product_backlog_file", "mode", "feature_field_name", "players"]
        widgets = {
            "product_backlog_file": forms.FileInput(attrs={"class": "form-control"}),
            "mode": forms.Select(attrs={"class": "form-control"}),
        }

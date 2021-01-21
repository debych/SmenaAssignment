from django import forms


class RenderCheckForm(forms.Form):
    order_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Order number"
        })
    )
    point_id = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "ID of the point"
        })
    )
    order = forms.CharField(
        max_length=1024,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Order"
        })
    )

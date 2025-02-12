from django import forms
from .models import Order


class BaseOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["user", "created_on", "is_completed", "number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["placeholder"] = field.label
            if field.required:
                field.widget.attrs["placeholder"] += "*"


class OrderForm(BaseOrderForm):
    agree_with_terms_of_use = forms.BooleanField(
        required=True,
        label="Запознат съм и съм съгласен с правилата и условията на сайта.",
    )

    def clean_agree_with_terms_of_use(self):
        agreed = self.cleaned_data.get("agree_with_terms_of_use")
        if not agreed:
            raise forms.ValidationError(
                "Трябва да се съгласите с правилата на сайта, преди да поръчате"
            )

        return agreed

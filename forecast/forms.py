from django import forms
from .models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Column



class VolumeForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))
    end_date = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))

    class Meta:
        model = VolumeItem
        fields = ('spirit','amount', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                        Div(
                            Row(
                                Column('spirit', css_class='form-group col-md-6'),
                                Column('amount', css_class='form-group col-md-6'),
                            ),
                            Row(
                                Column('start_date'),
                                Column('end_date'),
                            ),
                            Row(
                                Submit('submit', 'Add', css_class='my-3 btn btn-secondary')
                            )
            )
        )


class SpiritForm(forms.ModelForm):
    class Meta:
        model = Spirit
        fields =('name','category')

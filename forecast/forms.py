from django import forms
from .models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Column



class VolumeForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))
    end_date = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))

    class Meta:
        model = VolumeItem
        fields = ('product','amount', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                        Div(
                            Row(
                                Column('product', css_class='form-group col-md-6'),
                                Column('amount', css_class='form-group col-md-6'),
                            ),
                            Row(
                                Column('start_date'),
                                Column('end_date'),
                            ),
                            Row(
                                Submit('submit', 'Add', css_class='my-3 btn btn-secondary w-50'),
                                css_class='d-flex justify-content-center'
                            )
            )
        )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =('name','category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                        Div(
                            Row(
                                Column('name', css_class='form-group col-md-6'),
                                Column('category', css_class='form-group col-md-6'),
                            ),
                            Row(
                                Submit('submit', 'Add', css_class='my-3 btn btn-secondary w-50'),
                                css_class='d-flex justify-content-center'
                            )
            )
        )


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                        Div(
                            Row(
                                Column('name', css_class='form-group col-md-6'),
                                css_class='d-flex justify-content-center'

                            ),
                            Row(
                                Submit('submit', 'Add', css_class='my-3 btn btn-secondary w-50'),
                                css_class='d-flex justify-content-center'
                            )
            )
        )
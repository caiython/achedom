from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div
from django.urls import reverse
from django import forms


class LogoutForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-logout_form'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('logout')
        self.helper.form_class = 'py-2'

        self.helper.layout = Layout(
            Div(
                Submit('submit', 'Yes', css_class='btn-dark mb-3'),
                css_class='d-grid gap-2 col-6 mx-auto'
            ),

        )

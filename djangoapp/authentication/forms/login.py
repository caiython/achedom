from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from authentication.models import User


class LoginForm(forms.Form):

    class Meta:
        model = User

    email = forms.CharField(
        label="Email",
        required=True,
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-login_form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'
        self.helper.form_class = 'py-2'

        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-dark'))

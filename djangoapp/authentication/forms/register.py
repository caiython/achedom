from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import re
from django.urls import reverse
from authentication.models import User
from django import forms


class RegisterForm(forms.Form):

    email = forms.EmailField(
        label="Email",
        required=True,
        error_messages={
            'required': 'Email field is required.',
            'invalid': 'Provide a valid email address.'
        },
        widget=forms.EmailInput(attrs={'placeholder': 'email@domain.com'})
    )

    password = forms.CharField(
        label="Password",
        required=True,
        error_messages={
            'required': 'Password field is required.'
        },
        widget=forms.PasswordInput(),
    )

    confirm = forms.CharField(
        label="Confirm password",
        required=True,
        error_messages={
            'required': 'Password field is required.'
        },
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-register_form'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('register')

        # self.helper.form_class = 'py-2'

        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-dark'))

    def validate_password(self, password):
        """
        Validates that the password meets the following criteria:
        - At least 6 characters long
        - Contains at least one character
        - Contains at least one digit
        """
        if len(password) < 6:
            self.add_error(
                'password', 'Password must be at least 6 characters long.'
            )

        if not re.search(r'[a-zA-Z]', password):
            self.add_error(
                'password', 'Password must contain at least one character.'
            )

        if not re.search(r'\d', password):
            self.add_error(
                'password', 'Password must contain at least one digit.'
            )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")

        self.validate_password(password)

        if User.objects.filter(email=email):
            self.add_error('email', 'The provided email already exists.')

        if password and confirm and password != confirm:
            self.add_error('confirm', 'Passwords must match')

        return cleaned_data

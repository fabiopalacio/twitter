import re
from django import forms  # type: ignore
from django.contrib.auth.models import User

from utils.utils_form import add_placeholder


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise forms.ValidationError((
            'A senha deve possuir, pelo menos, 8 caracteres sendo '
            'ao menos uma letra maiúscula, uma minúscula e um número.'),
            code='invalid'
        )


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Nome de usuário')
        add_placeholder(self.fields['password'], 'Senha')

    username = forms.CharField(
        label='Nome de usuário',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'}),
        label="Senha",
    )


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Nome de usuário')
        add_placeholder(self.fields['email'], 'E-mail')
        add_placeholder(self.fields['password'], 'Senha')
        add_placeholder(self.fields['password2'], 'Confirme sua senha')

    username = forms.CharField(
        required=True,
        label='Nome de usuário',
        help_text='Deve conter entre 4 e 150 caracteres.',
        error_messages={
            'required': 'Campo obrigatório.',
            'min_length': 'Deve conter pelo menos 4 caracteres.',
            'max_length': 'Deve conter, no máximo, 150 caracteres.',
            'unique': 'Nome de usuário não disponível.'

        },

        min_length=4,
        max_length=150
    )

    email = forms.EmailField(
        error_messages={
            'required': 'Campo obrigatório.',
            'invalid': 'Deve ser um e-mail válido.',
        },
        required=True,
        label='E-mail',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': 'Campo obrigatório.'
        },
        help_text='A senha deve possuir, pelo menos, 8 caracteres sendo '
        'ao menos uma letra maiúscula, uma minúscula e um número.',
        validators=[strong_password],

        label='Senha'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        label='Confirme sua senha',
        error_messages={
            'required': 'Campo obrigatório.'
        },

    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise forms.ValidationError(
                'E-mail já cadastrado.', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:

            password_confirmation_error = forms.ValidationError(
                "As senhas devem ser iguais.",
                code='invalid'
            )

            raise forms.ValidationError(
                {

                    'password2': [password_confirmation_error]
                }
            )

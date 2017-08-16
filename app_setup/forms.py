# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class EnvironmentForm(forms.Form):
    ENGINES = [('sqlite', 'SQLite'),
               ('mysql', 'MySQL'),
               ('postgres', 'PostgreSQL')]

    proxy_name = forms.CharField(label='Proxy Name', max_length=100)
    central_host = forms.CharField(label='Host', max_length=100)
    central_port = forms.IntegerField(label='Port')

    engine = forms.ChoiceField(choices=ENGINES, widget=forms.RadioSelect())
    python = forms.CharField(label='Python Interpreter', max_length=100, required=False, disabled=True)
    host = forms.CharField(label='Host', max_length=100, required=False)
    port = forms.IntegerField(label='Port', required=False)
    name = forms.CharField(label='Database Name', max_length=100, required=False)
    username = forms.CharField(label='Username', max_length=100, required=False)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(), required=False)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-2 col-sm-offset-2'
    helper.field_class = 'col-sm-4'
    helper.form_id = 'main-form'
    helper.layout = Layout(
        Fieldset(
            'NEO Server Central',
            'central_host',
            'central_port',
            'proxy_name',
        ),
        Fieldset(
            'Interpreter',
            'python',
        ),
        Fieldset(
            'Database Engine',
            'engine',
        ),
        Fieldset(
            'Database Information',
            'host',
            'port',
            'name',
            'username',
            'password',
            css_class='db'
        ),
        FormActions(
            Submit('save_changes', 'Configure environment.', css_class="btn-primary"),
            css_class='actions'
        )
    )


class UserForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-4'
    helper.form_id = 'main-form'
    helper.layout = Layout(
        Fieldset(
            'Superuser Information',
            'email',
            'username',
            'password',
        ),
        FormActions(
            Submit('save_changes', 'Create superuser', css_class="btn-primary"),
        )
    )

    # def clean_username(self):
    #     raise forms.ValidationError("Username already exists!")

    # def clean_password(self):
    #     raise forms.ValidationError("El password es muy debil, ponete las eveready.")

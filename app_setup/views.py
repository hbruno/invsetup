# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import messages

import os
import sys
import environ
import subprocess
import _mysql

from .forms import EnvironmentForm, UserForm


class WelcomeView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(WelcomeView, self).get_context_data(**kwargs)
        context['step'] = 1
        return context


class EnvironmentView(View):
    step = 2
    template_name = 'setup_environment.html'
    form_class = EnvironmentForm
    env_separator = '# -- dynamic settings --'

    def clean (self, env_file):
        with open(env_file,"r") as f:
            lines = f.readlines()
        print lines

        with open(env_file,"w") as f:
            ins = True
            for line in lines:
                ins = ins and line.rstrip() != self.env_separator.rstrip()
                if ins:
                    f.write(line)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={
            'python': sys.executable,
            'engine': 'sqlite'
        })
        return render(request, self.template_name, {'step': self.step, 'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'step': self.step, 'form': form})

        env_file = str(settings.ROOT_DIR.path('.env'))
        self.clean(env_file)
        open(env_file, 'a').write('\n')
        open(env_file, 'a').write(self.env_separator)
        open(env_file, 'a').write('\nSETUP_COMPLETED=True')
        open(env_file, 'a').write('\nNEO_CENTRAL_HOST=%s' % form.cleaned_data['central_host'])
        open(env_file, 'a').write('\nNEO_CENTRAL_PORT=%s' % form.cleaned_data['central_port'])
        open(env_file, 'a').write('\nNEO_PROXY_ALIAS=%s' % form.cleaned_data['proxy_name'])

        if form.cleaned_data['engine'] == 'sqlite':
            if not os.path.isfile(str(settings.ROOT_DIR.path(form.cleaned_data['name']))):
                self.clean(env_file)
                messages.error(request, 'Sqlite database file not found. %s' % str(settings.ROOT_DIR.path(form.cleaned_data['name'])))
                return render(request, self.template_name, {'step': self.step, 'form': form})

            open(env_file, 'a').write('\nDATABASE_URL=sqlite:///%s' % str(settings.ROOT_DIR.path(form.cleaned_data['name'])))
        else:
            if form.cleaned_data['engine'] == 'mysql':
                try:
                    db = _mysql.connect(
                            form.cleaned_data['host'], 
                            form.cleaned_data['username'], 
                            form.cleaned_data['password'], 
                            form.cleaned_data['name'])
                except _mysql.Error as e:
                    messages.error(request, 'Can\'t connect to MySQL database. %s' % str(e))
                    return render(request, self.template_name, {'step': self.step, 'form': form})


            open(env_file, 'a').write('\nDATABASE_URL=%s://%s:%s@%s:%s/%s' % (
                form.cleaned_data['engine'],
                form.cleaned_data['username'],
                form.cleaned_data['password'],
                form.cleaned_data['host'],
                form.cleaned_data['port'],
                form.cleaned_data['name']
            ))

        env = environ.Env(DEBUG=(bool, False), )
        env.read_env(env_file)
        settings.SETUP_COMPLETED = True
        settings.DATABASES['default'] = env.db('DATABASE_URL')

        return HttpResponseRedirect(reverse('setup:migration'))


class MigrateView(View):
    template_name = 'setup_migration.html'

    def get(self, request, *args, **kwargs):
        python_file = sys.executable
        manage_file = str(settings.ROOT_DIR.path('manage.py'))

        try:
            command = '%s migrate --noinput' % manage_file
            process = subprocess.Popen([python_file, ] + command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # noqa
            (outStream, errStream) = process.communicate()
        except Exception as e:
            outStream = ''
            errStream = str(e)

        return render(request, self.template_name, {'step': 3, 'out': outStream, 'err': errStream})

    def post(self, request, *args, **kwargs):

        return HttpResponseRedirect(reverse('setup:user'))


class UserView(View):
    template_name = 'setup_user.html'
    form_class = UserForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'step': 4, 'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'step': 4, 'form': self.form_class()})

        user, _ = User.objects.get_or_create(
            email=form.cleaned_data['email'],
            username=form.cleaned_data['username'],
            defaults={'is_superuser': True, 'is_staff': True})
        user.set_password(form.cleaned_data['password'])
        user.save()

        return HttpResponseRedirect(reverse('setup:fixture'))


class FixtureView(View):
    template_name = 'setup_fixture.html'

    def get(self, request, *args, **kwargs):
        python_file = sys.executable
        manage_file = str(settings.ROOT_DIR.path('manage.py'))

        try:
            command = '%s loaddata' % manage_file
            process = subprocess.Popen([python_file, ] + command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # noqa
            (outStream, errStream) = process.communicate()
        except Exception as e:
            outStream = ''
            errStream = str(e)

        return render(request, self.template_name, {'step': 5, 'out': outStream, 'err': errStream})


class CompleteView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(CompleteView, self).get_context_data(**kwargs)
        context['step'] = 6
        return context


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.conf import settings

import re
import environ
import subprocess


class SetupView(View):
    template_name = 'setup.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        env_file = str(settings.ROOT_DIR.path('.env'))

        open(env_file, 'a').write('\n# -- dynamic settings --')
        open(env_file, 'a').write('\nSETUP_COMPLETED=True')
        open(env_file, 'a').write('\nDATABASE_URL=sqlite:///%s' % str(settings.ROOT_DIR.path('db.sqlite3')))
        env = environ.Env(DEBUG=(bool, False), )
        env.read_env(env_file)

        settings.SETUP_COMPLETED = True
        settings.DATABASES['default'] = env.db('DATABASE_URL')
        print settings.DATABASES['default']

        import django
        django.setup()

        return HttpResponseRedirect('/setup/migrate/')


class MigrateView(View):
    template_name = 'migrate.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        python_file = '/Users/hbruno/.virtualenvs/invsetup/bin/python'
        manage_file = str(settings.ROOT_DIR.path('manage.py'))

        print python_file + ' ' + manage_file
        try:
            command = '%s migrate' % manage_file
            process = subprocess.Popen([python_file, ] + command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # noqa
            (outStream, errStream) = process.communicate()
        except Exception as e:
            outStream = ''
            errStream = str(e)

        return render(request, self.template_name, {'out': outStream, 'err': errStream})

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)

        return HttpResponseRedirect('/')

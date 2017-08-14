# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.conf import settings

from django.db import connections, router
from django.db.utils import ConnectionHandler, ConnectionRouter

import environ
import subprocess


class SetupView(View):
    template_name = 'setup.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        print request.POST
        env_file = str(settings.ROOT_DIR.path('.env'))

        open(env_file, 'a').write('\n# -- dynamic settings --')
        open(env_file, 'a').write('\nSETUP_COMPLETED=True')

        if request.POST['db_type'] == 'sqlite':        
            open(env_file, 'a').write('\nDATABASE_URL=sqlite:///%s' % str(settings.ROOT_DIR.path('db.sqlite3')))
        else:
            open(env_file, 'a').write('\nDATABASE_URL=%s://%s:%s@%s:%s/%s' % (
                request.POST['db_type'],
                request.POST['db_user'],
                request.POST['db_pass'],
                request.POST['db_host'],
                request.POST['db_port'],
                request.POST['db_name']
            ))

        env = environ.Env(DEBUG=(bool, False), )
        env.read_env(env_file)

        settings.SETUP_COMPLETED = True
        settings.DATABASES['default'] = env.db('DATABASE_URL')
        print settings.DATABASES['default']

        connections = ConnectionHandler()
        router = ConnectionRouter()

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
            command = '%s migrate --noinput' % manage_file
            process = subprocess.Popen([python_file, ] + command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # noqa
            (outStream, errStream) = process.communicate()
        except Exception as e:
            outStream = ''
            errStream = str(e)

        return render(request, self.template_name, {'out': outStream, 'err': errStream})

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)

        return HttpResponseRedirect('/')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib import messages

from django.db import connection, connections, router
from django.db.utils import ConnectionHandler, ConnectionRouter

import os
import sys
import environ
import subprocess


class SetupView(View):
    template_name = 'setup.html'
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
        return render(request, self.template_name, { 'python': sys.executable})

    def post(self, request, *args, **kwargs):
        env_file = str(settings.ROOT_DIR.path('.env'))
        self.clean(env_file)
        open(env_file, 'a').write('\n')
        open(env_file, 'a').write(self.env_separator)
        open(env_file, 'a').write('\nSETUP_COMPLETED=True')
        
        if request.POST['db_type'] == 'sqlite':        
            if not os.path.isfile(str(settings.ROOT_DIR.path(request.POST['db_name']))):
                self.clean(env_file)
                messages.error(request, 'Sqlite database file not found.')
                messages.error(request, str(settings.ROOT_DIR.path(request.POST['db_name'])))
                return render(request, self.template_name, {})

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

        return HttpResponseRedirect('/setup/migrate/')


class MigrateView(View):
    template_name = 'migrate.html'

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

        return render(request, self.template_name, {'out': outStream, 'err': errStream})

    def post(self, request, *args, **kwargs):

        return HttpResponseRedirect('/')


class FixtureView(View):
    template_name = 'migrate.html'

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

        return render(request, self.template_name, {'out': outStream, 'err': errStream})

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)

        return HttpResponseRedirect('/')

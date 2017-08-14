from django.shortcuts import redirect
from django.conf import settings
import re


class NeoSetupMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not re.match('^/setup/.*', request.path) and not settings.SETUP_COMPLETED:
            return redirect('/setup/')

        response = self.get_response(request)
        return response

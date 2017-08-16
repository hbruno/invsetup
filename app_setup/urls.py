from django.conf.urls import url
from django.views.generic import TemplateView
from app_setup.views import WelcomeView, CompleteView, EnvironmentView, MigrateView, UserView, FixtureView


urlpatterns = [
    url(r'^$', WelcomeView.as_view(template_name="setup_welcome.html"), name="welcome"),
    url(r'^environment/$', EnvironmentView.as_view(), name="environment"),
    url(r'^migrate/$', MigrateView.as_view(), name="migration"),
    url(r'^user/$', UserView.as_view(), name="user"),
    url(r'^fixture/$', FixtureView.as_view(), name="fixture"),
    url(r'^completed/$', CompleteView.as_view(template_name="setup_completed.html"), name="completed"),
]

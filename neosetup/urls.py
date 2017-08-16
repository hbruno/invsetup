from django.conf.urls import url, include
from app_main.views import MainView

urlpatterns = [
    url(r'^$', MainView.as_view()),
    url(r'^setup/', include("app_setup.urls", namespace="setup")),
]

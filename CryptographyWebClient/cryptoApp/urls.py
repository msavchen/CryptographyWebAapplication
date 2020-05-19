from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('mac', views.mac, name='mac'),
    path('key', views.key, name='key'),
    path('hash', views.hash, name='hash'),
    path('encrypt', views.encrypt, name='encrypt'),
    path('decrypt', views.decrypt, name='decrypt'),
]
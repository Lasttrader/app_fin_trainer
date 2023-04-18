"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),  # Оставили только allauth
    path('pages/', include('django.contrib.flatpages.urls')), #это статичные страницы
    path('', include('NewsPortal.urls')), #это страницы с приложения
    path('swagger-ui/', TemplateView.as_view(
       template_name='swagger_ui.html',
       extra_context={'schema_url':'openapi-schema'}
   ), name='swagger_ui')
]

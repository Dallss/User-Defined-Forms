"""
URL configuration for user_defined_forms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from core.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/forms/', get_forms, name='get_form'),
    path('api/forms/<int:form_id>/', get_form, name='get_form'),
    path('api/forms/<int:form_id>/responses', get_form_responses, name='get_form'),
    path('api/forms/<int:form_id>/post-response/', post_response, name='post_rsponse')
]

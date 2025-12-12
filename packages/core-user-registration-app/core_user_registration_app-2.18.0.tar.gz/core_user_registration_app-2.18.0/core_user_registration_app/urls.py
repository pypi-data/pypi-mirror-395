"""core_user_registration_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include
from django.urls import re_path

import core_user_registration_app.views.user.ajax as user_ajax
import core_user_registration_app.views.user.views as registration_views

urlpatterns = [
    re_path("captcha/", include("captcha.urls")),
    re_path(
        r"^account-request/$",
        registration_views.request_new_account,
        name="core_user_registration_app_account_request",
    ),
    re_path(
        r"^request-metadata/(?P<objectid>\w+)/(?P<accountid>\w+)$",
        registration_views.AccountCreationView.as_view(),
        name="core_user_registration_app_account_metadata",
    ),
    re_path(
        r"^request-metadata/data-structure-element/value$",
        user_ajax.data_structure_element_value,
        name="core_user_registration_app_data_structure_element_value",
    ),
    re_path(
        r"^save-data$",
        user_ajax.save_data,
        name="core_user_registration_app_save_data",
    ),
]

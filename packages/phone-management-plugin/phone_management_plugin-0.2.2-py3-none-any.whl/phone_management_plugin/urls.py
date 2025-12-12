from django.urls import include, path
from django.views.generic.base import RedirectView
from netbox.views.generic import ObjectChangeLogView
from utilities.urls import get_model_urls
from . import models, views

urlpatterns = (
    path("phonenumbers/", include(get_model_urls("phone_management_plugin", "phonenumber", detail=False))),
    path("phonenumbers/<int:pk>/", include(get_model_urls("phone_management_plugin", "phonenumber"))),
    path("phonenumberranges/", include(get_model_urls("phone_management_plugin", "phonenumberrange", detail=False))),
    path("phonenumberranges/<int:pk>/", include(get_model_urls("phone_management_plugin", "phonenumberrange"))),
    path("sims/", include(get_model_urls("phone_management_plugin", "sim", detail=False))),
    path("sims/<int:pk>/", include(get_model_urls("phone_management_plugin", "sim"))),
    path("simadmins/", include(get_model_urls("phone_management_plugin", "simadmin", detail=False))),
    path("simadmins/<int:pk>/", include(get_model_urls("phone_management_plugin", "simadmin"))),
)

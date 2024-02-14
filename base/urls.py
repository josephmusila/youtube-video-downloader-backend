from django.urls import path
from . import views

urlpatterns=[
        path("getData",views.index3,name="getData")
]
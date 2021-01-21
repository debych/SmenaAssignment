from django.urls import path
from . import views

urlpatterns = [
    path("create_checks/", views.create_checks, name='create_checks'),
    path("new_checks/<str:api_key>/", views.new_checks, name='new_checks'),
    path("check/<str:api_key>/<int:check_id>/", views.check, name='check_download'),
]

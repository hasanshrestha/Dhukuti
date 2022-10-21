from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("fileUpload/", views.fileUpload, name="fileUpload"),
    path("showAllFiles/", views.showAllFiles, name="showAllFiles"),
    path("searchFiles/", views.searchFiles, name="searchFiles"),
    path("register/", views.register, name="register"),
    path("", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]

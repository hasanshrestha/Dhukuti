from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("fileUpload/", views.fileUpload, name="fileUpload"),
    path("", views.showAllFiles, name="showAllFiles"),
    path("searchFiles/", views.searchFiles, name="searchFiles"),
]

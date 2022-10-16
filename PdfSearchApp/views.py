from multiprocessing import context
from urllib import request
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .form import FilesForm, CreateUserForm, LoginAuthenticationForm
from .models import Files
import PyPDF2
import mimetypes
import os
from PIL import Image
import pytesseract
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from PdfSearchApp import form

# from PIL import Image
# from pytesseract import pytesseract

# Create your views here.

def index(request):
    file_form = FilesForm()
    return render(request, "index.html", {"form": file_form})


def fileUpload(request):
    file_form = FilesForm()
    if request.method == "POST":
        try:
            # title = request.POST.get("title")
            title = request.FILES["file"].name
            description = ""
            file = request.FILES["file"]

            pdfObj = PyPDF2.PdfFileReader(file)
            for i in range(0, pdfObj.getNumPages()):
                description += pdfObj.getPage(i).extractText()

            newdoc = Files(title=title[:-4],
                           description=description, file=file)
            newdoc.save()
            msg = "File Uploaded Successfully!!"
            return render(request, "fileupload.html", {"form": file_form, "msg": msg})
        except:
            msg = "Error. Cannot Upload File!!!"
            return render(request, "fileupload.html", {"form": file_form, "msg": msg})
    else:
        msg = ""
        return render(request, "fileupload.html", {"form": file_form, "msg": msg})


def showAllFiles(request):
    data = Files.objects.all()
    return render(request, "showAllFiles.html", {"data": data})


def searchFiles(request):
    print("search data: ", request.GET.get("search"))
    data = Files.objects.filter(description__search=request.GET.get("search"))
    counter = data.count()
    return render(
        request,
        "showAllFiles.html",
        {"data": data, "searchKey": request.GET.get(
            "search"), "counter": counter},
    )


def readImage(request):
    img = Image.open('')
    text = pytesseract.image_to_string(img)
    print(text)

    # # If you don't have tesseract executable in your PATH, include the following:
    # pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
    # # Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

    # # Simple image to string
    # print(pytesseract.image_to_string(Image.open('test.png')))

    # # In order to bypass the image conversions of pytesseract, just use relative or absolute image path
    # # NOTE: In this case you should provide tesseract supported images or tesseract will return error
    # print(pytesseract.image_to_string('test.png'))


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The Account have been created')
            return redirect('/login')
        else:
            messages.error(request, 'The Account is not created')

    context = {'form': form}
    return render(request, 'register.html', context)


def login(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/index')

    if request.POST:
        form = LoginAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                messages.info(request, 'You have been logged in successfully')
                dj_login(request, user)
                return redirect('/index')
    else:
        form = LoginAuthenticationForm()

    context['login_form'] = form
    return render(request, 'login.html', context)


def logout(request):
    dj_logout(request)
    messages.info(request, 'You have been logged out successfully')
    return redirect('/index')

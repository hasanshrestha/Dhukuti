from django.shortcuts import render, redirect
from .form import FilesForm, CreateUserForm, LoginAuthenticationForm
from .models import Files, WordFile
import PyPDF2
import mimetypes
import os
from django.http.response import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
import subprocess
from PIL import Image

import pytesseract
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib import messages

# from PIL import Image
# from pytesseract import pytesseract

# Create your views here.

# @login_required(login_url="signin")
def index(request):
    file_form = FilesForm()
    return render(request, "index.html", {"form": file_form})


def fileUpload(request):
    file_form = FilesForm()
    if request.method == "POST":
        try:
            print("Testing Testing")
            for file in request.FILES.getlist("file"):
                print("Testing Testing 1")
                mimetype = file.content_type
                if (
                    mimetype
                    == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                ):
                    title = file.name
                    file = file

                    newdoc = WordFile(title=title[:-5], file=file)
                    newdoc.save()

                    print("Newdoc Title Name: ", newdoc.file.name)
                    new_file_name = newdoc.file.name
                    file_path = (
                        os.path.join(settings.BASE_DIR, "media") + "/" + new_file_name
                    )
                    output_dir = (
                        os.path.join(settings.BASE_DIR, "media") + "/" + "files" + "/"
                    )
                    # filePATH = os.path.join(settings.BASE_DIR, "media") + "/wordfiles/"
                    print("File Path: ", file_path)
                    print("Output File Path: ", output_dir)

                    # convert
                    output = subprocess.check_output(
                        [
                            "libreoffice",
                            "--convert-to",
                            "pdf",
                            "--outdir",
                            output_dir,
                            file_path,
                        ],
                    )
                    print(output)

                    # extract text from pdf
                    pdf_file_path = (
                        os.path.join(settings.BASE_DIR, "media")
                        + "/files/"
                        + new_file_name[:-5]
                        + ".pdf"
                    )
                    print("Pdf File Path: ", pdf_file_path)
                    title = file.name
                    description = ""
                    file = "files/" + new_file_name[:-5] + ".pdf"

                    pdfObj = PyPDF2.PdfFileReader(pdf_file_path)
                    for i in range(0, pdfObj.getNumPages()):
                        description += pdfObj.getPage(i).extractText()

                    newdoc = Files(
                        title=title[:-5],
                        description=description,
                        file=file,
                        filetype="pdf",
                    )
                    newdoc.save()
                    # msg = "File Uploaded Successfully!!"
                    # return render(
                    #     request, "fileupload.html", {"form": file_form, "msg": msg}
                    # )

                elif mimetype == "application/pdf":
                    # title = request.POST.get("title")
                    title = file.name
                    description = ""
                    file = file

                    pdfObj = PyPDF2.PdfFileReader(file)
                    for i in range(0, pdfObj.getNumPages()):
                        description += pdfObj.getPage(i).extractText()

                    newdoc = Files(
                        title=title[:-4],
                        description=description,
                        file=file,
                        filetype="pdf",
                    )
                    newdoc.save()
                    # msg = "File Uploaded Successfully!!"
                    # return render(
                    #     request, "fileupload.html", {"form": file_form, "msg": msg}
                    # )
                else:
                    msg = "Select Word or Pdf Files Only!!"
                    return render(
                        request, "fileupload.html", {"form": file_form, "msg": msg}
                    )
            msg = "File Uploaded Successfully!!"
            # return render(request, "fileupload.html", {"form": file_form, "msg": msg})
            return JsonResponse({"data": msg})
        except Exception as e:
            msg = "Error. Cannot Upload File!!!"
            return JsonResponse({"data": msg})
            # return e
            # return render(request, "fileupload.html", {"form": file_form, "msg": msg})
    else:
        msg = ""
        return render(request, "fileupload.html", {"form": file_form, "msg": msg})


def showAllFiles(request):
    data = Files.objects.all()
    print("Counter: ", data.count())
    return render(request, "showAllFiles.html", {"data": data})


def searchFiles(request):
    print("search data: ", request.GET.get("search"))
    data = Files.objects.filter(description__search=request.GET.get("search"))
    counter = data.count()
    return render(
        request,
        "showAllFiles.html",
        {"data": data, "searchKey": request.GET.get("search"), "counter": counter},
    )


def readImage(request):
    img = Image.open("")
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

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The Account have been created")
            return redirect("login")
        else:
            messages.error(request, "The Account is not created")

    context = {"form": form}
    return render(request, "register.html", context)


def login(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("showAllFiles")

    if request.POST:
        form = LoginAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)

            if user:
                messages.info(request, "You have been logged in successfully")
                dj_login(request, user)
                return redirect("showAllFiles")
    else:
        form = LoginAuthenticationForm()

    context["login_form"] = form
    return render(request, "login.html", context)


def logout(request):
    dj_logout(request)
    messages.info(request, "You have been logged out successfully")
    return redirect("login")

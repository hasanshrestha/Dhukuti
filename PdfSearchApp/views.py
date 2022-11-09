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
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from pytesseract import pytesseract
import cv2
import ocrmypdf

# Create your views here.

# @login_required(login_url="signin")
def index(request):
    file_form = FilesForm()
    return render(request, "index.html", {"form": file_form})


@csrf_exempt
def fileUpload(request):
    file_form = FilesForm()
    if request.method == "POST":
        fileResponse = []
        status = []
        filename = ""
        try:
            files = request.FILES.getlist("file")
            for file in files:
                # file = request.FILES["file"]
                filename = file.name
                print(filename)
                print("hell2")
                mimetype = file.content_type
                print("Mimetype: ", mimetype)
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
                    fileResponse.append(filename)
                    status.append("success")

                elif mimetype == "application/msword":
                    title = file.name
                    file = file

                    newdoc = WordFile(title=title[:-4], file=file)
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
                        + new_file_name[:-4]
                        + ".pdf"
                    )
                    print("Pdf File Path: ", pdf_file_path)
                    title = file.name
                    description = ""
                    file = "files/" + new_file_name[:-4] + ".pdf"

                    pdfObj = PyPDF2.PdfFileReader(pdf_file_path)
                    for i in range(0, pdfObj.getNumPages()):
                        description += pdfObj.getPage(i).extractText()

                    newdoc = Files(
                        title=title[:-4],
                        description=description,
                        file=file,
                        filetype="pdf",
                    )
                    newdoc.save()
                    fileResponse.append(filename)
                    status.append("success")

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
                    fileResponse.append(filename)
                    status.append("success")

                elif mimetype == "application/vnd.ms-powerpoint":
                    title = file.name
                    file = file

                    newdoc = WordFile(title=title[:-4], file=file)
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
                        + new_file_name[:-4]
                        + ".pdf"
                    )
                    print("Pdf File Path: ", pdf_file_path)
                    title = file.name
                    description = ""
                    file = "files/" + new_file_name[:-4] + ".pdf"

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
                    fileResponse.append(filename)
                    status.append("success")

                elif mimetype == "image/jpeg":
                    title = file.name
                    file = file

                    newdoc = WordFile(title=title[:-4], file=file)
                    newdoc.save()

                    print("Newdoc Title Name: ", newdoc.file.name)
                    new_file_name = newdoc.file.name
                    file_path = (
                        os.path.join(settings.BASE_DIR, "media") + "/" + new_file_name
                    )

                    # extract text from image
                    img_cv = cv2.imread(file_path)
                    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

                    output_dir = os.path.join(settings.BASE_DIR, "media")

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

                    pdf_file_path = (
                        os.path.join(settings.BASE_DIR, "media")
                        + "/"
                        + new_file_name[:-4]
                        + ".pdf"
                    )

                    save_dir = (
                        os.path.join(settings.BASE_DIR, "media")
                        + "/"
                        + "files"
                        + "/"
                        + new_file_name[:-4]
                        + ".pdf"
                    )

                    print("Pdf File Path: ", pdf_file_path)
                    print("Save File Path: ", save_dir)

                    ocrmypdf.ocr(pdf_file_path, save_dir)

                    newdoc = Files(
                        title=title[:-4],
                        description=pytesseract.image_to_string(img_rgb),
                        file="files/" + new_file_name[:-4] + ".pdf",
                        filetype="image",
                    )
                    newdoc.save()

                    fileResponse.append(filename)
                    status.append("success")

                elif mimetype == "image/png":
                    title = file.name
                    file = file

                    newdoc = WordFile(title=title[:-4], file=file)
                    newdoc.save()

                    print("Newdoc Title Name: ", newdoc.file.name)
                    new_file_name = newdoc.file.name
                    file_path = (
                        os.path.join(settings.BASE_DIR, "media") + "/" + new_file_name
                    )

                    # extract text from image
                    img_cv = cv2.imread(file_path)
                    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

                    output_dir = os.path.join(settings.BASE_DIR, "media")

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
                        + "/"
                        + new_file_name[:-4]
                        + ".pdf"
                    )

                    save_dir = (
                        os.path.join(settings.BASE_DIR, "media")
                        + "/"
                        + "files"
                        + "/"
                        + new_file_name[:-4]
                        + ".pdf"
                    )

                    print("Pdf File Path: ", pdf_file_path)
                    print("Save File Path: ", save_dir)

                    newdoc = Files(
                        title=title[:-4],
                        description=pytesseract.image_to_string(img_rgb),
                        file="files/" + new_file_name[:-4] + ".pdf",
                        filetype="image",
                    )
                    newdoc.save()

                    ocrmypdf.ocr(pdf_file_path, save_dir)

                    fileResponse.append(filename)
                    status.append("success")

                else:
                    fileResponse.append(filename)
                    status.append("failed")
            return JsonResponse({"data": fileResponse, "status": status})
        except Exception as e:
            fileResponse.append(filename)
            status.append("failed")
            return JsonResponse({"data": fileResponse, "status": status})
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
        {"data": data, "searchKey": request.GET.get("search"), "counter": counter},
    )


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

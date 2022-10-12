from django.shortcuts import render
from .form import FilesForm
from .models import Files
import PyPDF2
import mimetypes
import os
from django.http.response import HttpResponse
from PIL import Image

import pytesseract

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

            newdoc = Files(title=title[:-4], description=description, file=file)
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
        {"data": data, "searchKey": request.GET.get("search"), "counter": counter},
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

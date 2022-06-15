from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import BookForm
from .models import Book
import pandas as pd 
import numpy as np
from PIL import Image
from firebase import firebase
import json


class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        width = request.POST.get("width", "")
        height = request.POST.get("height", "")
        print(width)
        print(uploaded_file)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        # print(name)
        context['url'] = fs.url(name)

        red_image = Image.open(uploaded_file)
        red_image_rgb = red_image.convert("RGB")
        image = red_image_rgb.resize((int(width), int(height)))
        pixels = image.load()
        width, height = image.size
        all_pixels = []
        for x in range(width):
            for y in range(height):
                cpixel = image.getpixel((x,y))
                all_pixels.append(cpixel)
        dframe = pd.DataFrame(all_pixels, columns=['r','g', 'b'])
        d = dframe.to_json(orient='records')
        print(d)
        print(dframe)
        data = json.loads(d)
        myDB = firebase.FirebaseApplication("https://my-awesome-pr-656bc-default-rtdb.firebaseio.com/",None)
        myDB.post("image1",data)
        

    return render(request, 'upload.html', context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'

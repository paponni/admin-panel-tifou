from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

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
        # print(np.linalg.inv(all_pixels))
        dframe = pd.DataFrame(all_pixels, columns=['r','g', 'b'])
        d = dframe.to_json(orient='records')
        # inv = print(np.linalg.inv(d))
        print(d)
        
        # print(dframe)
        data = json.loads(d)
        data2=[data[3],data[7],data[11],data[15],data[19],data[2],data[6],data[10],data[14],data[18],data[1],data[5],data[9],data[13],data[17],data[0],data[4],data[8],data[12],data[16]]
        print(data2)
        # print(data[0])
        # https://leds-ee136-default-rtdb.firebaseio.com/
        myDB = firebase.FirebaseApplication("https://leds-ee136-default-rtdb.firebaseio.com/",None)
        
        myDB.put('','image1',data2)
        

    return render(request, 'upload.html', context)













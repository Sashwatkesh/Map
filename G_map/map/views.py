from django.shortcuts import render, redirect
import folium
from . models import *
import geocoder
from.forms import SearchForm
from django.http import HttpResponse

# Create your views here.
def index(request):
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SearchForm()
    address = Search.objects.all().last()
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    if lat == None or lng == None:
        address.delete()
        return HttpResponse('Invalid Location')
    m = folium.Map(location=[19, -12], zoom_start=2)


    folium.Marker([lat,lng], tooltip='Click for more',popup=country).add_to(m)
    m = m._repr_html_()
    contex = {
        'm':m,
        'form':form

    }

    return render(request,'index.html',contex)
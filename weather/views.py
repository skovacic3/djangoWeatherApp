from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm
import requests

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=<key>'
    city = "London"


    gapiPlace = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={} attraction&inputtype=textquery&fields=photos&key=<key>"
    gapiPlaceReq = requests.get(gapiPlace.format("London")).json()
    photoRef = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=1200&photoreference={}&key=<key>".format(gapiPlaceReq["candidates"][0]["photos"][0]["photo_reference"])
    

    error = None
    if request.method == "POST":
        #print(request.POST["name"])
        cr = requests.get(url.format(request.POST["name"])).json()
        if(cr["cod"] == 200):
            alreadyExists = False
            for c in City.objects.all():
                #print("{} ... {}".format(c, request.POST["name"]))
                if(str(c).lower() == request.POST["name"].lower()):
                    alreadyExists = True
                    error = "City already added."
                    break
            if not alreadyExists:
                form = CityForm(request.POST)
                form.save()
        else:
            error = "This city does not exist."
            #print("Grad ne postoji")
  
    cities = City.objects.all()
    #print(cities)

    cities_weather = []
    form = CityForm()

    """
    city_weather1 = {
            'city': 'Zagreb',
            'temperature': 27,
            'description': 'cloudy',
            'icon': '01d',
            "photo": photoRef
        }
    city_weather2 = {
            'city': 'Tokyo',
            'temperature': 27,
            'description': 'sunny',
            'icon': '01d',
            "photo": photoRef
        }

    cities_weather.append(city_weather1)
    cities_weather.append(city_weather2)
    """
    for city in cities:
        r = requests.get(url.format(city)).json()

        gapiPlace = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=photos&key=<key>"
        gapiPlaceReq = requests.get(gapiPlace.format(city.name)).json()
        photoRef = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=1200&photoreference={}&key=<key>".format(gapiPlaceReq["candidates"][0]["photos"][0]["photo_reference"])

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'photo': photoRef
        }

        cities_weather.append(city_weather)
    

    context = {'cities_weather': cities_weather, 'form': form, 'errors': error}
    return render(request, "weather/city_widget.html", context)

def specific_city(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=<key>'
    city = request.GET.get('city', 'Title')

    r = requests.get(url.format(city)).json()

    gapiPlace = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=photos&key=<key>"
    gapiPlaceReq = requests.get(gapiPlace.format(city)).json()
    photoRef = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=1600&photoreference={}&key=<key>".format(gapiPlaceReq["candidates"][0]["photos"][0]["photo_reference"])

    city_weather = {
            'city': city,
            'temperature': r['main']['temp'],
            'feels_like' : r['main']['feels_like'],
            'temp_min': r['main']['temp_min'],
            'temp_max': r['main']['temp_max'],
            'pressure': r['main']['pressure'],
            'humidity': r['main']['humidity'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'wind_speed': r['wind']['speed'],
            'photo': photoRef
        }
    context = {'city_weather': city_weather}
    return render(request, "weather/city.html", context)

def delete_city(request):
    city = request.GET.get('city_name', '')
    City.objects.get(name=city).delete()
    return redirect('index')
    
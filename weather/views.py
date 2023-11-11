from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SearchForm
import os, requests, datetime
from django.contrib.auth.decorators import login_required
from .models import Location
from django.contrib import messages

# Create your views here.
def index(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # get city name
            city = form.cleaned_data['city_name']
            data = request_by_city(city)
            if data == 404:
                messages.add_message(request, messages.INFO, f'City "{city} not found!"')
                return redirect('index')
            r = deserialize(data)
            form = SearchForm()
            context = {
                'form': form,
                'data': r
            }
            return render(request, 'weather/index.html', context)
    else:
        form = SearchForm()
    return render(request, 'weather/index.html', {'form': form})

@login_required
def my_locations(request):
    # Return previously added locations by user
    locations_objects = Location.objects.filter(user_id=request.user)
    locations = serialize_objects(locations_objects)

    return render(request, 'weather/my_locations.html', {'locations': locations})

@login_required
def add_location(request):
    # Add location to DB 
    if request.method == 'POST':
        user = request.user
        city = request.POST.get('city')
        lon = request.POST.get('lon')
        lat = request.POST.get('lat')
        location, created = Location.objects.get_or_create(
            name = city,
            user_id = user,
            lattitude = lat,
            longitude = lon
        )
        print(location)
        if created:
            messages.add_message(request, messages.INFO, f'Location "{city}" added!')
            # return render(request, 'weather/my_locations.html')
            return redirect('index')
        elif location:
            messages.add_message(request, messages.INFO, f'Location "{city}" already exist!')
            # return render(request, 'weather/my_locations.html')
            return redirect('index')
        
@login_required
def delete_location(request, name):
    # Del location from DB 
    try:
        obj = Location.objects.get(name=name).delete()
        messages.add_message(request, messages.INFO, f'Location {name} deleted!')
        print(obj)
        return redirect('my_locations')
    except:
        messages.add_message(request, messages.ERROR, f'Location {name} does not exist!')
        return redirect('my_locations')

@login_required
def location_view(request, name):
    data = request_by_city(name)
    r = deserialize(data)
    context = {
        'data':r
    }
    return render(request, 'weather/location_view.html', context)

def serialize_objects(objects):
    result = []
    for obj in objects:
        result.append(obj)
    return result

def deserialize(data):
    result = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'weather': data['weather'][0]['main'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'date_time': datetime.datetime.fromtimestamp(data['dt']),
        'lon': data['coord']['lon'],
        'lat': data['coord']['lat'],
        }
    print(len(result))
    return result

def request_by_city(city):
    API_KEY = os.getenv('API_KEY')
    unit = 'metric'
    # url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}' # by coordinates
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units={unit}&appid={API_KEY}' # by city name
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        return e.response.status_code
    
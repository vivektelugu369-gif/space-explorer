from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from .models import *
import os
from dotenv import load_dotenv


def home(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date and start_date > end_date:
        messages.error(request,'End date cannot be earlier than start date!')
        return redirect('home')

    url = "https://science.nasa.gov/wp-json/wp/v2/apod-basic"

    params = {
        'api_key': os.getenv('NASA_API_KEY')
    }

    if start_date and end_date:
        params['start_date'] = start_date
        params['end_date'] = end_date

    pictures = []

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        print(start_date)
        print(end_date)
        print("Nasa returned dates:",[p.get('date') for p in data]
              if isinstance(data, list) else data)

        print("NASA STATUS:", response.status_code)
        print("NASA RESPONSE TYPE:", type(data).__name__)

        if isinstance(data, list):
            pictures = data
            if start_date and end_date:
                pictures = [
                    picture for picture in pictures
                    if start_date <= picture.get('date','') <= end_date
                ]
        elif isinstance(data, dict):
            if 'date' in data and 'url' in data:
                pictures = [data]
            else:
                print("NASA API MESSAGE:", data)

        print("Number of pictures:", len(pictures))
        for picture in pictures:
            print("DATE:", picture.get('date'))
            print("TITLE:", picture.get('title'))
            print("MEDIA TYPE:", picture.get('media_type'))
            print("IMAGE URL:", picture.get('hdurl'))
            print("NORMAL URL:", picture.get('url'))
            print("-" * 50)

    except requests.exceptions.Timeout:
        messages.error(request,'NASA API request timed out,please try again')
    except requests.exceptions.ConnectionError:
        messages.error(request,"Unable to connect .Check your internet connection")
    except requests.exceptions.RequestException as error:
        messages.error(request,"Something went wrong while fetching NASA pictures")
    except ValueError:
        messages.error(request,"Invalid response received from NASA API")

    saved_favourite_date = set()
    if request.user.is_authenticated:
        saved_favourite_date = { date.isoformat()
                                for date in Favourites.objects.filter(user=request.user).values_list('date',flat=True)}

    return render(request, 'home.html', {
        'pictures': pictures,
        'start_date': start_date,
        'end_date': end_date,
        'saved_favourite_date':saved_favourite_date
    })

@login_required
def add_favourate(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        image_url = request.POST.get('image_url')
        explanation = request.POST.get('explanation')

        favorite, created = Favourites.objects.get_or_create(
            user = request.user,
            title = title,
            date = date,
            defaults = {'image_url':image_url,
                       'explanation':explanation}
        )
        if created:
            messages.success(request,'Picture added to favourates!')
        else:
            messages.error(request,'this picture is already in your favourates')
    return redirect('home')

@login_required
def my_favourates(request):
    favourites = Favourites.objects.filter(user=request.user).order_by('-date')
    return render(request,'my_favourates.html',{'favourites':favourites})

@login_required
def remove_favourate(request, id):
    if request.method == 'POST':
        favourite = get_object_or_404(Favourites, id=id, user=request.user)
        favourite.delete()
        messages.success(request, 'Picture removed from favourites!')
    return redirect('my_favourates')

def about(request):
    return render(request,'about.html')

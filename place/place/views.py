from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, get_list_or_404
from place.models import Place, Open, Review, Highlights, Question
from django.core.paginator import Paginator
from .helpers import *
from django.http import Http404
from django.db.models import Q
from django.db.models import F
from django.db.models import Avg
import datetime
import arrow
from .forms import ReviewForm

def index(request):
    cities = Place.objects.order_by('city').values('city').distinct()
    categories = Place.objects.filter(city__isnull=False, category__isnull=False).values('city', 'category') \
        .order_by('category', 'city').distinct()
    paginator = Paginator(categories, 50)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    ratings = Place.objects.order_by('rating').values('rating').distinct()
    data = {'cities': cities, 'categories': page.object_list, 'ratings': ratings, 'page': page}

    return render(request, 'place/index.html', context=data)


def city(request, city_name):
    places = get_list_or_404(Place, city=city_name)
    paginator = Paginator(places, 50)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    city = []
    region = []
    if places:
        city = places[0].city
        region = places[0].region
    categories = Place.objects.filter(city=city_name).order_by('category').values('category').distinct()
    services = Place.objects.filter(city=city_name).order_by('services').values('services').distinct()

    # Comma separation
    serv = split_list(services, 'services')

    data = {'city': city, 'region': region, 'categories': categories, 'services': serv,
            'page': page, 'places': page.object_list, 'page_number': page_num}

    return render(request, 'place/city.html', context=data)


def get_cat(request, city_name):
    places = Place.objects.filter(city=city_name)
    city = places[0].city
    region = places[0].region
    categories = Place.objects.filter(city=city_name).order_by('category').values('category').distinct()

    data = {'places': places, 'city': city, 'region': region, 'categories': categories}

    return render(request, 'place/get_cat.html', context=data)


def category(request, city_name, category_name):
    places = Place.objects.filter(city=city_name, category=category_name)
    if not places:
        raise Http404
    places_all = places

    # Apply filters to get businesses
    r_list = request.GET.getlist('price[]')
    places = q_filter(r_list, places, 'price')

    r_list = request.GET.getlist('atmosphere[]')
    places = q_filter(r_list, places, 'atmosphere__icontains')

    r_list = request.GET.getlist('crowd[]')
    places = q_filter(r_list, places, 'crowd__icontains')

    r_list = request.GET.getlist('accessibility[]')
    places = q_filter(r_list, places, 'accessibility__icontains')

    r_list = request.GET.getlist('planning[]')
    places = q_filter(r_list, places, 'planning__icontains')

    r_list = request.GET.getlist('payments[]')
    places = q_filter(r_list, places, 'payments__icontains')

    r_list = request.GET.getlist('services[]')
    places = q_filter(r_list, places, 'services__icontains')

    open_now = request.GET.getlist('open_now[]')
    if open_now:
        open_list = []
        # time_now = datetime.datetime.today()
        time_now = arrow.now('Europe/Berlin')
        week_n = time_now.isoweekday()
        week_s = week_of_number(week_n)
        open_time = Open.objects.filter(day=week_s, place__in=places).values('place', 'open_interval')
        open_list = list(open_time)
        open_ids = check_open(open_list)
        # We will remove the closed places
        places = places.filter(id__in=open_ids)


    # Pass all unique buttons for filtering
    region = places_all[0].region
    services = places_all.order_by('services').values('services').distinct()
    # Comma separation
    services = split_list(services, 'services')
    price = places_all.order_by('price').values('price').distinct()
    price = to_list(price, 'price')

    atmosphere = places_all.order_by('atmosphere').values('atmosphere').distinct()
    atmosphere = split_list(atmosphere, 'atmosphere')

    crowd = places_all.order_by('crowd').values('crowd').distinct()
    crowd = split_list(crowd, 'crowd')

    accessibility = places_all.order_by('accessibility').values('accessibility').distinct()
    accessibility = split_list(accessibility, 'accessibility')

    planning = places_all.order_by('planning').values('planning').distinct()
    planning = split_list(planning, 'planning')

    payments = places_all.order_by('payments').values('payments').distinct()
    payments = split_list(payments, 'payments')

    data = {'places': places, 'services': services, 'city': city_name, 'category': category_name,
            'region': region, 'price': price,
            'atmosphere': atmosphere, 'crowd': crowd, 'accessibility': accessibility, 'planning': planning,
            'payments': payments}
    return render(request, 'place/category.html', context=data)


def business(request, city_name, category_name, business_name):

    place = Place.objects.filter(city=city_name, category=category_name, business_names=business_name).first()

    reviews = Review.objects.filter(place=place.pk)
    open_time = Open.objects.filter(place=place.pk)
    highlights = Highlights.objects.filter(place=place.pk)
    hg_slides = list(highlights.values(image=F('product_picture'), title=F('food_name')))
    questions = Question.objects.filter(place=place.pk)
    data = {'p': place, 'reviews': reviews, 'open_time': open_time,
            'highlights': highlights, 'questions': questions, 'hg_slides': hg_slides}

    if not place:
        raise Http404

    if request.method == 'GET':
        form = ReviewForm()
        data = {**data, **{'form': form}}
        return render(request, 'place/business.html', context=data)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        data = {**data, **{'form': form}}
        if form.is_valid():
            saving = form.save(commit=False)
            saving.place_id = place.pk
            saving.clean()
            try:
                saving.save()
            except IntegrityError as e:
                form.add_error('', 'Error! ' + str(e))
                return render(request, 'place/business.html', context=data)
            data = {**data, **{'form': form}}
            data = {**data, **{'send': 'ok'}}
            place.review = len(reviews)
            print(reviews.aggregate(Avg('rating_stars')))
            place.rating = round(reviews.aggregate(Avg('rating_stars'))['rating_stars__avg'], 1)
            place.save()
            return render(request, 'place/business.html', context=data)
        else:
            return render(request, 'place/business.html', context=data)


'''
Access by ID place/id
def get_place(request, pk):
    place = Place.objects.get(pk=pk)

    reviews = Review.objects.filter(place=place.pk)
    open_time = Open.objects.filter(place=place.pk)
    highlights = Highlights.objects.filter(place=place.pk)
    hg_slides = list(highlights.values(image=F('product_picture'), title=F('food_name')))
    questions = Question.objects.filter(place=place.pk)
    data = {'p': place, 'reviews': reviews, 'open_time': open_time,
            'highlights': highlights, 'questions': questions, 'hg_slides': hg_slides}

    if not place:
        raise Http404

    if request.method == 'GET':
        form = ReviewForm()
        data = {**data, **{'form': form}}
        return render(request, 'place/business.html', context=data)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        data = {**data, **{'form': form}}
        if form.is_valid():
            saving = form.save(commit=False)
            saving.place_id = place.pk
            saving.clean()
            try:
                saving.save()
            except IntegrityError as e:
                form.add_error('', 'Error! ' + str(e))
                return render(request, 'place/business.html', context=data)
            data = {**data, **{'form': form}}
            data = {**data, **{'send': 'ok'}}
            place.review = len(reviews)
            print(reviews.aggregate(Avg('rating_stars')))
            place.rating = round(reviews.aggregate(Avg('rating_stars'))['rating_stars__avg'], 1)
            place.save()
            return render(request, 'place/business.html', context=data)
        else:
            return render(request, 'place/business.html', context=data)
'''
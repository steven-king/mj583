from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse

from . import models


def home(request):
    return render(request, "winners/home.html", {
        'winners': models.Winner.objects.all(),
        'countries': models.Country.objects.all(),
        'categories': models.Category.objects.all(),
        'genders': models.GENDER_CHOICES,
    })


def list_winners(request):
    filter_by = request.GET.get('filter')
    filter_val = request.GET.get('val')
    filter_breadcrumb_name = None
    filter_breadcrumb_url = None
    
    objects = models.Winner.objects.all()

    if filter_by and filter_val:
        if filter_by == 'country':
            objects = objects.filter(country__name__iexact=filter_val)
            filter_breadcrumb_name = "Countries"
            filter_breadcrumb_url = reverse("winners:countries-list")
        if filter_by == 'category':
            objects = objects.filter(category__name__iexact=filter_val)
            filter_breadcrumb_name = "Categories"
            filter_breadcrumb_url = reverse("winners:categories-list")

    return render(request, "winners/list.html", {
        "list_type": "Winners",
        "objects": objects,
        "filter_by": filter_by,
        "filter_val": filter_val,
        "filter_breadcrumb_name": filter_breadcrumb_name,
        "filter_breadcrumb_url": filter_breadcrumb_url,
    })


def list_countries(request):
    return render(request, "winners/list.html", {
        "list_type": "Countries",
        "filter_by": "country",
        "objects": models.Country.objects.all()
    })


def list_categories(request, name=None):
    objects = models.Category.objects.all()
    if name:
        objects = objects.filter(name=name)
    return render(request, "winners/list.html", {
        "list_type": "Categories",
        "filter_by": "category",
        "objects": objects,
    })


def category_winners(request, category):
    category = get_object_or_404(models.Category, name=category)
    return render(request, "winners/category_winners.html", {
        "category": category,
        "objects": category.winner_set.all(),
    })


def api(request):
    category = request.GET.get('category')
    country = request.GET.get('country')
    gender = request.GET.get('gender')
    
    winners = models.Winner.objects.select_related('category', 'country', 'person')

    if category:
        winners = winners.filter(category__name=category)
    
    if country:
        winners = winners.filter(country__name=country)
    
    if gender:
        winners = winners.filter(person__gender=gender)
    
    data = {"winners": [w.to_json() for w in winners]}

    return JsonResponse(data)
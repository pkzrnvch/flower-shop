from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from flower_shop_app.models import FlowerBouquet


def index(request):
    bouquets = FlowerBouquet.objects.filter(availability=True).order_by('-created')[:3]
    return render(
        request,
        'flower_shop_app/index.html',
        context={
            'recommended_bouquets': bouquets,
        }
    )


def catalog(request):
    bouquet_list = FlowerBouquet.objects.filter(availability=True)

    bouquets_per_page = 6
    paginator = Paginator(bouquet_list, bouquets_per_page)
    page_number = request.GET.get('page', 1)

    try:
        bouquets = paginator.page(page_number)
    except PageNotAnInteger:
        bouquets = paginator.page(1)
    except EmptyPage:
        bouquets = paginator.page(paginator.num_pages)

    return render(
        request,
        'flower_shop_app/catalog.html',
        context={
            'bouquets': bouquets,
        }
    )

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


from flower_shop_app.forms import ConsultationRequestForm
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


def consultation(request):
    return render(
        request,
        'flower_shop_app/consultation.html',
        context={'form': ConsultationRequestForm()}
    )


@require_http_methods(['POST'])
def create_consultation_request(request):
    form = ConsultationRequestForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            'flower_shop_app/consultation.html',
            {'form': form}
        )

    form.save()
    return redirect('flower_shop_app:index')

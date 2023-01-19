from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
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
            'consultation_form': ConsultationRequestForm(),
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
            'consultation_form': ConsultationRequestForm(),
        }
    )


def consultation(request):
    form = ConsultationRequestForm()

    consultation_form_data = request.session.get('consultation_form_data')
    if consultation_form_data:
        form = ConsultationRequestForm(consultation_form_data)
        del request.session['consultation_form_data']

    return render(
        request,
        'flower_shop_app/consultation.html',
        context={'consultation_form': form}
    )


@require_http_methods(['POST'])
def create_consultation_request(request):
    form = ConsultationRequestForm(request.POST)

    if not form.is_valid():
        request.session['consultation_form_data'] = request.POST
        return redirect('flower_shop_app:consultation')

    form.save()

    page_url_which_request_was_made = request.META.get('HTTP_REFERER', '/')
    if page_url_which_request_was_made == request.build_absolute_uri(reverse('flower_shop_app:consultation')):
        return redirect('flower_shop_app:index')

    return redirect(page_url_which_request_was_made)

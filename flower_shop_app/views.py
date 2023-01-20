import random

from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect


from flower_shop_app.forms import ConsultationRequestForm
from flower_shop_app.models import FlowerBouquet, EventTag


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

    messages.success(request, 'Вы успешно записались на консультацию. Мы скоро перезвоним')

    page_url_which_request_was_made = request.META.get('HTTP_REFERER', '/')
    if page_url_which_request_was_made == request.build_absolute_uri(reverse('flower_shop_app:consultation')):
        return redirect('flower_shop_app:index')

    return redirect(page_url_which_request_was_made)


def quiz_step_1(request):
    event_tags = EventTag.objects.all()
    event_tag_id = request.GET.get('event_tag_id', None)
    if event_tag_id:
        request.session['event_tag_id'] = event_tag_id
        return redirect('flower_shop_app:quiz_step_2')
    return render(
        request,
        'flower_shop_app/quiz-1.html',
        context={'event_tags': event_tags}
    )


def quiz_step_2(request):
    if not request.session.get('event_tag_id', None):
        return redirect('flower_shop_app:quiz_step_1')
    bouquet_price_range = request.GET.get('bouquet_price_range', None)
    if bouquet_price_range:
        request.session['bouquet_price_range'] = bouquet_price_range
        return redirect('flower_shop_app:quiz_result')
    return render(
        request,
        'flower_shop_app/quiz-2.html',
    )


def quiz_result(request):
    event_tag_id = request.session.pop('event_tag_id', None)
    price_range = request.session.pop('bouquet_price_range', None)
    if not event_tag_id or not price_range:
        return redirect('flower_shop_app:quiz_step_1')
    bouquets = FlowerBouquet.objects.filter(availability=True)
    if event_tag_id != 'no_tag':
        bouquets = bouquets.filter(event_tags__id=event_tag_id)
    if price_range == 'less_than_1000':
        bouquets = bouquets.filter(price__lt=1000)
    elif price_range == 'from_1000_to_5000':
        bouquets = bouquets.filter(price__gte=1000).filter(price__lt=5000)
    elif price_range == 'more_than_5000':
        bouquets = bouquets.filter(price__gte=5000)
    bouquet_to_show = random.choice(list(bouquets.prefetch_related('flowers')))
    composition = bouquet_to_show.flower_bouquet_items.all().select_related('flower')
    bouquet_to_show.composition = ' ,'.join(
        f'{item.flower.name} - {item.flower_quantity} шт.' for item in composition
    )
    return render(
        request,
        'flower_shop_app/quiz-result.html',
        context={
            'bouquet': bouquet_to_show,
            'consultation_form': ConsultationRequestForm(),
        }
    )

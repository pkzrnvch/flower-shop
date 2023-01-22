import random
import uuid

from django.contrib import messages
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render, redirect
from yookassa import Payment

from flower_shop_app.forms import ConsultationRequestForm, OrderForm
from flower_shop_app.models import (FlowerBouquet,
                                    EventTag,
                                    FlowerBouquetAttributeItem,
                                    FlowerBouquetItem,
                                    Order)


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

    bouquets_per_page = 3
    paginator = Paginator(bouquet_list, bouquets_per_page)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if request.htmx:
        return render(
            request,
            'flower_shop_app/partials/category_bouquets.html',
            {
                'page_obj': page_obj,
            }
        )

    return render(
        request,
        'flower_shop_app/catalog.html',
        context={
            'page_obj': page_obj,
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

    price_ranges = {
        'less_than_1000': lambda bqts: bqts.filter(price__lt=1000),
        'from_1000_to_5000': lambda bqts: bqts.filter(price__gte=1000, price__lt=5000),
        'more_than_5000': lambda bqts: bqts.filter(price__gte=5000),
        'any': lambda bqts: bqts,
    }
    bouquets = price_ranges[price_range](bouquets)

    if not bouquets.exists():
        messages.info(request, 'К сожалению, мы не смогли подобрать для Вас букет. Попробуйте снова.')
        return redirect('flower_shop_app:quiz_step_1')

    bouquet_to_show = random.choice(list(bouquets.prefetch_related('flowers')))
    composition = bouquet_to_show.flower_bouquet_items.all().select_related('flower')
    bouquet_to_show.composition = ' ,'.join(
        f'{item.flower.name} - {item.flower_quantity} шт.' for item in composition
    )
    return render(
        request,
        'flower_shop_app/quiz_result.html',
        context={
            'bouquet': bouquet_to_show,
            'consultation_form': ConsultationRequestForm(),
        }
    )


def bouquet_detail(request, bouquet_id):
    bouquet = get_object_or_404(FlowerBouquet, id=bouquet_id)
    bouquet_flowers = FlowerBouquetItem.objects\
        .filter(flower_bouquet_id=bouquet.id)\
        .prefetch_related('flower')
    bouquet_attributes = FlowerBouquetAttributeItem.objects\
        .filter(flower_bouquet_id=bouquet.id)\
        .prefetch_related('flower_bouquet_attribute')

    return render(
        request,
        'flower_shop_app/bouquet_detail.html',
        {
            'bouquet': bouquet,
            'bouquet_flowers': bouquet_flowers,
            'bouquet_attributes': bouquet_attributes,
            'consultation_form': ConsultationRequestForm(),
        }
    )


def order(request, bouquet_id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            bouquet = FlowerBouquet.objects.get(id=bouquet_id)
            request.session['order_in_process'] = {
                'bouquet_id': bouquet_id,
                'bouquet_price': f'{bouquet.price}',
                'client_name': form.cleaned_data['client_name'],
                'phone_number': form.cleaned_data['phone_number'].as_e164,
                'address': form.cleaned_data['address'],
                'delivery_time': form.cleaned_data['delivery_time'],
            }
            print(request.session['order_in_process'])
            return redirect('flower_shop_app:payment')
    else:
        form = OrderForm()
    return render(
        request,
        'flower_shop_app/order.html',
        context={
            'order_form': form,
        }
    )


def order_payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number', None)
        card_month = request.POST.get('card_month', None)
        card_year = request.POST.get('card_year', None)
        card_cvc = request.POST.get('card_cvc', None)
        card_name = request.POST.get('card_name', None)
        client_email = request.POST.get('email', None)
        order_details = request.session.get('order_in_process', None)
        if not any([card_number, card_month, card_year, card_cvc, card_name]):
            return render(
                request,
                'flower_shop_app/payment.html',
            )
        if not order_details:
            return redirect('flower_shop_app:catalog')
        if len(card_year) == 2:
            card_year = f'20{card_year}'

        idempotence_key = str(uuid.uuid4())
        payment = Payment.create(
            {
                'amount': {
                    'value': str(order_details['bouquet_price']),
                    'currency': 'RUB'
                },
                'payment_method_data': {
                    'type': 'bank_card',
                    'card': {
                        'number': card_number,
                        'expiry_year': card_year,
                        'expiry_month': card_month,
                        'csc': card_cvc,
                        'cardholder': card_name
                    }
                },
                'confirmation': {
                    'type': 'redirect',
                    'return_url': request.build_absolute_uri(reverse('flower_shop_app:payment_confirmation'))
                },
                'capture': True,
                'description': 'Оплата: букет цветов'
            }, idempotence_key
        )
        confirmation_url = payment.confirmation.confirmation_url
        request.session['payment_id'] = payment.id
        request.session['order_in_process']['email'] = client_email
        return redirect(confirmation_url)

    return render(
        request,
        'flower_shop_app/payment.html',
    )


def order_payment_confirmation(request):
    payment_id = request.session.get('payment_id', None)
    order_details = request.session.get('order_in_process', None)
    bouquet = FlowerBouquet.objects.get(id=order_details['bouquet_id'])
    if not payment_id:
        return redirect('flower_shop_app:index')
    payment = Payment.find_one(payment_id)
    context = {
        'payment_status': payment.status,
        'bouquet': bouquet
    }
    if payment.status == 'succeeded':
        order_details = request.session.get('order_in_process', None)
        new_order = Order(
            client_name=order_details['client_name'],
            phone_number=order_details['phone_number'],
            address=order_details['address'],
            delivery_time=order_details['delivery_time']
        )
        if order_details['email']:
            new_order.email = order_details['email']
        new_order.save()
        context['order'] = new_order
        request.session.pop('payment_id', None)
        request.session.pop('order_in_process', None)
    return render(
        request,
        'flower_shop_app/payment_confirmation.html',
        context=context
    )


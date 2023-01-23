from django.urls import path

from flower_shop_app import views

app_name = 'flower_shop_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('consultation/', views.consultation, name='consultation'),
    path('create_consultation/', views.create_consultation_request, name='created_consultation'),
    path('quiz/step1/', views.quiz_step_1, name='quiz_step_1'),
    path('quiz/step2/', views.quiz_step_2, name='quiz_step_2'),
    path('quiz/step3/', views.quiz_step_3, name='quiz_step_3'),
    path('quiz/result/', views.quiz_result, name='quiz_result'),
    path('bouquet/<int:bouquet_id>/', views.bouquet_detail, name='bouquet_detail'),
    path('order/<int:bouquet_id>/', views.order, name='order'),
    path('payment/', views.order_payment, name='payment'),
    path('payment/confirmation', views.order_payment_confirmation, name='payment_confirmation'),
]

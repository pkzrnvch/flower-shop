from django import forms

from flower_shop_app.models import ConsultationRequest, Order


class ConsultationRequestForm(forms.ModelForm):

    class Meta:
        model = ConsultationRequest
        fields = ['name', 'phone_number', 'acceptance_of_rules']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'order__form_input',
            'placeholder': 'Введите Имя',
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'order__form_input',
            'placeholder': '+ 7 (999) 000 00 00',
        })
        self.fields['acceptance_of_rules'].widget.attrs.update({
            'class': 'singUpConsultation__ckekbox',
        })

    def clean_acceptance_of_rules(self):
        if not self.cleaned_data['acceptance_of_rules']:
            raise forms.ValidationError('Вы должны согласиться с правилами')
        return self.cleaned_data['acceptance_of_rules']


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['client_name', 'phone_number', 'address', 'delivery_time']
        widgets = {
            'delivery_time': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client_name'].widget.attrs.update({
            'class': 'order__form_input',
            'placeholder': 'Введите Имя',
        })
        self.fields['client_name'].label = ""
        self.fields['phone_number'].widget.attrs.update({
            'class': 'order__form_input',
            'placeholder': '+ 7 (999) 000 00 00',
        })
        self.fields['phone_number'].label = ""
        self.fields['address'].widget.attrs.update({
            'class': 'order__form_input',
            'placeholder': 'Адрес доставки',
        })
        self.fields['address'].label = ""
        self.fields['delivery_time'].widget.attrs.update({
            'class': 'order__form_radio',
        })

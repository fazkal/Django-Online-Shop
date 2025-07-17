from accounts.models import Profile
from shop.models import ProductModel
from django.contrib.auth import forms as auth_forms
from django import forms
from django.utils.translation import gettext_lazy as _


class AdminPasswordChangeForm(auth_forms.PasswordChangeForm):

    error_messages = {

        "password_incorrect": _(
            "رمز عبور فعلی که وارد کردید اشتباه می باشد."
        ),
        "password_mismatch": _(
            "رمز عبور جدید با تکرار آن مطابقت ندارد."
        ),
    }

    
class AdminProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'phone_number'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control text-center'


class AdminProductEditeForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = [
            'category',
            'title', 
            'slug', 
            'image',
            'description',
            'brief_description',
            'stock',
            'status',
            'price',
            'discount_percent',
        ]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['brief_description'].widget.attrs['class'] = 'form-control'
        #self.fields['stock'].widget.attrs['class'] = 'number'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        #self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['discount_percent'].widget.attrs['class'] = 'form-control'
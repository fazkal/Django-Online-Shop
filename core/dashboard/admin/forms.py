from accounts.models import Profile
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
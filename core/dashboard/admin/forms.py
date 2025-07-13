from django.contrib.auth import forms as auth_forms
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

    
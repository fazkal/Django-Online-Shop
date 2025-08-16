from django import forms
from .models import ReviewModels
from shop.models import ProductModel,ProductStatusType


class SubmitReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModels
        fields = ['product','rate','description']
        error_messages = {
            'description':{
                'required':'فیلد توضیحات اجباری ست.',
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')

        try:
            ProductModel.objects.get(
                id=product.id,status=ProductStatusType.publish.value)
        except ProductModel.DoesNotExist:
            raise forms.ValidationError('این محصول وجود ندارد.')
        return cleaned_data
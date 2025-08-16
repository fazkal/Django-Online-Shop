from django.contrib import admin
from .models import ReviewModels

# Register your models here.

@admin.register(ReviewModels)
class ReviewModelsAdmin(admin.ModelAdmin):
    list_display = ('id','user','product','rate','created_date')
from django.contrib import admin

from .models import Frequency, FrequencyDetail, FrequencyTitle

# Register your models here.
admin.site.register(Frequency)
admin.site.register(FrequencyTitle)
admin.site.register(FrequencyDetail)

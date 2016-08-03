from django.contrib import admin

from .forms import BugReportForm
from .models import Attachment, BugCategory, BugReport


class BugReportAdmin(admin.ModelAdmin):

    form = BugReportForm
    exclude = ('created', 'updated')
    list_display = ('__str__', 'category', 'status', 'is_solved', 'submitter', 'severity')
    list_filter = ('category', 'status', 'is_solved', 'severity')
    ordering = ('-created',)
    search_fields = ('title', 'project', 'description', 'reproduce', 'actual', 'expected', 'submitter')


# Register your models here.
admin.site.register(BugCategory)
admin.site.register(BugReport, BugReportAdmin)
admin.site.register(Attachment)

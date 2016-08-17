from django.contrib import admin

from .forms import BugReportForm
from .models import Attachment, BugCategory, BugReport


class BugReportAdmin(admin.ModelAdmin):
    """The admin site interface of the `BugReport` model."""

    form = BugReportForm
    exclude = ('created', 'updated')
    list_display = ('id', 'title', 'category', 'status', 'severity', 'submitter')
    list_display_links = ('id', 'title')
    list_filter = ('category', 'severity', 'status')
    ordering = ('-created',)
    search_fields = ('title', 'reproduce', 'actual', 'expected', 'submitter')


# Register your models here.
admin.site.register(BugCategory)
admin.site.register(BugReport, BugReportAdmin)
admin.site.register(Attachment)

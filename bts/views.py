from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import View


class Home(View):

    def get(self, request):
        return redirect('bugs_list')


def get_status(s):
    if s == 'New':
        return 0
    elif s == 'Rejected':
        return 1
    elif s == 'Assigned':
        return 2
    elif s == 'Fixed':
        return 3


def get_severity(s):
    if s == 'Feature':
        return 0
    elif s == 'Low':
        return 1
    elif s == 'Normal':
        return 2
    elif s == 'High':
        return 3
    elif s == 'Urgent':
        return 4


def fill(request):
    import csv
    from bugs.models import BugCategory, BugReport
    from django.contrib.auth.models import User

    with open(settings.BASE_DIR + "/ent.csv") as f:
        reader = csv.reader(f)
        data = [row for row in reader]

        for row in data[1:]:
            bug = BugReport(title=row[1], os=row[2], ram=row[3], vram=row[4], submitter=User.objects.get(username='admin'),
                            category=BugCategory.objects.get(name=row[5]), severity=get_severity(row[6]), status=get_status(row[7]),
                            actual=row[8], expected=row[9], reproduce=row[10], solution=row[12])
            bug.save()

    return redirect('/')

import csv

import bugs.signals
from bugs.models import BugCategory, BugReport
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Make sure you have user 'admin'"

    def add_arguments(self, parser):
        parser.add_argument("filename")

    def handle(self, *args, **options):
        # Clear the bug reports
        BugReport.objects.raw('TRUNCATE bugs_bugreport CASCADE')

        # Read the CSV file
        filename = options["filename"]
        data = []
        try:
            with open(filename) as f:
                for row in csv.reader(f):
                    data.append(row)
        except FileNotFoundError:
            print("File not found!")
            return

        # Helper functions
        user = User.objects.get(username="admin")

        def cat(name):
            return BugCategory.objects.get_or_create(name=name)[0]

        def stat(s):
            if s == "New":
                return BugReport.STATUS_NEW
            elif s == "Rejected":
                return BugReport.STATUS_REJECTED
            elif s == "Assigned":
                return BugReport.STATUS_ASSIGNED
            elif s == "Fixed":
                return BugReport.STATUS_FIXED
            else:
                raise ValueError("Invalid status name = " + s)

        def sev(s):
            if s == "Feature":
                return BugReport.SEVERITY_FEATURE
            elif s == "Low":
                return BugReport.SEVERITY_LOW
            elif s == "Normal":
                return BugReport.SEVERITY_NORMAL
            elif s == "High":
                return BugReport.SEVERITY_HIGH
            elif s == "Urgent":
                return BugReport.SEVERITY_URGENT
            else:
                raise ValueError("Invalid severity name = " + s)

        def mast(title):
            try:
                master = BugReport.objects.get(title=title)
            except:
                master = None
            return master

        # 0 := ID
        # 1 := Title
        # 2 := OS
        # 3 := RAM
        # 4 := VRAM
        # 5 := Category
        # 6 := Severity
        # 7 := Status
        # 8 := Actual
        # 9 := Expected
        # 10:= Reproduce
        # 11:= Master
        # 12:= Solution

        # Do the work
        for r in data[1:]:
            bug = BugReport(
                title=r[1], os=r[2], ram=r[3], vram=r[4],
                category=cat(r[5]), severity=sev(r[6]), status=stat(r[7]),
                actual=r[8], expected=r[9], reproduce=r[10],
                master=mast(r[11]), solution=r[12],
                submitter=user, assignee=user)
            bug.save()
            print(bug)

import csv

import bugs.signals
from bugs.models import BugCategory, BugReport
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Reload bug report database from a valid CSV file ('admin' user required)"

    def add_arguments(self, parser):
        parser.add_argument("filename", help="Path to the CSV file")

    def handle(self, *args, **options):
        # Clear the bug reports
        BugReport.objects.all().delete()

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
            """Returns the category with the given name, creating a new one if required.
            """
            return BugCategory.objects.get_or_create(name=name)[0]

        def stat(name):
            """Returns the status number with the given name.
            """
            name = name.lower()
            if name == "new":
                return BugReport.STATUS_NEW
            elif name == "rejected":
                return BugReport.STATUS_REJECTED
            elif name == "assigned":
                return BugReport.STATUS_ASSIGNED
            elif name == "fixed":
                return BugReport.STATUS_FIXED
            else:
                raise ValueError("Invalid status name = " + name)

        def sev(name):
            """Returns the severity number with the given name.
            """
            name = name.lower()
            if name == "feature":
                return BugReport.SEVERITY_FEATURE
            elif name == "low":
                return BugReport.SEVERITY_LOW
            elif name == "normal":
                return BugReport.SEVERITY_NORMAL
            elif name == "high":
                return BugReport.SEVERITY_HIGH
            elif name == "urgent":
                return BugReport.SEVERITY_URGENT
            else:
                raise ValueError("Invalid severity name = " + name)

        def report(title):
            """Returns a bug report with the given title.
            """
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
        for row in data[1:]:
            r = [e.strip() for e in row]
            bug = BugReport(
                title=r[1], os=r[2], ram=r[3], vram=r[4],
                category=cat(r[5]), severity=sev(r[6]), status=stat(r[7]),
                actual=r[8], expected=r[9], reproduce=r[10],
                master=report(r[11]), solution=r[12],
                submitter=user, assignee=user)
            bug.save()
            print(bug)

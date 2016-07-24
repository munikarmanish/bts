from django.shortcuts import redirect
from django.views.generic import View


class Home(View):

    def get(self, request):
        return redirect('bugs_list')

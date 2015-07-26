
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from user_profile.models import AuthUser
from models import Harvest, EquipmentType
from forms import NewEquipment, NewHarvest

from fixtureless import Factory
import itertools
import datetime

class JsonCalendar(View):
    def get(self, request):
        harvests = Harvest.objects.all()
        event = {}
        events = []
        for harvest in harvests:
            event["title"] = harvest.title
            event["allday"] = "false"
            event["description"] = harvest.description
            event["start"] = harvest.scheduled_date
            event["end"] = harvest.end_date
            event["url"] = "http://gnu.org"
            events.append(event)
        #events = [{"title":"Free Pizza","allday":"false","borderColor":"#5173DA","color":"#99ABEA","textColor":"#000000","description":"<p>This is just a fake description for the Free Pizza.</p><p>Nothing to see!</p>","start":"2015-07-25T15:00:34","end":"2015-07-25T16:00:34","url":"http://www.mikesmithdev.com/blog/worst-job-titles-in-internet-and-info-tech/"},{"title":"DNUG Meeting","allday":"false","borderColor":"#5173DA","color":"#99ABEA","textColor":"#000000","description":"<p>This is just a fake description for the DNUG Meeting.</p><p>Nothing to see!</p>","start":"2015-07-26T15:00:34","end":"2015-07-26T16:00:34","url":"http://www.mikesmithdev.com/blog/worst-job-titles-in-internet-and-info-tech/"}]
        return(JsonResponse(events, safe=False))


# Inserting random data. TODO: move it away
class DataTest(View):
    def get(self, request):
        factory = Factory()
        count = 10
        initial = {
            'title': 'harvest title',
            'description': 'test description',
            'scheduled_date': datetime.datetime.now(),
            'end_date': datetime.datetime.now()
        }
        initial_list = list()
        for _ in itertools.repeat(None, count):
            initial_list.append(initial)
        h = factory.create(Harvest, initial_list)
        return HttpResponseRedirect('/harvests/')

class EquipmentForm(View):
    def get(self, request):
        equipment_form = NewEquipment()
        return render(request, 'form_new_equipment.html', {'form': equipment_form})

    def post(self, request):
        params = dict()
        equipment = NewEquipment(request.POST)
        new_equipment = equipment.save()
        if equipment.is_valid():
            return HttpResponseRedirect('/new_equipment/')

class HarvestForm(View):
    def get(self, request):
        harvest_form = NewHarvest()
        return render(request, 'form_new_harvest.html', {'form': harvest_form})

    def post(self, request):
        params = dict()
        harvest = NewHarvest(request.POST)
        new_harvest = harvest.save()
        if harvest.is_valid():
            return HttpResponseRedirect('/new_harvest/')

class Calendar(View):
    def get(self, request):
        params = dict()
        params["view"] = "calendar"
        return render(request, 'calendar.html', params)


class Harvests(View):
    def get(self, request):
        params = dict()
        all_harvests = Harvest.objects.all()
        params["harvests"] = all_harvests
        params["view"] = "harvests"
        return render(request, 'harvests.html', params)

class Profile(View):
    def get(self, request, username):
        params = dict()
        user = AuthUser.objects.get(username=username)
        params["user"] = user
        return render(request, 'profile.html', params)

class Index(View):
    def get(self, request):
        params = dict()
        email = None
        if request.user.is_authenticated():
            email = request.user.email
            user = AuthUser.objects.get(email=email)
            params["user"] = user
            return render(request, 'dashboard.html', params)
        else:
            return render(request, 'login.html', params)

    # Index also handles authentication from login form
    def post(self, request):
        params = dict()
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'login.html', params)
                # TODO: Return a 'disabled account' error message
        else:
            return render(request, 'login.html', params)
            # TODO: Return an 'invalid login' error message.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event

# Create your views here.

# class Event:
#     def __init__(self, name, location, address, date, time, occasion):
#         self.name = name
#         self.location = location
#         self.address = address
#         self.date = date
#         self.time = time
#         self.occasion = occasion


# events = [
#     Event('Drinks On Saturday', 'Toronto', '250 King Street', 'Nov 10', '7:00 pm', "let's meet for drinks"),
#     Event('Birthday for Laura', 'Niagara Falls', '15 main st', 'Dec 6', '5:00 pm', 'birthday party')
# ]

def home(request):
    return render(request, 'home.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid credentials - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def events_index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', { 'events': events })

def events_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/detail.html', { 'event': event })
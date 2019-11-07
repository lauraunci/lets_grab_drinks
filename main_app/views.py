from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Profile, Event
from .forms import UserUpdateForm, ProfileUpdateForm, AttendantForm

class EventCreate(CreateView):
    model = Event
    fields = ['name', 'location', 'address', 'date_time', 'occasion']
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class EventUpdate(UpdateView):
  model = Event
  fields = ['location', 'address', 'date_time']

class EventDelete(DeleteView):
  model = Event
  success_url = '/events/'

def home(request):
    return render(request, 'home.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            error_message = 'Invalid credentials - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def profile(request):
    return render(request, 'profile.html')


def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            profile = Profile.objects.create(user_id=request.user.id,
                                             phone=p_form.cleaned_data['phone'],
                                             location=p_form.cleaned_data['location'],
                                             birthday=p_form.cleaned_data['birthday'])
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'registration/profile_update.html', context)


def events_index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', {'events': events})


def events_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    attendant_form = AttendantForm()
    return render(request, 'events/detail.html', {
        'event': event, 'attendant_form': attendant_form 
    })

def add_attendant(request, event_id):
    form = AttendantForm(request.POST)
    if form.is_valid():
        new_attendant = form.save(commit=False)
        new_attendant.event_id = event_id
        new_attendant.user = request.user
        new_attendant.save()
    return redirect('detail', event_id=event_id)

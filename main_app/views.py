from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *


class EventCreate(CreateView):
    model = Event
    fields = ['name', 'location', 'address', 'date_time', 'occasion']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class EventUpdate(UpdateView):
    model = Event
    # Let's make it impossible to rename a cat :)
    fields = ['location', 'address', 'date_time']


class EventDelete(DeleteView):
    model = Event
    success_url = '/events/'


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
            return redirect('profile')
        else:
            error_message = 'Invalid credentials - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
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
    comments = Comment.objects.filter(event_id=event_id, parent=None)
    comment_form = CommentForm()
    return render(request, 'events/detail.html', {'event': event, 'comments': comments, 'comment_form': comment_form})


@login_required
def post_comment(request, event_id, parent_comment_id=None):
    event = Event.objects.get(pk=event_id)
    # print(event)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.event_id = event
            new_comment.author = request.user

            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                new_comment.parent_id = parent_comment.get_root().id
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')

            new_comment.save()
            return redirect(event)
        else:
            return HttpResponse('The form is incorrect')
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'event_id': event_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)

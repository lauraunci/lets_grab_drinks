from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile, Attendant, Comment


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'location', 'birthday']


class AttendantForm(ModelForm):
    class Meta:
        model = Attendant
        fields = ['confirmation']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

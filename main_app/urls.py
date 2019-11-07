from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('events/', views.events_index, name='index'),
    path('events/<int:event_id>/', views.events_detail, name='detail'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:event_id>/add_attendant/', views.add_attendant, name='add_attendant'),
    path('events/<int:pk>/update/',
         views.EventUpdate.as_view(), name='events_update'),
    path('events/<int:pk>/delete/',
         views.EventDelete.as_view(), name='events_delete'),
    path('events/<int:event_id>/post_comment/',
         views.post_comment, name='post_comment'),
    path('events/<int:event_id>/<int:parent>/comment_reply',
         views.post_comment, name='comment_reply')
]

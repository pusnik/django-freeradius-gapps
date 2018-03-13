from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from GApps.views import LoginView
from GApps.views import ProfileView
from GApps.views import triggerSync

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', auth_views.logout, {'next_page': '/accounts/login/'}, name='logout'),
    path('profile/', login_required(ProfileView.as_view()), name="profile"),
    path('schedule-sync/', login_required(triggerSync))
]

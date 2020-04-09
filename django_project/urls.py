"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as users_views
from users.api import views as api_user_views
from words.api import views as api_words_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as api_auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', users_views.register, name='register'),
    path('profile', users_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    # rest-api urls
    path('api/register', api_user_views.register, name='api-register'),
    path('api/login', api_auth_views.obtain_auth_token, name='api-login'),
    path('api/profileupdate', api_user_views.profile_update, name='api-profileupdate'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/words/<int:level>', api_words_views.get_words, name='api-words'),
    path('api/allwords/<int:level>', api_words_views.ApiAllWordsView.as_view(), name='api-allwords'),
    path('api/reviewedwords/<int:level>', api_words_views.ApiReviewedWordsView.as_view(), name='api-reviewedwords'),
    path('api/masteredwords/<int:level>', api_words_views.ApiMasteredWordsView.as_view(), name='api-masteredwords'),
    path('api/searchwords', api_words_views.ApiSearchWordsView.as_view(), name='api-allwords'),
    # words urls
    path('', include('words.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

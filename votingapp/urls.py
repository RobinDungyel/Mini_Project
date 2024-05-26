from django.contrib import admin
from django.urls import path
from votingapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homeView, name='home'),
    path('register/', views.registrationView, name='registration'),
    path('login/', views.loginView, name='login'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('logout/', views.logoutView, name='logout'),
    path('position/', views.positionView, name='position'),
    path('candidate/<int:pos>/', views.candidateView, name='candidate'),
    path('candidate/detail/<int:id>/', views.candidateDetailView, name='detail'),
    path('result/', views.resultView, name='result'),
    path('changepass/', views.changePasswordView, name='changepass'),
    path('editprofile/', views.editProfileView, name='editprofile'),

    # Custom admin panel URLs
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('admin_panel/add_position/', views.add_position, name='add_position'),
    path('admin_panel/edit_position/<int:id>/', views.edit_position, name='edit_position'),
    path('admin_panel/delete_position/<int:id>/', views.delete_position, name='delete_position'),
    path('admin_panel/add_candidate/', views.add_candidate, name='add_candidate'),
    path('admin_panel/edit_candidate/<int:id>/', views.edit_candidate, name='edit_candidate'),
    path('admin_panel/delete_candidate/<int:id>/', views.delete_candidate, name='delete_candidate'),
    path('admin_panel/edit_user/<int:id>/', views.edit_user, name='edit_user'),
    path('admin_panel/delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('admin_panel/update_voting_times/', views.update_voting_times, name='update_voting_times'),
    path('admin_panel/delete_voting_time/', views.delete_voting_time, name='delete_voting_time'),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('admin_panel/add_user/', views.add_user, name='add_user'),  # URL for adding user
   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register_view, login_view, logout_view, edit_profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.register_view, name='register'),
    path('tasks/', views.task_list, name='task_list_main'),
    path('create/', views.create_task, name='create_task'),
    path('base/', views.base, name='base'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/edit/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
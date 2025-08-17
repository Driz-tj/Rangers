from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views, views_api

urlpatterns = [
    path('', views.home, name='home'),
    path('fixtures/', views.fixtures, name='fixtures'),
    path('book-ticket/<int:match_id>/', views.book_ticket, name='book_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('process-payment/', views.process_payment, name='process_payment'),
    # Health checks and API endpoints
    path('health/', views_api.health_check, name='health_check'),
    path('api/status/', views_api.api_status, name='api_status'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('description/<str:id>/', views.description, name='description'),
    path('theater/<int:id>/', views.theater, name='theater'),
    path('seatselect/<int:id>/', views.seatselect, name='seatselect'),
    path('seatselected/', views.seatselected, name='seatselected'),
    path('payment/', views.payment, name='payment'),  # New payment URL
    path('history/', views.history, name='history'),
    path('logout/', views.logout_view, name='logout'),
    path('stripe_config/', views.stripe_config, name='stripe_config'),
    path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    
]
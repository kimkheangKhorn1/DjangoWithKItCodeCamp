# from django.urls import path
# from . import views

# urlpatterns = [
#   path('', views.login, name='login'),
#   path('', views.home, name='home')
  
# ]

from django.urls import path
from . import views

# app_name = 'library'

urlpatterns = [
    # home page
    path('home/', views.home, name='home'),
    # next page
    path('', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),  # Added comma here
    
    # New Adding
    path('index/', views.index, name='index'),
    path('base_generic/', views.index, name='base_generic'),
]



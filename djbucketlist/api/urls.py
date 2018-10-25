from django.urls import path, include
from .views import CreateView, DetailView

urlpatterns=[
    
    path('', CreateView.as_view(), name="create"),
    path('<int:pk>', DetailView.as_view(), name="details"),
    
]
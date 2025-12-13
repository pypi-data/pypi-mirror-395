from django.urls import path
from . import views

app_name = 'soccerpoll'
urlpatterns = [
    #This path is mapped to a view template that is mapped to a views.py file -> index method
    path("", views.IndexView.as_view(), name="index"),
    #path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:q_id>/", views.detail, name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:q_id>/vote/", views.vote, name="vote")
]
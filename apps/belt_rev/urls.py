from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add),
    url(r'^books/create$', views.addBook),
    url(r'^books/(?P<id>\d+)$', views.review),
    url(r'^addReview/(?P<id>\d+)$',views.addReview),
    url(r'^users/(?P<id>\d+)$', views.profile),
    url(r'^logout$', views.logout)
]
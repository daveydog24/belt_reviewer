from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^registration$', views.registration),
    url(r'^books/add$', views.add_book),
    url(r'^books/(?P<book_id>\d+)$', views.show_book),
    url(r'^users/(?P<user_id>\d+)$', views.show_user),
    url(r'^books$', views.books_home),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^', views.index),
]
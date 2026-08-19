from django.urls import path
from .views import add_email_to_newsletter

urlpatterns = [
    path("add/", add_email_to_newsletter, name="add_email_to_newsletter"),
]

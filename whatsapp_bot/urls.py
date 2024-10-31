from django.contrib import admin
from django.urls import path
from whatsapp_bot.views import webhook_whatsapp

urlpatterns = [
    path('webhook-whatsapp/', webhook_whatsapp, name="webhook_whatsapp")
]
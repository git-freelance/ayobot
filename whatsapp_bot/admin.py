from django.contrib import admin
from .models import WhatsAppConversation

@admin.register(WhatsAppConversation)
class WhatsAppConversationAdmin(admin.ModelAdmin):
    list_display = ['wa_id', 'message', 'response', 'content_sid', 'created_at']
    list_filter = ['wa_id', 'content_sid', 'created_at']
    search_fields = ['wa_id', 'message', 'response']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


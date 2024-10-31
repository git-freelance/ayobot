from django.db import models

# Create your models here.

class WhatsAppConversation(models.Model):
    wa_id = models.CharField(max_length=20)  # Store the WhatsApp ID
    message = models.TextField()  # Store the user's message
    response = models.TextField()  # Store the bot's response
    content_sid = models.CharField(max_length=50, null=True, blank=True)  # Store which template was used
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wa_id} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']

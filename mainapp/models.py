from django.db import models
from django.utils import timezone


class Message(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Mensagem')
    sent_at = models.DateTimeField(default=timezone.now, verbose_name='Data de Envio')
    read = models.BooleanField(default=False, verbose_name='Lido')

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['read']),
            models.Index(fields=['-sent_at']),
        ]

    def __str__(self):
        return f'Mensagem de {self.name} <{self.email}>'

    def mark_as_read(self):
        self.read = True
        self.save(update_fields=['read'])

    def mark_as_unread(self):
        self.read = False
        self.save(update_fields=['read'])

    def formatted_date(self):
        return self.sent_at.strftime('%d/%m/%Y %H:%M')

    def short_message(self):
        return (self.message[:75] + '...') if len(self.message) > 75 else self.message
    
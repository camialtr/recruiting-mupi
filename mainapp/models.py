from django.db import models
from django.utils import timezone

class Message(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name='Nome Completo'
    )

    email = models.EmailField(
        verbose_name='Email'
    )

    message = models.TextField(
        verbose_name='Mensagem'
    )

    sended_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data de Envio'
    )

    read = models.BooleanField(
        default=False,
        verbose_name='Lida'
    )

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['-sended_at']

        indexes = [
            models.Index(fields=['read']),
            models.Index(fields=['-sended_at']),
        ]

    def __str__(self):
        return f'Mensagem de {self.name} <{self.email}>'
    
    def mark_as_read(self):
        self.read = True
        self.save()

    def mark_as_unread(self):
        self.read = False
        self.save()

    def formatted_date(self):
        return self.data_envio.strftime('%d de %B de %Y às %H:%M')
    
    def short_message(self):
        return (f'{self.message[":50"]}...') if len(self.message) > 75 else self.message
    
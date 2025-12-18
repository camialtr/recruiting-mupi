from django.contrib.auth.models import User
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
        local_time = timezone.localtime(self.sent_at)
        return local_time.strftime('%d/%m/%Y %H:%M')

    def short_message(self):
        return (self.message[:50] + '...') if len(self.message) > 75 else self.message


class AuditLog(models.Model):
    """Registro de auditoria para ações administrativas"""
    ACTION_TYPES = (
        ('view', 'Visualização'),
        ('unview', 'Remoção de visualização'),
        ('edit', 'Edição'),
        ('delete', 'Exclusão'),
        ('create_user', 'Criação de usuário'),
        ('change_password', 'Alteração de senha'),
        ('delete_user', 'Exclusão de usuário'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Usuário')
    action = models.CharField(max_length=20, choices=ACTION_TYPES, verbose_name='Ação')
    description = models.TextField(verbose_name='Descrição')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data/Hora')
    
    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username if self.user else "Sistema"}: {self.description}'
    
    def formatted_date(self):
        local_time = timezone.localtime(self.created_at)
        return local_time.strftime('%d/%m/%Y %H:%M')
    
    @classmethod
    def log(cls, user, action, description):
        """Método helper para criar logs facilmente"""
        return cls.objects.create(user=user, action=action, description=description)
    
from django.db import models


class ServiceCredentials(models.Model):
    host = models.CharField(max_length=255)
    token = models.CharField(max_length=255, null=True, blank=True)
    service = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.service}'

    class Meta:
        verbose_name = 'Service credentials'
        verbose_name_plural = 'Services credentials'
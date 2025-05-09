from django.db import models
from django.conf import settings

# Create your models here.

TYPES = [
    ('TEXT','text'),
    ('NUMBER','number'),
    ('DATE','date'),
    ('SELECT','select'),
]

class Form(models.Model):
    title = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='forms')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_forms')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and self.creator:
            self.owners.add(self.creator)

    def __str__(self):
        return self.title


class Field(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=100, blank=False)
    type = models.CharField(max_length=10, choices=TYPES)
    choices = models.JSONField(null=True, blank=True)
    is_required = models.BooleanField(default=False)
    regex_validation = models.CharField(max_length=100, blank=True, null=True)
    placeholder = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.label
class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)
    response = models.JSONField()

# TODO: Add Functionality: Delete Form when now owners left
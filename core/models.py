from django.db import models
from django.contrib.auth.models import User

# Create your models here.

TYPES = [
    ('text','text'),
    ('number','number'),
    ('date','date'),
    ('select','select'),
]

class Form(models.Model):
    title = models.CharField()
    created_on = models.DateField(auto_now_add=True)

class Field(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField()
    type = models.CharField(max_length=10, choices=TYPES)
    required = models.BooleanField(default=True)

    regex_validation = models.CharField(blank=True, null=True)

    placeholder = models.CharField()

class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    response = models.JSONField()
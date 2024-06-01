from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    
    
class Task(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    title = models.CharField(max_length=20,unique=True,null=False,blank=False)
    description = models.TextField(default="")
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)


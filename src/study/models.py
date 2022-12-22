from django.db import models
from user.models import User

class StudyGuide(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    public = models.BooleanField(default=False)
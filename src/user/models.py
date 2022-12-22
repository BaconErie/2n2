from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    hashed_password = models.TextField()
    date_created = models.DateTimeField()
    ok_after = models.DateTimeField() # Any token created BEFORE this date is INVALID
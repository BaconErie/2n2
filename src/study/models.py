from django.db import models
from user.models import User

class StudyGuide(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    public = models.BooleanField(default=False)



class QAReference(models.Model):
    # This class keeps track of the many questions and answers a Q&A question may have
    # We can't just use a many to many relationship because we want to know which questions are part of the same Q&A Question
    study_guide = models.ForeignKey(StudyGuide, on_delete=models.CASCADE)

class QAQuestion(models.Model):
    content = models.TextField()
    reference_qa = models.ForeignKey(QAReference, on_delete=CASCADE)

class QAAnswer(models.Model):
    content = models.TextField()
    reference_qa = models.ForeignKey(QAReference, on_delete=CASCADE)



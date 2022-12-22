from django.db import models
from user.models import User

class StudyGuide(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    last_updated = models.DateTimeField()
    public = models.BooleanField(default=False)



class QAReference(models.Model):
    '''Keeps track of the many questions and answers a Q&A question may have
    We can't just use a many to many relationship because we want to know which questions are part of the same Q&A Question'''
    study_guide = models.ForeignKey(StudyGuide, on_delete=models.CASCADE)

class QAQuestion(models.Model):
    content = models.TextField()
    reference_qa = models.ForeignKey(QAReference, on_delete=models.CASCADE)

class QAAnswer(models.Model):
    content = models.TextField()
    reference_qa = models.ForeignKey(QAReference, on_delete=models.CASCADE)



class FormulaQuestion(models.Model):
    study_guide = models.ForeignKey(StudyGuide, on_delete=models.CASCADE)
    formula_string = models.TextField()

class FormulaTemplate(models.Model):
    question = models.ForeignKey(FormulaQuestion, on_delete=models.CASCADE)
    template_string = models.TextField()



class StudyProgress(models.Model):
    '''Keeps track of how many times a user has gotten a question correct'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qa_question = models.ForeignKey(QAReference, on_delete=models.CASCADE)
    formula_question = models.ForeignKey(FormulaQuestion, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=200)
    times_correct = models.IntegerField(default=0)

    @property
    def question(self):
        if self.question_type == 'QAReference':
            return self.qa_question
        
        elif self.question_type == 'FormulaQuestion':
            return self.formula_question
    
    @question.setter
    def question(self, new_question):
        self.question_type = type(new_question).__name__

        if self.question_type == 'QAReference':
            self.qa_question = new_question
            self.formula_question = None
        
        elif self.question_type == 'FormulaQuestion':
            self.formula_question = new_question
            self.qa_question = None
from django.db import models

# Create your models here.
class StudentProfile(models.Model):
    username = models.CharField(max_length=100, blank=False)
    email = models.EmailField()
    
    avg_score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.username} - Student Profile'
    
    def __repr__(self) -> str:
        return f'<StudentProfile: {self.username} - {self.email}>'
        
class EmailPreset(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=120)
    body = models.TextField()

    def __str__(self) -> str:
        return f'{self.recipient} - Subject: {self.subject}'
    
    def __repr__(self) -> str:
        return f'<{self.recipient}><Subject: {self.subject}>'
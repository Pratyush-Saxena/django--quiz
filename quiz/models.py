from django.db import models
import jsonfield
json_default="""[
  {
    "Value": " ",
    "Answer": false
  },
  {
    "Value": " ",
    "Answer": false
  },
  {
    "Value": " ",
    "Answer": false
  },
  {
    "Value": " ",
    "Answer": false
  }
]"""
# Create your models here.
class question(models.Model):
    question=models.CharField(max_length=1000)
    answer=jsonfield.JSONField(default=json_default)
    score=models.IntegerField(default=5)
    level=models.CharField(max_length=50,default="Easy")
    def __str__(self):
        return self.level
    
    
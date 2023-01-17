from django.db import models

# Create your models here.
class AI_model(models.Model):
    model = models.FileField(null=False, upload_to='model/')
    version = models.CharField(max_length=200)
    use_type = models.BooleanField(default=False)
    total_cnt = models.IntegerField(default=0)
    predict_cnt = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    

    
class Result(models.Model):
    image = models.ImageField(blank=True, upload_to='img/%Y/%m/')
    answer = models.CharField(max_length=10)
    result = models.CharField(max_length=10)
    predict = models.BooleanField(default=True)
    model = models.ForeignKey(AI_model, on_delete=models.SET_NULL, null=True)
    pub_date = models.DateTimeField('date published')
    





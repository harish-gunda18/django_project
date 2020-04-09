from django.db import models
# Create your models here.


class Words(models.Model):
    word = models.CharField(max_length=30)
    meaning = models.TextField()
    example_sentence = models.TextField()
    level = models.IntegerField()

    def __str__(self):
        return self.word

from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mastered_list = models.TextField(default='[]')
    reviewed_list = models.TextField(default='[]')
    new_list = models.TextField(default='[]')
    image = models.ImageField(default="default.jpg", upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def set_mastered_list(self, s):
        self.mastered_list = json.dumps(s)

    def get_mastered_list(self):
        return json.loads(self.mastered_list)

    def set_reviewed_list(self, s):
        self.reviewed_list = json.dumps(s)

    def get_reviewed_list(self):
        return json.loads(self.reviewed_list)

    def set_new_list(self, s):
        self.new_list = json.dumps(s)

    def get_new_list(self):
        return json.loads(self.new_list)

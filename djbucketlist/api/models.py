from django.db import models

# Create your models here.
class Bucketlist(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    owner = models.ForeignKey('auth.User', default=-1, related_name='bucketlists', on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)


    def __str__(self):
        """return a human readable instance of this class"""
        return "{}".format(self.name)


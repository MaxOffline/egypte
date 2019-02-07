from django.db import models
from django.contrib.auth.models import User



# Bedding products model
class product(models.Model):
    currentuser      = models.CharField(max_length = 50, blank = True )
    creator          = models.CharField(max_length = 50, blank = True, default = "")
    productname      = models.CharField(max_length = 50, blank = True, )
    productcategory  = models.CharField(max_length = 50, blank = True)
    sessionkey       = models.CharField(max_length = 50, blank = True)
    productimage1    = models.ImageField(upload_to = "bedding/", blank = True)
    productimage2    = models.ImageField(upload_to = "bedding/", blank = True)
    productimage3    = models.ImageField(upload_to = "bedding/", blank = True)
    productimage4    = models.ImageField(upload_to = "bedding/", blank = True)
    productimage5    = models.ImageField(upload_to = "bedding/", blank = True)
    productimage6    = models.ImageField(upload_to = "bedding/", blank = True)
    productadded     = models.BooleanField(default = False)
    orderedTime      = models.DateTimeField(auto_now_add = True)
    submitted        = models.BooleanField(default = False)
    stock            = models.IntegerField(blank = True, null = True)
    def __str__(self):
        return(str(self.currentuser))

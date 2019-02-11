from django.db import models
from django import forms
from django.contrib.auth.models import User


class userProfile(models.Model):
    user           = models.OneToOneField(
                    User,
                    on_delete = models.CASCADE,
                    null      = True,
                    )
    firstname      = models.CharField(
                    verbose_name = "First Name",
                    max_length = 20,
                    blank = True,
                    null = True,
                    )
    lastname       = models.CharField(
                    max_length = 20,
                    blank = True,
                    verbose_name = "Last Name",
                    null = True
                    )
    mobile         = models.IntegerField(
                    blank = True,
                    null = True,
                    verbose_name = "Mobile"
                    )
    streetAdrress1 = models.CharField(
                    max_length = 100,
                    blank = True,
                    verbose_name = "Street Address",
                    null = True
                    )
    streetAdrress2 = models.CharField(
                    max_length = 100,
                    blank = True,
                    verbose_name = "Street Address 1",
                    null = True
                    )
    city           = models.CharField(
                    max_length = 100,
                    blank = True,
                    verbose_name = "City",
                    null = True
                    )
    state          = models.CharField(
                    max_length = 100,
                    blank = True,
                    verbose_name = "State",
                    null = True
                    )
    zip            = models.IntegerField(
                    blank = True,
                    verbose_name = "ZIP Code",
                    null = True
                    )


    def __str__(self):
        return(str(self.id))

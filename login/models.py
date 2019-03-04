from django.db import models
from django import forms
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.storage import default_storage as storage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

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

    image          = models.ImageField(
                    upload_to = "Profile_Pix/",
                    blank=True,
                    null=True
                    )




    def save(self, *args, **kwargs):
        super(userProfile, self).save(*args, **kwargs)
        previous = userProfile.objects.get(id = self.id)
        if self.image.width > 128:
            orig = Image.open(self.image)
            orig.thumbnail((128,128), Image.ANTIALIAS)
            fileBytes = BytesIO()
            orig.save(fileBytes, format="JPEG")
            memoryFile = InMemoryUploadedFile(fileBytes, None, str(self.user) + "_thumb.JPG", 'image/jpeg',1, None)
            self.image = memoryFile
            self.image.save(self.image.name, self.image)




    def __str__(self):
        return(str(self.id))

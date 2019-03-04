from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from product.models import product
from django.core.files.storage import default_storage as AWSstorage




class productImages(models.Model):
    productImage      = models.ForeignKey(product, on_delete = models.CASCADE)

    image1            = models.ImageField(
                        # We could use upload_to = models.FileField(storage=S3BotoStorage(bucket='other-bucket'))
                        upload_to = "Product_Images/",
                        blank = True,
                        null = True
                        )
    image2            = models.ImageField(
                        upload_to = "Product_Images/",
                        blank = True,
                        null = True
                        )
    image3            = models.ImageField(
                        upload_to = "Product_Images/",
                        blank = True,
                        null = True
                        )
    image4            = models.ImageField(
                        upload_to = "Product_Images/",
                        blank = True,
                        null = True
                        )
    image5            = models.ImageField(
                        upload_to = "Product_Images/",
                        blank = True,
                        null = True
                        )
    image6            = models.ImageField(
                        upload_to = "Product_Images/",
                        blank = True,
                        null = True
                        )


    def save(self, *args, **kwargs):

        super(productImages, self).save(*args, **kwargs)
        allimgs = [ self.image1,
                    self.image2,
                    self.image3,
                    self.image4,
                    self.image5,
                    self.image6,
                ]
        for im in allimgs:

            previous = productImages.objects.get(id = self.id)

            if im and im.width > 128:
                orig = Image.open(im)
                orig.thumbnail((128,128), Image.ANTIALIAS)
                fileBytes = BytesIO()
                orig.save(fileBytes, format="JPEG")
                memoryFile = InMemoryUploadedFile(
                                                fileBytes,
                                                None,
                                                str(self.productImage) + "_thumb.JPG",
                                                'image/jpeg',
                                                1,
                                                None
                                                )
                im = memoryFile
                # you can add the Folder path before the imagename to specify a folder in the bucket
                AWSstorage.save("Product_Images/"+im.name, im)


    def __str__(self):
        return(str(self.productImage))

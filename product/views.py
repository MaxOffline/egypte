import datetime
from PIL import Image
from django.views import generic
from django.conf import settings
from product.models import product
from django.views.generic import View
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect




#This is the mainpage view
class index(View):

    template_name = "egytemp/index.html"

    def get(self,request):

        return render(request, self.template_name,{})



# Beddingcatrgory
class beddingCatrgory(View):
    model = product.objects.filter(
                                productcategory = "bedding",
                                creator         = "Maxoffline",
            )

    template_name = "egytemp/productshow.html"

    def get(self,request):

        return render(request, self.template_name,{"product":self.model})



# AntiquesCategory
class antiquesCategory(View):

    # All of the antiques product
    model = product.objects.filter(
                                productcategory = "antiques",
                                creator         = "Maxoffline",
                                )

    template_name = "egytemp/productshow.html"

    def get(self,request):

        return render(request, self.template_name,{"product":self.model})






class productDetails(generic.DetailView):

    model = product
    template_name = "egytemp/productdetails.html"





class cartView(View):

    template_name = "egytemp/cart.html"

    def get(self, request):

        # Check if the user is logged in
        if request.user.is_authenticated:

            # We will get all the products he added
            findItems = product.objects.filter(
                                            currentuser  = request.user,
                                            productadded = True ,
                                            submitted    = False,
                                            )

            return render(
            request, self.template_name, {"cartitems" : findItems}
            )


        # If the user is not logged in, We will get all the products he added by the session id
        else:

            sessionItems = product.objects.filter(
                                                sessionkey   = str(request.session.session_key),
                                                productadded = True,
                                                submitted    = False
                                                )
            return render(
            request, self.template_name, {"sessionItems" : sessionItems}
            )








# What happens when user clicks add to cart
class addToCart(View):

    def post(self,request):

        try:

            findSession = Session.objects.get(pk = request.session.session_key)

        # If session key doesn't exist, We will create one and use the key
        except Session.DoesNotExist:

            createSession = request.session.create()

        sessionid       = request.session.session_key
        user            = request.POST["currentuser"]
        productLabel    = request.POST["productname"]
        productcategory = request.POST["productcategory"]
        added           = request.POST["productadded"]
        productid       = request.POST["productid"]
        productimage    = request.POST["productimage"]
        quantity        = request.POST["count"]

        # Get the total stock of the item
        totalStock      = product.objects.get(
                        productname = productLabel,
                        creator = "Maxoffline",
                        )

        # Check stock
        if totalStock.stock < int(quantity):

            return HttpResponse(
            "Sorry, We don't have enough stock. Please select a different number"
                                )

        # IF THE USER IS NOT LOGGED IN
        # we will search and see if the that session already exists in our model database
        if not request.user.is_authenticated:

            findProductsWithSession = product.objects.filter(
                                    productname = productLabel,
                                    sessionkey  = sessionid,
                                    submitted   = False,
                                    )

            for i in findProductsWithSession:

                currentStock = i.stock

            # if there are no items with the same session ID
            if not findProductsWithSession:

                # We will create a new one then add the product to the database
                createProduct = product.objects.create(
                                                    productimage1 = productimage,
                                                    productname   = productLabel,
                                                    sessionkey    = sessionid,
                                                    stock         = quantity,
                                                    productadded  = True
                                                    )

            else:
                # We will update the current ones
                product.objects.filter(
                                    productname = productLabel,
                                    sessionkey  = sessionid,
                                    submitted   = False
                                    ).update(
                                            productimage1 = productimage,
                                            productadded  = True,
                                            stock         = int(currentStock) +
                                                            int(quantity),
                                            )

        # IF THE USER IS LOGGED IN
        else:

            findProduct = product.objects.filter(
                                            currentuser = request.user,
                                            productname = productLabel,
                                            submitted   = False
                                            )

            # Check if there is a unsubmitted product in DB so we can update quantity
            if findProduct:

                for i in findProduct:
                    currentStock = i.stock

                updateQuantity = product.objects.filter(
                                currentuser = request.user,
                                productname = productLabel,
                                submitted = False
                                ).update(
                                        stock         = int(currentStock) +
                                                        int(quantity),
                                        productadded  = True,
                                        productimage1 = productimage
                                        )
            else:

                createProduct = product.objects.create(
                                                    productimage1 = productimage,
                                                    currentuser = request.user,
                                                    productname = productLabel,
                                                    productadded = True,
                                                    submitted = False,
                                                    stock = quantity,
                                                    )

        return HttpResponseRedirect(""+productid+"/itemshow/")
        #Just another method for rendering.
        # return HttpResponseRedirect(reverse('product:item:5'))




class Submitted_View(View):

    template_name = "egytemp/Summary.html"

    # We will use this time to get all the items that was submitted lastly.
    now = datetime.datetime.now()

    # get the last item in items that has submitted = True
    def post(self,request):

        if request.POST["Submit"] == "Submit Order":
            allproducts = product.objects.filter(
                                                currentuser=request.user,
                                                productadded = True,
                                                submitted = False,
                                                productname = request.POST["productname"]
                                                )

            for item in allproducts:

                # Get the TOTAL stock of the ORIGINAL ITEM
                totalStock = product.objects.get(creator = "Maxoffline", productname = item.productname)

                if request.POST["quantity"] != item.stock:

                    updateProduct = allproducts.update(
                                                    stock = int(request.POST["quantity"])
                                                    )


                #if item stock is bigger than the total stock return render message
                if item.stock > totalStock.stock:

                    return HttpResponse("Sorry, We don't have enough stock of " + item.productname)

                # Get the stock of the items added and deduct them from the OIRIGINAL ITEM TOTAL
                else:
                    deduct   = product.objects.filter(
                                                    creator = "Maxoffline",
                                                    productname = item.productname
                                                    ).update(
                                                            stock = totalStock.stock-int(item.stock)
                                                            )

                    changeLastorder = product.objects.filter(
                                                            currentuser = request.user,
                                                            submitted = True,
                                                            count = 998
                                                            ).update(count = 0)



            # update the cart items to Submitted = True andorderedTime = now.
                    updateItems = product.objects.filter(
                                                    currentuser=request.user,
                                                    productadded = True,
                                                    submitted = False
                                                    ).update(
                                                            submitted = True,
                                                            orderedTime=self.now,
                                                            count = 998,
                                                            )

            # The order Summary items
                    orderSummary = product.objects.filter(
                                                        currentuser=request.user,
                                                        productadded = True,
                                                        submitted = True,
                                                        count=998
                                                        )


                    # send_mail('Subject here',"Yaaay",settings.EMAIL_HOST_USER,['maxoffline2@gmail.com'],
                    # fail_silently=False,)

                    # subject, from_email = 'Order Summary', settings.EMAIL_HOST_USER
                    #
                    # html_content = render_to_string('egytemp/Summary.html', {"items":torender}) # render with dynamic value
                    # text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.
                    #
                    # # create the email, and attach the HTML version as well.
                    # msg = EmailMultiAlternatives(subject, text_content, from_email, ['maxoffline2@gmail.com'])
                    # msg.attach_alternative(html_content, "text/html")
                    # msg.send()

                    return render(request,self.template_name,{"items":orderSummary})

        elif request.POST["Submit"] == "Delete":

            if request.user.is_authenticated:

                product.objects.filter(
                                    currentuser = request.user,
                                    productname = request.POST["productname"],
                                    id = request.POST["id"]
                                    ).delete()

                return redirect("product:show")

            else:

                product.objects.filter(
                                    sessionkey = request.session.session_key,
                                    productname = request.POST["productname"],
                                    id = request.POST["id"]
                                    ).delete()

                return redirect("product:show")
        else:
            return redirect("index")


from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
class upload(View):
    def post(self, request):
        image = request.FILES['pic']
        #Save the image first to the DB
        default_storage.save(image.name, image)
        #Open the file in the DB
        thisdude = default_storage.open(image.name)
        #Use the opened file in the DB in Images
        img = Image.open(thisdude)
        # Resize that babe
        img.thumbnail((128, 128), Image.ANTIALIAS)
        #Get the Bytes of the file from memory
        thumbnailString = BytesIO()
        #Save the image with the bytes as JPEG
        img.save(thumbnailString, format='JPEG')
        #Get the file in the memory
        thumb_file = InMemoryUploadedFile(thumbnailString, None, 'foo.jpg', 'image/jpeg',1, None)
        #Save it to the DB
        default_storage.save("abc.jpg", thumb_file)
        return redirect("index")








































#My 7 years old typed this so I'm sorry but I'm not deleting it :)

# i remeber years ago someone told me i should take caution when it comes to love
# i did and you were strong and i was not my illusion my mistake i was careless i
# forgot i did and now when all is done there is nothing to say you have gone and
#  so effortlessly you have won you can go ahead tell them tell them all i know now
#  shout it from the roof tops write it on the sky line all we had is gone now tell
#  them i was happy and my heart is broken all my scars are open tell them what i
#  hoped would be impossible impossible impossible impossible







#

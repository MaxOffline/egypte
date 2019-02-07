import datetime
from django.shortcuts import render, redirect
from django.views.generic import View
from product.models import product
from django.views import generic
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse, reverse_lazy





#This is the mainpage view
class index(View):
    model = product.objects.filter(creator = "Maxoffline")
    template_name = "egytemp/index.html"

    def get(self,request):
        return render(request, self.template_name,{"all":self.model,})








class beddingView(View):
    model = product.objects.filter(creator = "Maxoffline", productcategory = "bedding")
    template_name = "egytemp/productshow.html"

    def get(self,request):
        return render(request, self.template_name,{"product":self.model})














class Antiques(View):
    # This loop over stock is for using the stock numbers in the HTML option input if needed.
    #stock = []
    template_name = "egytemp/productshow.html"
    model = product.objects.filter(creator = "Maxoffline", productcategory = "antiques")
    # for i in model:
    #     totalstock = i.stock
    #     for number in range(totalstock+1):
    #         stock.append(number)
    def get(self,request):
        return render(request, self.template_name,{"product":self.model})





class itemView(generic.DetailView):

    model = product
    template_name = "egytemp/productdetails.html"

    # context_object_name = 'product'
    # queryset = product.objects.all()












class showProduct(View):
    template_name = "egytemp/cart.html"

    def get(self, request):
        # If the user is logged in,
        # We will get all the products he added with the request.user and added = True

        if request.user.is_authenticated:
            findItems = product.objects.filter(currentuser = request.user,
                                               productadded = True ,
                                               submitted = False)
            return render(request, self.template_name, {"cartitems" : findItems})


        # If the user is not logged in, We will get all the products he added by the session id
        else:
            sessionItems = product.objects.filter(sessionkey = str(request.session.session_key),
                                                  productadded = True,
                                                  submitted = False)
            return render(request, self.template_name, {"sessionItems" : sessionItems})

















#This global variable is used to for deducting from the total stock.
#count = 0
class addToCart(View):

    def post(self,request):

        #global count

        # Check if a session exists.
        try:
            findsession = Session.objects.get(pk = request.session.session_key)

        # If session key doesn't exist, We will create one and use the key
        except Session.DoesNotExist:
            createSession = request.session.create()
        sessionid        = request.session.session_key
        user             = request.POST["currentuser"]
        productLabel     = request.POST["productname"]
        productcategory  = request.POST["productcategory"]
        added            = request.POST["productadded"]
        productid        = request.POST["productid"]
        productimage     = request.POST["productimage"]
        #count            = request.POST["count"]
        quantity              = request.POST["count"]
        totalStock         = product.objects.get(creator = "Maxoffline", productname = productLabel)

        if totalStock.stock < int(quantity):
            return HttpResponse("Sorry, We don't have enough stock. Please select a different number")
        # if the user is NOT logged in
        # we will search and see if the that session already exists in our model database
        if not request.user.is_authenticated:
            findmodelsession = product.objects.filter(sessionkey=sessionid)

            for i in findmodelsession:
                currentStock = i.stock
            # if it does NOT exist
            # We will create a new one then add the product to the database and change "addedtocart" to True.
            #if not findmodelsession:

            if not findmodelsession:
                createmodel   = product.objects.create(sessionkey =sessionid,
                productname = productLabel, productadded = True, stock = quantity, productimage1 = productimage )

            else:
                findcurrentProduct = product.objects.filter(sessionkey=sessionid, productname = productLabel, submitted = False)
                if findcurrentProduct:
                    product.objects.filter(sessionkey=sessionid, productname = productLabel, submitted = False).update(
                    stock = int(currentStock) + int(quantity), productadded = True, productimage1 = productimage)
                else:
                    createmodel   = product.objects.create(sessionkey =sessionid,
                    productname = productLabel, productadded = True, stock = quantity, productimage1 = productimage )
            # if it does.
            # then we will need to add that product to cart by creating a new object and changing the "productadded" to True.
            #else:
                # updateuser    = product.objects.create(sessionkey = sessionid,
                #                 productname=productLabel,productadded=True )

        # if the user is already logged in and adds the item to cart.
        # then we will just create a object and change the "Currentuser" to request.user
        else:
            findcurrent = product.objects.filter(currentuser = request.user, productname = productLabel, submitted = False)



            if findcurrent:
                for i in findcurrent:
                    currentStock = i.stock

                updateuser = product.objects.filter(currentuser = request.user, productname = productLabel, submitted = False).update(
                stock = int(currentStock) + int(quantity), productadded = True, productimage1 = productimage)
            else:
                createModel = product.objects.create(currentuser = request.user, productname = productLabel,
                 submitted = False , stock = quantity, productadded = True, productimage1 = productimage)

        return HttpResponseRedirect(""+productid+"/itemshow/")
        # return HttpResponseRedirect(reverse('product:item:5'))










class Submitted_View(View):
    template_name = "egytemp/Summary.html"
    # We will use this time to get all the items that was submitted lastly.
    now = datetime.datetime.now()

    # get the last item in items that has submitted = True
    # then get it's time.
    def post(self,request):
        #findobj = product.objects.filter(currentuser=request.user).last()
        if request.POST["Submit"] == "Submit Order":
            allproducts = product.objects.filter(currentuser=request.user, productadded = True,
             submitted = False, productname = request.POST["productname"])


            for item in allproducts:
                # Get the TOTAL stock of the ORIGINAL ITEM
                totalStock = product.objects.get(creator = "Maxoffline", productname = item.productname)

                if request.POST["quantity"] != item.stock:
                    updateProduct = allproducts.update(stock = int(request.POST["quantity"]))


                #if item stock is bigger than the total stock return render message
                if item.stock > totalStock.stock:
                    return HttpResponse("Sorry, We don't have enough stock of " + item.productname)
                #else deduct
                # Get the stock of the items added and deduct them from the OIRIGINAL ITEM TOTAL
                else:
                    deduct   = product.objects.filter(creator = "Maxoffline", productname = item.productname).update(
                    stock = totalStock.stock-int(item.stock))




            # update the cart items to Submitted = True andorderedTime = now.
            updated = product.objects.filter(currentuser=request.user, productadded = True, submitted = False).update(
            submitted = True,orderedTime=self.now)

            # search for all the products for the User, added= True, Submitted = True, orderedTime= Now
            # The order items Summary
            torender = product.objects.filter(currentuser=request.user,
            productadded = True, submitted = True,orderedTime=self.now)


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

            return render(request,self.template_name,{"items":torender})
        elif request.POST["Submit"] == "Delete":
            if request.user.is_authenticated:
                product.objects.filter(currentuser = request.user, productname = request.POST["productname"], id = request.POST["id"]).delete()
                return redirect("product:show")
            else:
                product.objects.filter(sessionkey = request.session.session_key, productname = request.POST["productname"], id = request.POST["id"]).delete()
                return redirect("product:show")
        else:
            return redirect("index")

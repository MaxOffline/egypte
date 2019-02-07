from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import Register
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from product.models import product
from django.contrib.sessions.models import Session
from django.urls import reverse_lazy
from login.models import userProfile



class register(View):
    registerationForm = Register
    template_name = "egytemp/register.html"

    allusers = User.objects.all()

    def get(self, request):
        return render(request,self.template_name, {"form" : self.registerationForm} )

    def post(self, request):
        form = self.registerationForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            password2 = form.cleaned_data["ConfirmPassword"]
            email = form.cleaned_data["email"]
            email2 = form.cleaned_data["ConfirmEmail"]
            for i in self.allusers:
                if i.email == email or i.username == username:
                    return render(request, self.template_name,{"registered":"User is already registered","form":self.registerationForm(None)})
                elif password != password2 :
                    return render(request, self.template_name,{"passwordmatch":"Passwords don't match","form":self.registerationForm(None)})
                elif email != email2 :
                    return render(request, self.template_name,{"emailmatch":"Email addresses don't match","form":self.registerationForm(None)})


                else:
                    user.set_password(password)
                    user.save()
                    login(request,user)
                    createProfile = userProfile.objects.create(user = request.user)
                    return redirect("index")

        return render(request,self.template_name,{})








class loginView(View):
    template_name = "egytemp/login.html"
    def get(self,request):
        return render(request,self.template_name, {})

    def post(self,request):
        session_key = request.session.session_key
        #findsession = Session.objects.get(pk = request.session.session_key)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None :
            if user.is_active:
                login(request, user)

                # if the user logs in
                # we will search for all the sessions in any product.
                try:
                    findsession = product.objects.filter(sessionkey = str(session_key))
                except Session.DoesNotExist:
                    return redirect("product:cart")
                else:
                    # We will get all the items with the same session id
                    # Then we will check and see if there is a product with the same name for the same user, submitted =FASLE
                    # If there is then we will get the stock of that session's item and add it to the current user's item
                    # Then we will delete that item with the same session and product name
                    # then we will update the "Currentuser" to the request.user
                    findsession = product.objects.filter(sessionkey = str(session_key))
                    for i in findsession:
                        check = product.objects.filter(productname = i.productname, currentuser = request.user, submitted = False)
                        for number in check:
                            if check:
                                update = check.update(stock = int(i.stock) + number.stock)
                                delete = product.objects.filter(sessionkey = str(session_key), productname = i.productname).delete()
                    else:
                        updateuser = findsession.update(currentuser = str(request.user))
                        return redirect("index")

        else:
            return render(request, self.template_name,
            {"error":"Please enter the correct ID and Password"})






class logoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")




class createProfile(CreateView):
    model = userProfile
    success_url = reverse_lazy("index")
    template_name = "egytemp/userprofile_form.html"
    fields = ['firstname','lastname','mobile', 'streetAdrress1', 'streetAdrress2','city', 'state','zip','profilepicture']
    #This function is for validation the form and changing value of inputs after submittion
    #I'm using it here to define the current user of each objectself.
    #I could replace it by adding ("user" : self.request.user.userprofile.user or self.request.user ) in the get_initial
    def form_valid(self, form):
        form.instance.id = self.request.user.id
        form.instance.user = self.request.user
        return super().form_valid(form)





class updateProfile(UpdateView):
    model = userProfile
    success_url = reverse_lazy("index")
    template_name = "egytemp/userprofile_form.html"
    fields = ['firstname','lastname','mobile', 'streetAdrress1', 'streetAdrress2','city', 'state','zip','profilepicture']


    #This function adds initial value for the form profile
    # def get_initial(self):
    #     return {
    #             "zip" : self.request.user.userprofile.zip,
    #             "city" : self.request.user.userprofile.city,
    #             "state" : self.request.user.userprofile.state,
    #             "mobile" : self.request.user.userprofile.mobile,
    #             "streetAdrress1" : self.request.user.userprofile.streetAdrress1,
    #             "streetAdrress2" : self.request.user.userprofile.streetAdrress2,
    #             "profilepicture" : self.request.user.userprofile.profilepicture,
    #             }






















#

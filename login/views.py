from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.urls import reverse_lazy
from login.models import userProfile
from product.models import product
from .forms import Register







class register(View):
    
    template_name = "egytemp/register.html"
    allUsers = User.objects.all()
    registerationForm = Register
    
    def get(self, request):
        return render(
                    request,
                    self.template_name,
                    {"form" : self.registerationForm}
                    )

    def post(self, request):
        
        form = self.registerationForm(request.POST)

        if form.is_valid():
            
            user      = form.save(commit = False)
            username  = form.cleaned_data["username"]
            password  = form.cleaned_data["password"]
            password2 = form.cleaned_data["ConfirmPassword"]
            email     = form.cleaned_data["email"]
            email2    = form.cleaned_data["ConfirmEmail"]
            
            # Validating inputs 
            for i in self.allUsers:
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
                    # createProfile = userProfile.objects.create(user = request.user)
                    return redirect("index")

        return render(request,self.template_name,{})








class loginView(View):
    
    template_name = "egytemp/login.html"
    
    def get(self,request):
        
        return render(
                    request,
                    self.template_name,
                    {})

    def post(self,request):
        
        #findsession = Session.objects.get(pk = request.session.session_key)
        username    = request.POST["username"]
        password    = request.POST["password"]
        session_key = request.session.session_key
        user        = authenticate(username=username, password=password)
        
        if user is not None :
            
            if user.is_active:
                
                login(request, user)
                
                try:
                    
                    # we will search for all the sessions in any product.
                    findsession = product.objects.filter(sessionkey = str(session_key))
                    
                except Session.DoesNotExist:
                    
                    return redirect("index")
                
                else:
                    
                    # We will get all the items with the same session id
                    findSession = product.objects.filter(sessionkey = str(session_key))
                    
                    
                    for i in findSession:
                        
                        # Then we will check and see if there is a product with the same name and user
                        check = product.objects.filter(
                                productname = i.productname,
                                currentuser = request.user,
                                submitted = False
                                )
                        
                        for number in check:
                            
                            # If there is an object 
                            if check:
                                
                                #we will get the stock of that session's item and add it to the #current   #user's item
                                update = check.update(
                                        stock = int(i.stock) + number.stock
                                        )
                                
                                # Then we will delete that item with the same session and product name
                                delete = product.objects.filter(
                                        sessionkey = str(session_key),
                                        productname = i.productname
                                        ).delete()
                                
                    else:
                        #If no items with same session id
                        #Change the username of the session to the current user's username
                        updateUser = findsession.update(currentuser = str(request.user))
                        return redirect("index")

        else:
            return render(
                        request,
                        self.template_name,
                        {"error":"Please enter the correct ID and Password"}
                        )






class logoutView(View):
    
    def get(self, request):
        
        logout(request)
        return redirect("index")


    
    


class createProfile(CreateView):
    
    model = userProfile
    success_url = reverse_lazy("index")
    template_name = "egytemp/userprofile_form.html"
    fields = [
            'firstname',
            'lastname',
            'mobile',
            'streetAdrress1',
            'streetAdrress2',
            'city',
            'state',
            'zip',
            ]
  
    #I could replace it by adding ("user" : self.request.user.userprofile.user or self.request.user ) in the #get_initial method
    def form_valid(self, form):
        form.instance.id = self.request.user.id
        form.instance.user = self.request.user
        return super().form_valid(form)





class updateProfile(UpdateView):
    
    model = userProfile
    success_url = reverse_lazy("index")
    template_name = "egytemp/userprofile_form.html"
    fields = [
            'firstname',
            'lastname',
            'mobile',
            'streetAdrress1',
            'streetAdrress2',
            'city',
            'state',
            'zip',
            ]


    def get_initial(self):
        
     return {
             "zip" : self.request.user.userprofile.zip,
             "city" : self.request.user.userprofile.city,
             "state" : self.request.user.userprofile.state,
             "mobile" : self.request.user.userprofile.mobile,
             "streetAdrress1" : self.request.user.userprofile.streetAdrress1,
             "streetAdrress2" : self.request.user.userprofile.streetAdrress2,
             }







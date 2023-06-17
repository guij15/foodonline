from django.shortcuts import render,redirect

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

def check_vendor(user):
    if user.user_type==User.RESTAURANT:
        return True
    else:
        raise PermissionDenied

def check_customer(user):
    if user.user_type==User.CUSTOMER:
        return True
    else:
        raise PermissionDenied
    


# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('customerdashboard')
    elif request.method =='POST':
        print(request.POST)
        form=UserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(  form.cleaned_data['password'])
            user.user_type=User.CUSTOMER
            user.save() 
            messages.success(request,'User Created Successfully')
            return redirect('registerUser')
        else:
            context={
            'form':form,
            }
            return render(request,'accounts/registerUser.html',context)
       
        """first_name=form.cleaned_data['first_name']
           last_name=form.cleaned_data['last_name']
           username=form.cleaned_data['username']
           email=form.cleaned_data['email']
           password=form.cleaned_data['password']
           user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
           user.save() """
        
            

    else:
        form=UserForm()
        context={
        'form':form,
        }
        return render(request,'accounts/registerUser.html',context)
    

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('vendordashboard')
    elif request.method =='POST':
        form=UserForm(request.POST)
        v_form=VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.user_type=User.RESTAURANT
            user.save() 
            vendor=v_form.save(commit=False)
            vendor.user=user
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request,'Vendor Created Successfully')
            return redirect('registerVendor')
        else:
            print(form.errors)
    else:
        form=UserForm()
        v_form=VendorForm()
    context={
    'form':form,
    'v_form':v_form,
    }
    return render(request,'accounts/registerVendor.html',context) 

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('customerdashboard')
    elif request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            return redirect('myAccount')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
            
        """user=User.objects.get(email=email)
        if user.check_password(password):
            if user.user_type==User.RESTAURANT:
                return redirect('vendor_dashboard')
            else:
                return redirect('customer_dashboard')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')"""
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You are now logged out')
    return redirect('login')

@login_required(login_url='login')
@user_passes_test(check_customer)
def customerdashboard(request):
    return render(request,'accounts/customerdashboard.html')

@login_required(login_url='login')
@user_passes_test(check_vendor)
def vendordashboard(request):
    return render(request,'accounts/vendordashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirect_url=detectUser(user)
    return redirect(redirect_url)
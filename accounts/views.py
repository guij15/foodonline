from django.shortcuts import render,redirect

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if request.method =='POST':
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
    if request.method =='POST':
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

    
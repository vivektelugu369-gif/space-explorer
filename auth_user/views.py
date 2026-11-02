from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == 'POST':
        a = request.POST['fname']
        b = request.POST['lname']
        c = request.POST['uname']
        d = request.POST['email']
        e = request.POST['pasw']
        f = request.POST['cpasw']
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        # check for password match
        if e != f:
            messages.error(request,'Passwords do not match')
            return render(request,'register.html')

        # check for username exists or not
        if  User.objects.filter(username=c).exists():
            messages.error(request,'Username already exists')
            return render(request,'register.html')
        # check for email exists or not
        if  User.objects.filter(email=d).exists():
                messages.error(request,'email already exists')
                return render(request,'register.html')
        u = User.objects.create_user(
            first_name = a,
            last_name = b,
            username = c,
            email = d,
            password=e
        )
        UserProfile.objects.create(
             user = u,
             phone = phone,
             image = image
        )
        messages.success(request,'Registration successfull...!')
        
        # try:
        #     User.objects.get(username=c)
        #     messages.error(request,'user name already exists...!')
        #     return render(request,'register.html',{'error':True})
        # except:
            # u = User.objects.create(
            #     first_name = a,
            #     last_name = b,
            #     username = c,
            #     email = d
            # )
            # u.set_password(e)
            # u.save()
            # messages.success(request,'registration successfull...!')
    return render(request,'register.html')

def login_(request):
    if request.method == 'POST':
        a = request.POST['uname']
        b = request.POST['pasw']
        user = authenticate(username=a,password=b)
        if user:
            login(request,user)
            messages.success(request,'login successfull....!')
            return redirect('home')
        else:
            messages.error(request,'username or password is incorrect')
            return redirect('login_')
    return render(request,'login_.html')

def logout_(request):
     logout(request)
     return redirect('register')

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults = {'phone':''}
    )
    return render(request,'profile.html',{'profile':profile})

@login_required
def update_profile(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults = {'phone':''}
    )
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.username = request.POST.get('uname')
        user.email = request.POST.get('email')
        user.save()

        profile.phone = request.POST.get('phone')
        if request.FILES.get('image'):
            profile.image = request.FILES.get('image')
        profile.save()
        return redirect('profile')
    return render(request,'update_profile.html',{'profile':profile})


@login_required
def reset_password(request):
    if request.method == 'POST':

        if 'opasw' in request.POST:
            old_password = request.POST.get('opasw')

            user = authenticate(
                request,
                username=request.user.username,
                password=old_password
            )

            if user:
                return render(request, 'reset_password.html', {'new': True})
            else:
                messages.error(request, 'Entered password is incorrect.')
                return redirect('reset_password')

        elif 'npasw' in request.POST:
            new_password = request.POST.get('npasw')
            confirm_password = request.POST.get('ncpasw')

            if new_password != confirm_password:
                messages.error(request, "Passwords don't match.")
                return render(request, 'reset_password.html', {'new': True})

            user = request.user
            user.set_password(new_password)
            user.save()

            messages.success(request, 'Password updated successfully!')
            return redirect('profile')

    return render(request, 'reset_password.html')

# def reset_password(request):
#     if request.method == 'POST':
#         if 'opasw' in request.POST:
#             a = request.POST['opasw']
#             user = authenticate(password=a)
#             if user:
#                 messages.success(request,'Enter new Password')
#                 return render(request,'reset_password.html',{'new':True})
#             else:
#                 messages.error(request,'Entered password is wrong')
#                 return redirect('reset_password')
#         if 'npasw' in request.POST:
#             b = request.POST['npasw']
#             user = user.objects.get(username=user)

#             if b != 'cpasw':
#                 messages.error(request,'password doesnt match')
#                 return redirect('reset_password')
#             user.set_password('npasw')
#             user.save()
#             messages.success(request,'password updated successfully....!')
#             return redirect('login_')
#     return render(request,'reset_password.html')

# def forget_password(request):
#     if request.method == 'POST':
#         a = request.POST['uname']
#         if a in request.POST:

#     return render(request,'forget_password.html')

def forget_password(request):
    if request.method == 'POST':
        # Step 1: User enters username
        if 'uname' in request.POST:
            uname = request.POST['uname']
            try:
                user = User.objects.get(username=uname)
                request.session['fp_user'] = user.username
                # Pass both flags in one context dictionary
                return render(request, 'forget_password.html', {'new': True, 'old': user})
            except User.DoesNotExist:
                messages.error(request, "User not found")
                return redirect('forget_password')

        # Step 2: User enters new password
        if 'npasw' in request.POST:
            new_pass = request.POST['npasw']
            conf_pass = request.POST['cnpasw']

            uname = request.session.get('fp_user')
            if not uname:
                messages.error(request, "Session expired. Try again.")
                return redirect('forget_password')

            user = User.objects.get(username=uname)

            if new_pass != conf_pass:
                messages.error(request, "Passwords do not match")
                return redirect('forget_password')

            if user.check_password(new_pass):
                messages.error(request, "New password cannot be same as old password")
                return redirect('forget_password')

            user.set_password(new_pass)
            user.save()
            messages.success(request, "Password updated successfully. Please login.")
            return redirect('login_')

    # Default page load
    return render(request, 'forget_password.html', {'new': False})

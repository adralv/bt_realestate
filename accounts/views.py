from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from contacts.models import Contact

# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Successful login!")
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login! Try agian.')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('index')
    # else:
    #     messages.error(request, "You must login first.")
    #     return redirect('login')
    # return render(request, 'accounts/logout.html')

def register(request):
    if request.method == "POST":
        # register user
        # messages.error(request, "testing errxr messages")
        # get data from forms
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        # password check
        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        else:
            # check if unique username
            if User.objects.filter(username = username).exists():
                messages.error(request, "That username is taken!")
                return redirect('register')
            else:
                # check if email is user
                if User.objects.filter(email=email).exists():
                    messages.error(request, "That email is being used!")
                    return redirect('register')
                else:
                    newUser = User.objects.create_user(username=username, password=password, email=email,first_name=first_name,last_name=last_name)
                    # save new user
                    newUser.save()
                    messages.success(request, "User is created! You may log in.")
                    return redirect('login')
                
    else:
        return render(request, 'accounts/register.html')

def dashboard(request):
    user_inquiries = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'inquiries' : user_inquiries,
    }
    return render(request, 'accounts/dashboard.html', context)

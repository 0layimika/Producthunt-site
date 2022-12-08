from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
def signup(request):
    if request.method == 'POST':
        #user wants to sign up
        if request.POST['password'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html',{'error':'Username is not available'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password'])
                auth.login(request,user)
                return redirect('home')
        else:
                return render(request, 'accounts/signup.html', {'error': 'Password must match'})

    else:
        #user wants to enter info
        return render(request,'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/signin.html', {'error':'username or password is incorrect.'})
    else:
        return render(request,'accounts/signin.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    else:
        return render(request,'accounts/signup.html')
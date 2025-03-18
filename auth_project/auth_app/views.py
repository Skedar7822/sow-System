from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


# ✅ Register View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('dashboard')

    return render(request, 'auth/register.html')
# ✅ Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Fix: Pass request to form
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)  # Fix authentication
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid username or password")  

    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})

# ✅ Dashboard View (Only for Logged-in Users)
@login_required(login_url='/auth/login/')
def dashboard_view(request):
    return render(request, 'auth/dashboard.html')

# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

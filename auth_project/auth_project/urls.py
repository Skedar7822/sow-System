from django.contrib import admin
from django.urls import path, include
from auth_app.views import login_view  # Import your home page view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('', login_view, name='login'),  # Set the root URL to dashboard (or another view)
]

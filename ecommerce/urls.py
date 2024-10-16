"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

admin.site.site_header = 'E-Commerce Administration'
admin.site.index_title = 'Admin Panel'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('', RedirectView.as_view(url='/admin/', permanent=False)),  # Redirect root URL to /home/
    path('__debug__/', include(debug_toolbar.urls)),
]

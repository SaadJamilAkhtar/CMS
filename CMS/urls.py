"""CMS URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from API.views import *
from main.views import *

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', index, name='index'),
                  path('dashboard/', dashboard, name='dashboard'),
                  path('client/<int:id>', getClient, name='client'),
                  path('edit/<int:id>', edit, name='edit'),
                  path('delete/<int:id>', delete, name='delete'),
                  path('logout', log_out, name='logout'),
                  path('add', add, name='add'),
                  path('api/v1/get/clients', ClientView.as_view(), name='API'),
                  path('apikey', getApiKey, name='apikey'),
                  path('apikey/delete', deleteApiKey, name='delApiKey'),
                  path('addGroup', addGroup, name='add-group'),
                  path('editGroup/<int:id>', editGroup, name='edit-group'),
                  path('groups/', groupView, name='groups'),
                  path('deleteGroup/<int:id>', deleteGroup, name='delete-group'),
                  path('addField', addNewField, name='add_field'),
                  path('editField/<int:id>', editExtraField, name='edit-field'),
                  path('fields', showAllFields, name='fields'),
                  path('fields/delete/<int:id>', deleteExtraField, name='del-field'),

                  path('test', form_renderer)

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

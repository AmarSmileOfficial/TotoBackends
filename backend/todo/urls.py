"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
 
# add include to the path
from django.urls import path, include
 
# import views from todo
from todo import views
 
urlpatterns = [
    path('todo/api/create/', views.CreateTodo.as_view(), name='create-todo'),
    path('todo/api/list/', views.ListTodos.as_view(), name='list-todo'),
    path('todo/api/update/', views.UpdateTodo.as_view(), name='update-todo'),
    path('todo/api/retrieve/', views.RetrieveTodo.as_view(), name='deatils-todo'),
    path('todo/api/delete/', views.DeleteTodo.as_view(), name='delete-todo'),
]


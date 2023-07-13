"""
URL configuration for justDigitalDiary project.

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

from hello import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.sign_in, name='signIn'),
    path('postSignIn/', views.post_sign_in, name='postSignIn'),
    path('logout/', views.logout, name="logout"),
    path('postSignUp/', views.post_sign_up, name='postSignUp'),
    path('adminReq/', views.admin_req, name="adminReq"),
    path('postAdminReq/', views.post_admin_req, name="postAdminReq"),
    path('adminReqList/', views.admin_req_list, name="adminReqList"),
    path('postAdminReqAccept/', views.post_admin_req_accept, name='postadminReqAccept'),
    path('postAdminReqReject/', views.post_admin_req_reject, name='postadminReqReject'),
    path('adminList/', views.admin_list, name="adminList"),
    path('postAdminRemove/', views.post_admin_remove, name="postAdminRemove"),
    path('addTea/', views.add_tea, name='addTea'),
    path('postAddTea/', views.post_add_tea, name='postAddTea'),
    path('addStu/', views.add_stu, name='addStu'),
    path('postAddStu/', views.post_add_stu, name='postAddStu'),
    path('stuList/', views.stu_list, name='stuList'),
    path('teaList/', views.tea_list, name='teaList'),
    path('sAdminStuList/', views.s_admin_stu_list, name='sAdminStuList'),
    path('sAdminTeaList/', views.s_admin_tea_list, name='sAdminTeaList')
]

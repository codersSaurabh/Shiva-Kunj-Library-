from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('book/', views.book, name='book'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('admin-login/', views.admin, name='admin-login'),
    path('logout/',views.logout,name="logout"),
    path('admin_fee/',views.admin_fee,name="admin_fee"),
    path('admin_sheets/',views.admin_sheets,name="admin_sheets"),
    path('adminportal/remove/<int:id>/', views.remove_student, name='remove'),
    path('adminportal/mark-paid/<int:id>/', views.mark_paid, name='mark_paid'),
    path('adminportal/send-reminder/', views.send_reminder, name='send_reminder'),
    path('adminportal/search/', views.admin_search, name='admin_search'),

    
]
